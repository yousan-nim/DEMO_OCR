

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


[
{'id': 0, 'box': [[86, 80], [134, 80], [134, 128], [86, 128]], 'text': '西', 'score': 0.6588299684045182}, 
{'id': 1, 'box': [[187, 75], [469, 75], [469, 165], [187, 165]], 'text': '愚园路', 'score': 0.9601406073752329},
 {'id': 2, 'box': [[517, 81], [565, 81], [565, 123], [517, 123]], 'text': '东', 'score': 0.9935730580773452}, 
 {'id': 3, 'box': [[78, 126], [136, 126], [136, 156], [78, 156]], 'text': '315', 'score': 0.9999928421498292}, 
 {'id': 4, 'box': [[514, 124], [574, 124], [574, 156], [514, 156]], 'text': '309', 'score': 0.9999728139709217}, 
 {'id': 5, 'box': [[81, 175], [125, 175], [125, 211], [81, 211]], 'text': 'I', 'score': 0.9386335118164233}, 
 {'id': 6, 'box': [[226, 171], [414, 171], [414, 220], [226, 220]], 'text': 'Yuyuan Rd。', 'score': 0.47561011318964314}, 
 {'id': 7, 'box': [[529, 173], [569, 173], [569, 213], [529, 213]], 'text': 'E', 'score': 0.5179032005942332}
 ]