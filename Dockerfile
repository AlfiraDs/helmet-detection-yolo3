# Get base image
FROM python:slim-buster

LABEL maintainer="sanket.deshmukh@globant.com"

# Update Debian package list
RUN apt-get update

# install cv2 based packages
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install python3-opencv -y

# 
WORKDIR /code

# 
COPY requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# d 
COPY app /code/app

EXPOSE 5000 
# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]

