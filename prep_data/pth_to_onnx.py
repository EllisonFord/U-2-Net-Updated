import torch.onnx
from model import U2NET


def main():
    # Load the trained model from file
    trained_model = U2NET(3, 1)
    checkpoint_path = "../saved_models/mcnet/mcnet_checkpoint.pth"  # Update with your .pth file path

    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path)

    # Extract the model state dictionary
    model_state_dict = checkpoint['model_state_dict']

    trained_model.load_state_dict(model_state_dict)
    trained_model.eval()

    # trained_model.load_state_dict(torch.load(checkpoint_path))
    # trained_model.eval()

    # Create a dummy input tensor.
    # The shape of the dummy input should match the input shape of the model
    # For U2NET, assuming input size is 320x320, change if necessary
    dummy_input = torch.randn(1, 3, 320, 320)

    # Set the model to evaluation mode
    trained_model.eval()

    # Export the model to an ONNX file
    output_onnx = 'output_model.onnx'  # Name of the output ONNX file
    torch.onnx.export(trained_model, dummy_input, output_onnx,
                      export_params=True,
                      opset_version=11,  # Set the ONNX version
                      do_constant_folding=True,
                      input_names=['input'],
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})

    print(f"Model successfully converted to ONNX and saved to {output_onnx}")


if __name__ == "__main__":
    main()
