# Form-Extractor

A Flask WebApp for extracting text from images and performing relevant analysis. Ananlysis includes skills extraction from resumes, sentimental analysis of feedback forms and extractive text summarisation of large texts.

## Directory Structure
```bash
.
├── ResumeAndFeedbackClassifier
│   ├── mylists.py
│   └── test.py
├── ResumeParser
│   ├── config.yaml
│   ├── field_extraction.py
│   ├── generate_top_skills.py
│   ├── lib.py
│   └── main.py
├── templates
│   ├── classifier.html
│   ├── index2.html
│   ├── login.html
│   ├── pdf_template.html
│   ├── register.html
│   ├── resume.html
│   ├── sentimental.html
│   └── summarizer.html
├── static
├── VoiceForm.py
├── cloudmersive_api.py
├── cloudmersive_extract.py
├── main.py
├── requirements.txt
├── text_summariser.py
├── top_skills.csv
└── top_titles.csv
```






## Setup
* Clone the repository
```bash
$ git clone https://github.com/Saif807380/Form-Extractor
```
* Create a virtual environment and install requirements.txt
```bash
$ virtual environment VIRTUAL_ENV_NAME

$ pip install -r requirements.txt
```
* Download the `model.h5` and `tokenizer.pkl` files from [here](https://drive.google.com/open?id=1yGvxBxezg145-QzZVb5LSy6KjHVnWRjI) and put the files in the root directory of the project.

* Set your API KEY in `cloudmersive_api.py`

* Set up your MySQL localhost and password

* Run `main.py`
```bash
$ python main.py
```
## Individual Modules
* [App](https://github.com/Saif807380/Form-Extractor-App)
* [Text Summarizer](https://github.com/Saif807380/Text-Summariser)
* [Resume Parser](https://github.com/Saif807380/Resume-Parser)

