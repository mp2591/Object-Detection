
import io
import os
import argparse
import datetime
import torch
import seaborn #import it explicitly since it causes problem if not imported
from PIL import Image
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"

@app.route("/", methods=["GET"])
def get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def pred():
    file = extract_img(request)
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    model = torch.hub.load('ultralytics/yolov5','yolov5s',
                           pretrained=True)
    model.eval()
    results = model(img,size=640)
    results.render()

    time = datetime.datetime.now().strftime(DATETIME_FORMAT)
    img_savename = f"static/{time}.png"
    Image.fromarray(results.ims[0]).save(img_savename)

    return redirect(img_savename)

def extract_img(request):
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if not file:
        return 
    else:
        return file

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    
    app.run(host='0.0.0.0')
                


