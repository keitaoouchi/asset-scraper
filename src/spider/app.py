from flask import Flask
import task
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "OK!"

@app.route('/sbiscrape')
def sbi():
    id = os.environ["SBI_ID"]
    pw = os.environ["SBI_PW"]
    bucket = os.environ["BUCKET"]
    task.scrape_sbi(id, pw, bucket)
    return "OK!"


if __name__ == '__main__':
    app.run()