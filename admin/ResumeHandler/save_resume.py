from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import pickle
import spacy

from scripts.job_scraper import scrape_job_data
from utils.model_support import skill_finder,get_semantically_related_keywords
from utils import text_cleaner

import pathlib
pathlib.PosixPath = pathlib.WindowsPath

def fetch_model():
    try:
        pkl_filename = 'D:\dev\python\RASER-Parser-v2\spacy_ner_model.pkl'
        with open(pkl_filename,'rb') as file:
            model=pickle.load(file)
            
        return model
    except Exception as error:
        print(f'Error: {error}')
        return error
    
class SaveResumeToDatabase(Resource):
    def handle_user_data(self, name, resume_text, keywords,semantic_keywords):
        try:
            # make an api call here to nodejs backend to create user document in mongodb collection
            data = {
                'name': name,
                'resumeText': resume_text,
                'cleanResumeText': text_cleaner.cleanText(resume_text),
                'resumeKeywords': keywords,
                "semanticKeywords":semantic_keywords
            }
            response = requests.post(
                "http://localhost:8080/addUser", json=data)
            # print(response.json())
            if response.status_code == 200:
                return {"data": "User data saved to database.", "user_id": response.json()}
        except Exception as error:
            return {'error': error}
    
    def get_jobs_from_internet(self,model, keywords):
        try:
            # First check if the jobs are available in the database or not , if not then only scrape the internet
            scraped_job_results = scrape_job_data(model,keywords)
            print('Jobs scraped!')
            # data = {
            #     'resume_keywords': keywords
            # }
            # response = requests.post(
            #     "http://localhost:8080/jobs", json=data)
            # if len(response.json()['Jobs']) > 0:
            #     return response.json()
            
            # call the nodejs api to store the jobs data in the database
            for job in scraped_job_results:
                try:
                    data = {
                        'job_id': job['id'],
                        'job_title': job['title'],
                        'job_link': job['job_link'],
                        'job_company': job['company'],
                        'job_location': job['location'],
                        'job_keywords' : job['keywords']
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
            if (value):
                model = fetch_model()
                keywords = skill_finder(model,resume_text)
                print(keywords)
                semantic_keywords = get_semantically_related_keywords(keywords)
                print(semantic_keywords)
                response = self.handle_user_data(name, resume_text, keywords ,semantic_keywords)
                if (response):
                    keywords = keywords + semantic_keywords
                    result = self.get_jobs_from_internet(model,keywords)
                    return [result, {"message": "Job search successful."}], 201
                else:
                    return {"error": "Something went wrong."}
                # return {"keywords":keywords,"semantic_keywords":semantic_keywords}, 201
            
            return {"error": "Something went wrong."}

        except Exception as error:
            return {'error': error}
