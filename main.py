from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_restful import Resource, Api, reqparse
import spacy
import pandas as pd
import json
import os
import csv
from PIL import Image
from werkzeug.utils import secure_filename
from cloudmersive_api import extract
from cloudmersive_extract import predict
from ResumeParser.main import transform
from text_summariser import generate_summary
from ResumeAndFeedbackClassifier.test import classify
app = Flask(__name__)
api= Api(app)
app.config['SECRET_KEY']='mysecretkey'

nlp=spacy.load('en_core_web_sm')

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj

class Dashboard(Resource):
    def __init__(self):
        pass
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index2.html'),200,headers)

class Classifier(Resource):
    def post(self):
        f = request.files['file-name']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        reg_dic = extract(file_path)                                            
        headers = {'Content-Type':'text/html'}
        return make_response(render_template('registration.html',text_data=reg_dic),200,headers)

    def get(self):
        headers = {'Content-Type':'text/html'}
        dic = dict()
        return make_response(render_template('registration.html',data=dic),200,headers)


class Resume(Resource):
    def post(self):
        f = request.files['file-name']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        resume_string = extract(file_path)                                            
        dic = dict()
        nlp = spacy.load('en')
        dic = transform(dic, nlp,resume_string)
        for x in dic[0]:
            if type(dic[0][x]) == set:
                dic[0][x] = list(dic[0][x])
        # dic[0] is tuple of lists(which contains key-value pair)
        print('DATA CONTENT OF DIC[0]',dic[0])
        headers = {'Content-Type':'text/html'}
        keys = []
        values = []
        count = 0
        with open('top_skills.csv', 'r') as csvfile: 
            csvreader = csv.reader(csvfile) 
            for row in csvreader:
                if count==0:
                    keys = row
                    count = count+1
                else:
                    values = row
        print('keys',keys)
        print('values',values)
        skills = []
        for i in range(len(keys)): 
            skills.append([keys[i],values[i]]) 
        print('skills',skills)
        return make_response(render_template('resume.html',text_data=dic[0],skills=skills),200,headers)

    def get(self):
        headers = {'Content-Type':'text/html'}
        dic={}
        skills = {}
        return make_response(render_template('resume.html',text_data=dic,skills=skills),200,headers)
        

    
class Sentimental(Resource):
    def post(self):
        f = request.files['file-name']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        reg_dic = extract(file_path)     
        senti_output = predict(reg_dic,True)
        headers = {'Content-Type':'text/html'}
        return make_response(render_template('sentimental.html',text_data=senti_output),200,headers)

    def get(self):
        headers = {'Content-Type':'text/html'}
        dic=""
        return make_response(render_template('sentimental.html',text_data=dic),200,headers)


class Summarizer(Resource):
    def post(self):
        f = request.files['file-name']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        sents_in_summary = 5
        summary_string = extract(file_path)
        doc = nlp(summary_string)  
        text = generate_summary(doc,sents_in_summary)
        print(text)
        headers = {'Content-Type':'text/html'}
        return make_response(render_template('summarizer.html',text_data=text),200,headers)
    
    def get(self):
        headers = {'Content-Type':'text/html'}
        data = ""
        return make_response(render_template('summarizer.html',text_data=data),200,headers)
  
class Inbox(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('inbox.html'),200,headers)



api.add_resource(Dashboard, '/')
api.add_resource(Inbox, '/inbox')
api.add_resource(Classifier, '/classifier')
api.add_resource(Resume, '/resume')
api.add_resource(Sentimental, '/sentimental') #feedback
api.add_resource(Summarizer, '/summarizer')


if __name__ == "__main__":
    app.run(debug=True)
