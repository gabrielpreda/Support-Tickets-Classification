import sys
from flask import Flask, jsonify, request, make_response, abort
import os
import time
import logging
import pickle
import re

IS_LOCAL = False
IS_DEBUG = False

# Use with Azure Web Apps
if(IS_LOCAL):
    os.environ['PATH'] = r'C:\Program_Files\Anaconda3;' + os.environ['PATH']
else:
    os.environ['PATH'] = r'D:\home\python354x64;' + os.environ['PATH']
sys.path.append(".")
sys.path.append("..")
sys.path.append("webservice/models")
sys.path.append("wwwroot/models")
    
app = Flask(__name__)
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__), 'models'))

# Download models
if(IS_LOCAL):
    print("Model loaded locally")
else:
    from models.download_models import download_file, download_models
    download_models()

# Loading models
model_impact = pickle.load(
    open(
        os.path.join(__location__, "impact.model"), "rb"
    )
)
model_ticket_type = pickle.load(
    open(
        os.path.join(__location__, "ticket_type.model"), "rb"
    )
)
model_category = pickle.load(
    open(
        os.path.join(__location__, "category.model"), "rb"
    )
)


model_business_service = pickle.load(
    open(
        os.path.join(__location__, "business_service.model"), "rb"
    )
)
    
model_urgency = pickle.load(
    open(
        os.path.join(__location__, "urgency.model"), "rb"
    )
)
    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Service not found'}), 404)


@app.route('/')
def index():
    return """
        <html>
        <body>
        
        This is a simple web service for support tickets classification written in Python using <a href=""http://flask.pocoo.org/"">Flask</a> module.<br>
        Please read the API documentation for more details.
        </body>
        </html>
        """

if(IS_DEBUG):
	@app.route('/endava/api/v1.0/status', methods=['GET'])
	def status():
	    return jsonify({'status': "OK"})

@app.route('/endava/api/v1.0/predictall', methods=['POST'])
def predictall():
    ts = time.gmtime()
    logging.info("Request received - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    if (not request.json) or ('description' not in request.json):
        abort(400)
    description = request.json['description']
    description = preprocess_data(description)

    predicted_ticket_type = model_ticket_type.predict([description])[0]
    print("predicted ticket_type: "+str(predicted_ticket_type))

    predicted_category = model_category.predict([description])[0]
    print("predicted category: "+str(predicted_category))

    predicted_impact = model_impact.predict([description])[0]
    print("predicted impact: "+str(predicted_impact))

    predicted_business_service = model_business_service.predict([description])[0]
    print("predicted business_service: "+str(predicted_business_service))

    predicted_urgency = model_urgency.predict([description])[0]
    print("predicted urgency: "+str(predicted_urgency))

    ts = time.gmtime()
    logging.info(
        "Request sent to evaluation - %s"
        % time.strftime("%Y-%m-%d %H:%M:%S", ts)
    )
    return jsonify({
        "description": description,
        "ticket_type": predicted_ticket_type,
        "business_service": predicted_business_service,
        "category": predicted_category,
        "impact": predicted_impact,
        "urgency": predicted_urgency
    })


@app.route('/endava/api/v1.0/category', methods=['POST'])
def category1():
    ts = time.gmtime()
    logging.info("Request received - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    print(request)
    print(request.json)
    if not request.json or 'description' not in request.json:
        abort(400)
    description = request.json['description']
    print(description)

    predicted = model_category.predict([description])
    print("Predicted: "+str(predicted))

    ts = time.gmtime()
    logging.info("Request sent to evaluation - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    return jsonify({"category": predicted[0]})


@app.route('/endava/api/v1.0/tickettype', methods=['POST'])
def tickettype():
    ts = time.gmtime()
    logging.info("Request received - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    print(request)
    print(request.json)
    if not request.json or 'description' not in request.json:
        abort(400)
    description = request.json['description']
    print(description)

    predicted = model_ticket_type.predict([description])
    print("Predicted: " + str(predicted))

    ts = time.gmtime()
    logging.info("Request sent to evaluation - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    return jsonify({"ticket_type": predicted[0]})

@app.route('/endava/api/v1.0/impact', methods=['POST'])
def impact():
    ts = time.gmtime()
    logging.info("Request received - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    print(request)
    print(request.json)
    if not request.json or 'description' not in request.json:
        abort(400)
    description = request.json['description']
    print(description)

    predicted = model_impact.predict([description])
    print("Predicted: " + str(predicted))

    ts = time.gmtime()
    logging.info("Request sent to evaluation - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    return jsonify({"impact": predicted[0]})


@app.route('/endava/api/v1.0/urgency', methods=['POST'])
def urgency():
    ts = time.gmtime()
    logging.info("Request received - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    print(request)
    print(request.json)
    if not request.json or 'description' not in request.json:
        abort(400)
    description = request.json['description']
    print(description)

    predicted = model_urgency.predict([description])
    print("Predicted: " + str(predicted))

    ts = time.gmtime()
    logging.info("Request sent to evaluation - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    return jsonify({"urgency": predicted[0]})

@app.route('/endava/api/v1.0/business_service', methods=['POST'])
def business_service():
    ts = time.gmtime()
    logging.info("Request received - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    print(request)
    print(request.json)
    if not request.json or 'description' not in request.json:
        abort(400)
    description = request.json['description']
    print(description)

    predicted = model_business_service.predict([description])
    print("Predicted: " + str(predicted))

    ts = time.gmtime()
    logging.info("Request sent to evaluation - %s" % time.strftime("%Y-%m-%d %H:%M:%S", ts))
    return jsonify({"business service": predicted[0]})


# Data prep - much to improve :)
regexArr1 = []
regexArr2 = []


def getRegexList1():
    regexList = []
    regexList += ['From:(.*)']  # from line
    regexList += ['Sent:(.*)']  # sent to line
    regexList += ['Received:(.*)']  # received data line
    regexList += ['To:(.*)']  # to line
    regexList += ['CC:(.*)']  # cc line
    regexList += ['https?:[^\]\n\r]+']  # https & http
    regexList += ['Subject:']
    regexList += ['[\w\d\-\_\.]+@[\w\d\-\_\.]+']  # emails
    return regexList


def getRegexList2():
    regexList = []
    regexList += ['From:']  # from line
    regexList += ['Sent:']  # sent to line
    regexList += ['Received:']  # received data line
    regexList += ['To:']  # to line
    regexList += ['CC:']  # cc line
    regexList += ['The information(.*)infection']  # footer
    regexList += ['Endava Limited is a company(.*)or omissions']  # footer
    regexList += ['The information in this email is confidential and may be legally(.*)interference if you are not the intended recipient']  # footer
    regexList += ['\[cid:(.*)]']  # images cid
    regexList += ['https?:[^\]\n\r]+']  # https & http
    regexList += ['Subject:']
    regexList += ['[\w\d\-\_\.]+@[\w\d\-\_\.]+']  # emails
    regexList += ['[\\r]']  # \r\n
    regexList += ['[\\n]']  # \r\n

    regexList += ['^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$']
    regexList += ['[^a-zA-Z]']

    return regexList


def preprocess_data(data):
    print(data)
    content = data.lower()
    content = content.split('\\n')

    for word in content:
        for regex in regexArr1:
            word = re.sub(regex.lower(), ' ', word)

    print(content)
    content = "".join(content)
    print(content)

    for regex in regexArr2:
        content = re.sub(regex.lower(), ' ', content)
    print(content)

    return content


if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    regexArr1 = getRegexList1()
    regexArr2 = getRegexList2()

    app.run(HOST, PORT)
