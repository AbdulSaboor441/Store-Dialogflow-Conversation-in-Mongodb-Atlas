from flask import Flask, request
from flask_ngrok import run_with_ngrok
import pymongo
import json

with open('config.json')as file:
    params = json.load(file)['params']


app = Flask(__name__)
run_with_ngrok(app)

client = pymongo.MongoClient(params['client_url'])
db = client[params['db']]

@app.route('/webhook',methods =['Post','GET'])

def webhook():
    req = request.get_json(force = True)
    query = req['queryResult']['queryText']
    result = req['queryResult']['fulfillmentText']
    data = {
        "query":query,
        'result': result
    }

    col = db['chat_data']
    col.insert_one(data)
    print("data got inserted into db")

    


if __name__ == "__main__":
    app.run()
