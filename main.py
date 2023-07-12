from urllib import response
from flask import Flask,Response,request
from flask_ngrok import run_with_ngrok

# import pymongo for mongodb connection:
import pymongo

# import json for read the parameter (queryText, fullfillmentText)
import json

with open('config.json')as file:
    params = json.load(file)['params']

# i have created an app
app = Flask(__name__)

# i have created an ngrok object so that our app will be running here
run_with_ngrok(app)

# i have created mongodb client
client = pymongo.MongoClient(params['client_url'])

# i have created a mongodb database
db = client[params['db']]

# we create a app route for flask and we have to keep the url like Api url as webhook and methods will get and post both.
@app.route('/webhook',methods =['Post','GET'])


# define a function with the name of the webhook
def webhook():
    # fethching all the data as json request this one by this method
    req = request.get_json(force = True)

    # queryResult like a father parameter, queryText and fullfillmentText parameters present inside the queryResult parameter.So, we will have to pass queryResult inside that we will be accessing queryText and fullfillmentText parameters, you can see in google diallogflow.
    query = req['queryResult']['queryText']
    result = req['queryResult']['fulfillmentText']

    # we can create date like dictionary because mongodb takes dictionary by default. 
    data = {
        "query":query,
        'result': result
    }

    # Iam creating collection in mongodb database and iam inserting the above data(a variable which datatype is dict) with the query and result data
    col = db['chat_data']
    col.insert_one(data)
    print("data got inserted into db")

    # iam returning a response status=200. status = 200 means your application is fine enough to run the code.
    return Response(status=200)



    

# Running the code.
if __name__ == "__main__":
    app.run()
