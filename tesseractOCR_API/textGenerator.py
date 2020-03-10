from flask import Flask, request, jsonify, request
from flask_restful import Api, Resource
import subprocess
import json
import requests
from PIL import Image
import pytesseract
import argparse
import cv2
import os

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_check():
	return 'Hello Soni'
def checkPostedData(postedData, route):
        if route == 'ocr':
                if 'url' not in postedData:
                        return 301
                else:
                        return 200
class OCR(Resource):
	def post(self):
		
		postedData = request.get_json()
		checkData = checkPostedData(postedData, 'ocr')
		if checkData != 200:
                        retJson = {
                                'status code': 301,
                                'message': 'URL is missing'
                        }
                        return jsonify(retJson)
		imageURL = postedData['url']
		r = requests.get(imageURL)
		with open('doc.jpg', 'wb') as f:
			f.write(r.content)
			process = subprocess.Popen(['python', './model/ocr.py', '--image', 'doc.jpg'])
			process.communicate()[0]
			process.wait()
		with open('res.txt', 'r') as g:
			retJson = json.load(g)
		return retJson
api.add_resource(OCR, '/ocr')
		

if __name__ == '__main__':
	app.run()

