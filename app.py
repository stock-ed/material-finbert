from finbert.finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
import nltk
import db
import fcntl
import os
from logging import Logger
# from transformers import AutoModelForSequenceClassification

nltk.download('punkt')
model_path = 'models/classifier_model/finbert-sentiment'
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=3, cache_dir=None)

# model = AutoModelForSequenceClassification.from_pretrained(model_path,num_labels=3,cache_dir=None)


def score(text):
    return(predict(text, model).to_json(orient='records'))


def get_not_analyzed_stocks():
    return [{"id": 1, "tweet_text": "it is good news for aapl"}]


def main_process():
    analysis_count = 600
    conn = db.Conn('')
    stocks = db.get_not_analyzed_stocks(analysis_count)
    for stock in stocks:
        sentiment_score = score(stock.tweet_text)
        db.update_sentiment(conn, id, sentiment_score)


def run(lockfile, application):
    "check mysql replication and handle errors"

    # add file lock first to sure only 1 process is running on this instance
    if not os.path.exists(lockfile):
        os.system("touch %s" %(lockfile))

    f = open(lockfile, "r")

    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
        Logger.debug("get file lock on %s success" %(lockfile))
        application()
    except Exception, e:
        msg = "can't get lock. The script is already running"
        Logger.error(msg)


if __name__ == '__main__':
    lockfile = 'lockfile.txt'
    run(lockfile, main_process)
