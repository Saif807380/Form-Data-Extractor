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
from flask_mysqldb import MySQL
from flask import session
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'	
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']	= 'team6nn'
mysql = MySQL(app)
api = Api(app)

app.config['SECRET_KEY']='mysecretkey'

nlp=spacy.load('en_core_web_sm')
class UserLogin(Resource):

    def post(self):
        email =request.form['email']
        password = request.form['password']
        print(email)
        emailt=''
        for i in email:
         if i == '@':
            break
         else:
            emailt=emailt+i
        print(emailt)
        result=""
        try:
            string = "SELECT * FROM "+emailt+" WHERE email = '"+email+"' and password ='"+password+"' "
            cur = mysql.connection.cursor()
            cur.execute(string)
            result = cur.fetchall()
            print(result)
        finally:
            if result == "":
                session['login']='0'
                return redirect(url_for('userlogin'))
            else:
                print(result)
                words = result[0][2].split()
                text = ""
                for word in words:
                    text=text+word[0]
                session['email']=email
                session['logged_in']=True
                return redirect(url_for('dashboard', user_name=result[0][2],initials=text),code=307)
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'),200,headers)

class UserRegister(Resource):
    
    def post(self):
      name = request.form['name']
      email = request.form['email']
      password = request.form['password']
      typee = request.form['type']
      emailt=''
      for i in email:
         if i == '@': 
            break
         else:
            emailt=emailt+i
      print(emailt) 

      cur = mysql.connection.cursor()
      temp="CREATE TABLE if not exists "+emailt+" (id int PRIMARY KEY AUTO_INCREMENT, email varchar(200),name varchar(200), password varchar(200),type varchar(200))"
      cur.execute(temp)
      flag="INSERT INTO "+emailt+" (email,name,password,type) VALUES(%s,%s,%s,%s)"
      cur.execute(flag,(email,name,password,typee))
      mysql.connection.commit()
      return redirect(url_for('userlogin')) 

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'),200,headers)


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj



class Dashboard(Resource):
    def __init__(self):
        pass
    def post(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index2.html',user_name=user_name,initials=initials),200,headers)

    
    def get(self):
        if session.get('logged_in') == True:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index2.html',user_name="",initials=""),200,headers)

           
        else:
            return redirect(url_for('userlogin')) 

class Classifier(Resource):
    def post(self):
        f = request.files['file-name']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join('uploads', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        reg_dic = extract(file_path) 

        if classify(reg_dic) == 1:
            senti_output = predict(reg_dic,True)
            print(senti_output)
            headers = {'Content-Type':'text/html'}
            # return make_response(render_template('sentimental.html',text_data=senti_output),200,headers)
            return redirect(url_for('sentimental',text_data=senti_output),code=307)
        elif classify(reg_dic) == 2:
            dic = dict()
            nlp = spacy.load('en')
            dic = transform(dic, nlp,reg_dic)
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
            # return make_response(render_template('resume.html',text_data=dic[0],skills=skills),200,headers)
            return redirect(url_for('resume',text_data=dic[0],skills=skills),code=307)
        else:
            output = 3
            headers = {'Content-Type':'text/html'}
            return make_response(render_template('classifier.html',text_data=output),200,headers)

    def get(self):
        headers = {'Content-Type':'text/html'}
        dic = dict()
        return make_response(render_template('classifier.html',data=dic,flag=0),200,headers)


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
        print(senti_output)
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

class Logout(Resource):
    def get(self):
      
        session.pop('logged_in', None)

class AppVoice(Resource):

    
   def post(self):
      data = request.get_json()
      s=data                               
      palak=s['data']
      email=s['email'] 
      emailj=''
      print(email)
      for i in email:
         if i == '@':
            break
         else:
            emailj=emailj+i
      emailt = "".join((str(emailj),"voice"))
      print(emailt)
   
      print("hrllo")
      print(palak)
      cur = mysql.connection.cursor()
      temp="CREATE TABLE if not exists "+emailt+" (voiceform varchar(2000))"
      cur.execute(temp)
      for i in palak:
         print(i)
         sql = "INSERT INTO "+emailt+" VALUES (%s)"
         cur.execute(sql,[i])
      mysql.connection.commit()
   
            
      return {"message": "voice done"}, 201


class AppRetrieveVoice(Resource):

    
   def post(self):
      data = request.get_json()
      email = data['email']
      emailj=''
      print(email)
      for i in email:
         if i == '@':
            break
         else:
            emailj=emailj+i
      emailt = "".join((str(emailj),"voice"))
      string = "SELECT * FROM "+emailt+""
      cur = mysql.connection.cursor()
      cur.execute(string)
      row = [item[0] for item in cur.fetchall()]
      #response = cur.fetchall()
      print(row)
      ans={'data':row}
      print(ans)
      return ans

class AppFormDetails(Resource):

    
   def post(self):
      data = request.get_json()
      print(data)
      #generate pdf @saif
      return {"message": "voice done"}, 201


#jwt = JWT(app, authenticate, identity)
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Dashboard, '/')
api.add_resource(Inbox, '/inbox')
api.add_resource(Classifier, '/classifier')
api.add_resource(Resume, '/resume')
api.add_resource(Sentimental, '/sentimental') #feedback
api.add_resource(Summarizer, '/summarizer')
api.add_resource(Inbox, '/logout')
api.add_resource(AppVoice, '/createvoicefields')
api.add_resource(AppRetrieveVoice, '/getvoicefields')
api.add_resource(AppFormDetails, '/getformdetails')


if __name__ == "__main__":
    app.run(debug=True,port=5000)
