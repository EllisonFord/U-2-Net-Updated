## Updated for Torch 11.8

Removed all errors and warnings. Made it specifically for training and creating new models.

### Instructions

1. Check what versions of CUDA PyTorch are currently available [here](https://pytorch.org/ "PyTorch homepage")
2. Based on that go to NVIDIA and download that version of CUDA
3. Go back to the PyTorch website and PIP install Torch, this code works well for 11.8 and the pip command is below 

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

4. Finally do `pip install -r requirements.txt` to get the couple of requirements installed that were not by default in the PyTorch installation
