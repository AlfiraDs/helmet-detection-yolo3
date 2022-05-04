# YOLOv3-FastAPI-Helmate-Detection

This project provided YOLOv3 Model based helmate detection prediction to users. 
Supports JPEG/JPG images only.

## Installation

This project uses Python 3.8 for operation and is venv based. 

```bash
python -m venv  fastapienv
source fastapienv/bin/activate 
pip install -r requirements.txt
```

## Usage

For dev and debugging :

```python
uvicorn app.main:app --port 5000 
```

Python Dev URL :  http://127.0.0.1:5000/docs


For pre-deployment testing : 

```docker
docker build -t hdtr-yolov3:v1 .

docker run -p 5050:5000 -t hdtr-yolov3:v1

```

Docker URL : http://127.0.0.1:5050/docs


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Contact : Sanket Deshmukh 

## License
[MIT](https://choosealicense.com/licenses/mit/)


<!-- python -m venv  fastapienv
source fastapienv/bin/activate 
uvicorn app.main:app --port 5000 
http://127.0.0.1:5000/docs


docker build -t hdtr-yolov3:v1 .

docker run -p 5000:5000 -t hdtr-yolov3:v1 -->
