# from admin.ResumeHandler import save_resume
from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import pickle
import spacy

from scripts.job_scraper import scrape_job_data
from utils.model_support import skill_finder, get_semantically_related_keywords
from utils import text_cleaner


import pathlib
pathlib.PosixPath = pathlib.WindowsPath


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)


# SaveResumeToDatabaseInstance = save_resume.SaveResumeToDatabase


class Home(Resource):
    def get(self):
        return 'Welcome to, Test App API!'

    def post(self):
        try:
            value = request.get_json()
            if (value):
                return "Data received", 201

            return {"error": "Invalid format."}

        except Exception as error:
            return {'error': error}


requestSid = None


@socketio.on('update')
def handle_connect():
    global requestSid
    requestSid = request.sid
    print('Client connected', requestSid)
    socketio.emit('status_update', {
                  'message': 'Backend is processing...'}, to=requestSid)


def fetch_model():
    try:
        pkl_filename = 'D:\models\spacy_ner_model.pkl'
        with open(pkl_filename, 'rb') as file:
            model = pickle.load(file)

        return model
    except Exception as error:
        print(f'Error: {error}')
        return error


class SaveResumeToDatabase(Resource):
    def handle_user_data(self, name, resume_text, keywords, semantic_keywords):
        try:
            # make an api call here to nodejs backend to create user document in mongodb collection
            data = {
                'name': name,
                'resumeText': resume_text,
                'cleanResumeText': text_cleaner.cleanText(resume_text),
                'resumeKeywords': keywords,
                "semanticKeywords": semantic_keywords
            }
            response = requests.post(
                "http://localhost:8080/addUser", json=data)
            # print(response.json())
            if response.status_code == 200:
                return {"data": "User data saved to database.", "user_id": response.json()}
        except Exception as error:
            return {'error': error}

    def get_jobs_from_internet(self, model, keywords, isCronJob):
        try:
            # First check if the jobs are available in the database or not , if not then only scrape the internet
            data = {
                'resume_keywords': keywords
            }
            if isCronJob == False:
                response = requests.post(
                    "http://localhost:8080/jobs", json=data)
                if len(response.json()['Jobs']) > 0:
                    return response.json()

            scraped_job_results = scrape_job_data(model, keywords)
            print('Jobs scraped!')
            # call the nodejs api to store the jobs data in the database
            for job in scraped_job_results:
                try:
                    data = {
                        'job_id': job['id'],
                        'job_title': job['title'],
                        'job_link': job['job_link'],
                        'job_company': job['company'],
                        'job_location': job['location'],
                        'job_keywords': job['keywords']
                    }
                    response = requests.post(
                        "http://localhost:8080/addJobs", json=data)
                    if response.status_code != 200:
                        print("Message", response.json())

                except Exception as error:
                    return {"error": error}
            return scraped_job_results

        except Exception as error:
            return {'error': error}

    def post(self):
        try:
            value = request.get_json()
            name = value['name']
            resume_text = value['resume_text']
            socketio.emit('status_update', {
                'message': 'Name and resume text fetched successfully'}, to=requestSid)
            if (value):
                model = fetch_model()
                keywords = skill_finder(model, resume_text)
                print(keywords)
                socketio.emit('status_update', {
                    'message': 'Resume Keywords Extracted'}, to=requestSid)
                semantic_keywords = get_semantically_related_keywords(keywords)
                print(semantic_keywords)
                response = self.handle_user_data(
                    name, resume_text, keywords, semantic_keywords)
                socketio.emit('status_update', {
                    'message': 'User data saved to database'}, to=requestSid)
                if (response):
                    keywords = keywords + semantic_keywords
                    socketio.emit('status_update', {
                        'message': 'Getting best jobs across internet for you'}, to=requestSid)
                    result = self.get_jobs_from_internet(
                        model, keywords, False)
                    return result, 201
                else:
                    return {"error": "Something went wrong."}
                # return {"keywords":keywords,"semantic_keywords":semantic_keywords}, 201

            return {"error": "Something went wrong."}

        except Exception as error:
            return {'error': error}


class CronJob(Resource):
    def get(self):
        try:
            response = requests.get("http://localhost:8080/keywords")
            if response.status_code == 200:
                model = fetch_model()
                result = self.get_jobs_from_internet(
                    model, response.json()['keywords'])
                return result, 201
        except Exception as error:
            return {'error': error}


api.add_resource(Home, '/')
api.add_resource(SaveResumeToDatabase,
                 '/admin/save_resume_to_database')
api.add_resource(CronJob, '/admin/cron')

if __name__ == "__main__":
    # port = int(5000)
    # app.run(host='0.0.0.0', port=port)
    socketio.run(app, debug=False)
