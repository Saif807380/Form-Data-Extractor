from rake_nltk import Rake
from ResumeAndFeedbackClassifier.mylists import feedback_list, resume_list, application_list
# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake()

# Extraction given the text.
a='''
SAIF KAZI
saif1204kazi@gmail.com
CE Undergrad, Graduating 2022
+91-8104679894
Mumbai
Data Science enthusiast having keen interest
in designing complete solutions.
linkedin.com/in/saif-k-647640132 in
github.com/Saif807380 (>
EDUCATION
SKILLS
B.Tech in Computer Engineering
Veermata Jijabai Technological Institute
C
C+ +
Python
Dart
Flutter
(VJTI)
Machine Learning
Deep Learning
07/2018 -Present
CPI - 9.0
Neural Networks
JavaScript
HTML
CSS
HSC
Bootstrap
Java
Shri T.P. Bhatia College of Science
06/2016-04/2018
Marks - 94.92%
ACHIEVEMENTS
PROJECTS
Smart India Hackathon (SIH)
Qualified among the top 10 teams of VITI SIH internal hackathon
Voice Prescription (01/2020)
and will be representing VITI in the upcoming SIH 2020.
- A flutter app for digitisation of the process of creating
prescription for the patients by the doctor.
MHT-CET Cell
Developed as a part of VJTI's SIH internal hackathon.
Secured 58th rank in the state with aggregate score of 183/200.
Movie Recommender App (09/2019 - 12/2019)
Managing Workshops
Successfully conducted and managed C language and Web
A Flutter app that recommends movies based on the users
Development Workshop as a member of the Community of
selected genres and liked movies.
Coders, VITI
An Application of recommender system.
Healthify (10/2019)
ORGANIZATIONS
An app that helps identify diseases based on the symptoms,
ind out diseases that are widespread in any given area,
calculate BMI and dish out diet advice based on it.
Community of Coders, VJTI (06/2019 - Present)
Developed as a part of KJHACK 2019
Active Member
VJTI APP (05/2019 - 08/2019)
The VJTI-APP is an application designed for the purpose of
CERTIFICATIONS
easy notes sharing between the students and the teacher.
The application also features an events section and a map
Neural Networks and Deep Learning
section.
Developed under COC, VJTI's summer project internship
programme.
Improving Deep Neural Networks C
Structuring Machine Learning Projects C
Convolutional Neural Networks C
'''
def classify(a):
    r.extract_keywords_from_text(a)

    l = r.get_ranked_phrases()
    l=str(l)
    s1=0
    for i in feedback_list:
        if i in l:
            s1+=1
    s2=0
    for i in resume_list:
        if i in l:
            s2+=1
    s3=0
    for i in application_list:
        if i in l:
            s3+=1
    if s1>s2 and s1>s3:
        print("feedback form")
        return 1
    elif s2>s3 and s2>s1:
        print("resume")
        return 2
    else:
        print("application form")
        return 3

# To get keyword phrases ranked highest to lowest with scores.
#r.get_ranked_phrases_with_scores()