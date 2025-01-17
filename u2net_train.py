import torch
import torch.nn as nn

from torch.utils.data import DataLoader
from torchvision import transforms
import torch.optim as optim

import glob
import os
from typing import Dict

from data_loader import RescaleT
from data_loader import RandomCrop
from data_loader import ToTensorLab
from data_loader import SalObjDataset

from model import U2NET


# ------- 1. define loss function --------
bce_loss = nn.BCELoss(reduction='mean')


def muti_bce_loss_fusion(d0, d1, d2, d3, d4, d5, d6, labels_v):
    loss0 = bce_loss(d0, labels_v)
    loss1 = bce_loss(d1, labels_v)
    loss2 = bce_loss(d2, labels_v)
    loss3 = bce_loss(d3, labels_v)
    loss4 = bce_loss(d4, labels_v)
    loss5 = bce_loss(d5, labels_v)
    loss6 = bce_loss(d6, labels_v)

    loss = loss0 + loss1 + loss2 + loss3 + loss4 + loss5 + loss6
    print("l0: %3f, l1: %3f, l2: %3f, l3: %3f, l4: %3f, l5: %3f, l6: %3f\n" % (
        loss0.data.item(), loss1.data.item(), loss2.data.item(), loss3.data.item(), loss4.data.item(),
        loss5.data.item(),
        loss6.data.item()))

    return loss0, loss


# ------- 2. set the directory of training dataset --------

model_name = 'mcnet'  # 'u2netp'

data_dir = os.path.join(os.getcwd(), 'train_data' + os.path.sep)
tra_image_dir = os.path.join('DUTS-TR-Image' + os.path.sep)
tra_label_dir = os.path.join('DUTS-TR-Mask' + os.path.sep)

label_ext = '.png'

model_dir = os.path.join(os.getcwd(), 'saved_models', model_name + os.path.sep)

epoch_num = 100_000
batch_size_train = 12
batch_size_val = 1
train_num = 0
val_num = 0

tra_img_name_list = glob.glob(data_dir + tra_image_dir + '*.jp*g')

tra_lbl_name_list = []
for img_path in tra_img_name_list:
    img_name = img_path.split(os.path.sep)[-1]

    aaa = img_name.split(".")
    bbb = aaa[0:-1]
    imidx = bbb[0]
    for i in range(1, len(bbb)):
        imidx = imidx + "." + bbb[i]

    tra_lbl_name_list.append(data_dir + tra_label_dir + imidx + label_ext)

print("---")
print("train images: ", len(tra_img_name_list))
print("train labels: ", len(tra_lbl_name_list))
print("---")

train_num = len(tra_img_name_list)

salobj_dataset = SalObjDataset(
    img_name_list=tra_img_name_list,
    lbl_name_list=tra_lbl_name_list,
    transform=transforms.Compose([
        RescaleT(320),
        RandomCrop(288),
        ToTensorLab(flag=0)]))
salobj_dataloader = DataLoader(salobj_dataset, batch_size=batch_size_train, shuffle=True, num_workers=1)

# ------- 3. define model --------
# define the net
net = U2NET(3, 1)
# if(model_name=='u2net'):
#     net = U2NET(3, 1)
# elif(model_name=='u2netp'):
#     net = U2NETP(3,1)

if torch.cuda.is_available():
    net.cuda()

# ------- 4. define optimizer --------
print("---define optimizer...")
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0)


def main():
    # Check for a saved checkpoint
    checkpoint_path = model_dir + model_name + "_checkpoint.pth"
    start_epoch = 0
    if os.path.isfile(checkpoint_path):
        print("=> Loading checkpoint '{}'".format(checkpoint_path))
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']
        net.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print("=> Loaded checkpoint '{}' (epoch {})".format(checkpoint_path, checkpoint['epoch']))
    else:
        print("=> No checkpoint found at '{}'".format(checkpoint_path))

    # ------- 5. training process --------
    print("---start training...")
    ite_num = 0
    running_loss = 0.0
    running_tar_loss = 0.0
    ite_num4val = 0
    save_frq = 20  # save the model every 20 iterations

    for epoch in range(start_epoch, epoch_num):
        net.train()

        for idx, data in enumerate(salobj_dataloader):

            data: Dict[str, torch.Tensor] = data

            ite_num = ite_num + 1
            ite_num4val = ite_num4val + 1

            inputs, labels = data['image'], data['label']

            inputs = inputs.type(torch.FloatTensor)
            labels = labels.type(torch.FloatTensor)

            # wrap them in Variable
            if torch.cuda.is_available():
                inputs_v, labels_v = inputs.cuda(), labels.cuda()
            else:
                inputs_v, labels_v = inputs, labels

            # y zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            d0, d1, d2, d3, d4, d5, d6 = net(inputs_v)
            loss2, loss = muti_bce_loss_fusion(d0, d1, d2, d3, d4, d5, d6, labels_v)

            loss.backward()
            optimizer.step()

            # # print statistics
            running_loss += loss.data.item()
            running_tar_loss += loss2.data.item()

            # del temporary outputs and loss
            del d0, d1, d2, d3, d4, d5, d6, loss2, loss

            print("[epoch: %3d/%3d, batch: %5d/%5d, ite: %d] train loss: %3f, tar: %3f " % (
                epoch + 1, epoch_num, (idx + 1) * batch_size_train, train_num, ite_num, running_loss / ite_num4val,
                running_tar_loss / ite_num4val))

            if ite_num % save_frq == 0:

                # Create the directory if it does not exist
                os.makedirs(model_dir, exist_ok=True)

                checkpoint = {
                    'epoch': epoch,
                    'model_state_dict': net.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'loss': running_loss / ite_num4val,
                    'tar_loss': running_tar_loss / ite_num4val
                }

                torch.save(checkpoint, model_dir + model_name + "_checkpoint.pth")
                print('---💾 saved')
                running_loss = 0.0
                running_tar_loss = 0.0
                ite_num4val = 0


if __name__ == '__main__':
    main()
