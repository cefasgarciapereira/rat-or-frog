from flask import Flask, jsonify, render_template, request
from PIL import Image
from joblib import load
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return 'No file part'

    file = request.files['image']

    # If the user submits an empty form
    if file.filename == '':
        return 'No selected file'
    
    res = process_image(file=file)

    return render_template('result.html',  frog=int(res[0]), rat=int(res[1]), animal=("frog" if int(res[0]) > int(res[1]) else "rat"))
  

def process_image(file):
  mlp = load("./filename.joblib")
  img = Image.open(file)
  img = img.resize(size=(64,64))
  img = img.convert("L")
  img = list(img.getdata())
  res = mlp.predict_proba([img])
  res = [res[0][0]*100, res[0][1]*100]
  return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)