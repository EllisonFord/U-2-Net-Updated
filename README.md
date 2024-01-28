## Updated for CUDA 11.8

Removed all errors and warnings. Made it specifically for training and creating new models.

### Instructions - Zero to Hero

1. Check what versions of CUDA PyTorch are currently available [here](https://pytorch.org/ "PyTorch homepage")
2. Based on that go to NVIDIA and download that version of CUDA, in this example its CUDA 11.8
3. Go back to the PyTorch website and PIP install Torch. For 11.8 this should work: `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
4. Finally, do `pip install -r requirements.txt` to get the couple of requirements that were not in the PyTorch install

### Training

Training is done running the `u2net_train.py` script, I left mask and image directories as they came. Training parameters 
have also not been altered.

During training, the program saves a checkpoint every 200 iterations. This means you can resume training from where the
checkpoint left it last.
