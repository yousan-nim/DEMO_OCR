

from utils import base64_to_pil, np_to_base64 
from flask import Flask, redirect, request, render_template, jsonify, json

import easyocr
# reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
# result = reader.readtext('chinese.jpg')



app = Flask(__name__)

reader = easyocr.Reader(['ch_sim','en'])

def get_prediction(image, reader): 
    result = reader.readtext(image)
    return result

@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict(): 

    if request.method == 'POST': 
        image = base64_to_pil(request.json)
        preds = get_prediction(image, reader)

        result = []
        for idx, data in enumerate(preds): 
            toJson = { 
                "id"   :int(idx),
                "box"  :str(data[0]),
                "text" :data[1],
                "score":int(data[2] * 100),
            }
            result.append(toJson)
        return jsonify(result=result)


if __name__ == '__main__': 
    app.run(debug=True)
