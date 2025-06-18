import os
os.environ["PYTORCH_NO_PIN_MEMORY"] = "1"

import easyocr
import torch

IMAGE_FILEPATH = r"C:\Users\andrew.kim\Documents\CrystalEyes-v0.9.0\assets\sucrose-small.jpg"


print("Making model")
try:
    print("torch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
    # Force pin_memory=False for all dataloaders (monkey-patch)
    for attr in dir(reader):
        obj = getattr(reader, attr)
        if hasattr(obj, 'pin_memory'):
            obj.pin_memory = False
    print("Reading text")
    result = reader.readtext(IMAGE_FILEPATH)
    # print("result: ", result)
except Exception as e:
    print("Exception occurred:", e)

print("the end")


