from flask import Flask
from flask_cors import CORS
import sys
import optparse
import time
from flask import request
import sys
from finbert.finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
import nltk
import os
# from transformers import AutoModelForSequenceClassification

nltk.download('punkt')
app = Flask(__name__)
CORS(app)
start = int(round(time.time()))
model_path = 'models/classifier_model/finbert-sentiment'
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=3, cache_dir=None)

# model = AutoModelForSequenceClassification.from_pretrained(model_path,num_labels=3,cache_dir=None)


@app.route("/sentiment", methods=['POST'])
def score():
    text = request.get_json()['text']
    return(predict(text, model).to_json(orient='records'))


@app.route("/live/ping", methods=['GET'])
def live():
    return 'OK'

if __name__ == '__main__':
    hostEnv = os.getenv('HOST_URL', '0.0.0.0')
    portEnv = os.getenv('HOST_PORT', 8102)
    app.run(host=hostEnv, port=portEnv, debug=False, threaded=True)
    # app.run(host='0.0.0.0', port=8102, debug=False, threaded=True)
