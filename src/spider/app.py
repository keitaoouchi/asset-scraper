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
    bucket = os.environ["SBI_BUCKET"]
    task.scrape_sbi(id, pw, bucket)
    return "OK!"

@app.route('/rakutenscrape')
def rakuten():
    id = os.environ["RAKUTEN_ID"]
    pw = os.environ["RAKUTEN_PW"]
    bucket = os.environ["RAKUTEN_BUCKET"]
    task.scrape_rakuten(id, pw, bucket)
    return "OK!"


if __name__ == '__main__':
    app.run()