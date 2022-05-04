import os 
import cv2
import sys
import numpy as np
import uvicorn
from   fastapi import FastAPI, File, UploadFile

from app.yolov3_utils import *


# Load Environment variables 
port = 5050

# Init
app = FastAPI()

@app.get("/")
def index():
    return {"data" : "Application ran successfully"}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    npimg = np.fromstring(file, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    result = detection_recognition(image)
    return result

# Use below command to rrun
# uvicorn main:app --port 5000  --reload

# if __name__ == "__main__":
#     uvicorn.run("main:app", host='0.0.0.0', port=5050, reload=True)