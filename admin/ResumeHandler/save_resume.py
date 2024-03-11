from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import requests

from scripts.job_scraper import scrape_job_data


class SaveResumeToDatabase(Resource):
    def parse_resume_text(self, resume_text):
        keywords = []
        # pass resume_data through ml model to get keywords here
        return keywords

    def handle_user_data(self, name, resume_text, keywords):
        try:
            # make an api call here to nodejs backend to create user document in mongodb collection
            data = {
                'name': name,
                'resumeText': resume_text
            }
            response = requests.post(
                "http://localhost:8080/addUser", json=data)
            # print(response.json())
            if response.status_code == 200:
                return {"data": "User data saved to database.", "user_id": response.json()}
        except Exception as error:
            return {'error': error}

    def get_jobs_from_internet(self, keywords):
        try:
            # dummy_job = {
            # "job_id":99141411321,
            # "job_portal":'internshala',
            # "job_link":'url',
            # "job_description":'jdakopskjdks',
            # "job_keywords_ordered":['ruby','js'],
            # "job_posted":'date'
            # }
            # hard-coded keywords
            keywords = ['javascript', 'python']

            # First check if the jobs are available in the database or not , if not then only scrape the internet

            scraped_job_results = scrape_job_data(keywords)
            return scraped_job_results
            # call the nodejs api to store the jobs data in the database
            for job in scraped_job_results:
                try:
                    data = {
                        'job_id': job['id'],
                        'job_title': job['title'],
                        'job_link': job['job_link'],
                        'job_company': job['company'],
                        'job_location': job['location']
                    }
                    # response = requests.post(
                    #     "http://localhost:8080/addJobs", json=data)
                except Exception as error:
                    return {"error": error}
            return scraped_job_results

        except Exception as error:
            return {'error': error}

    def post(self):
        try:
            value = request.get_json()
            name = value['name']
            # last_name=value['last_name'];
            resume_text = value['resume_text']
            if (value):
                keywords = self.parse_resume_text(resume_text)
                response = self.handle_user_data(name, resume_text, keywords)
                if (response):
                    result = self.get_jobs_from_internet(keywords)
                    return [result, {"message": "Job search successful."}], 201
                else:
                    return {"error": "Something went wrong."}

            return {"error": "Something went wrong."}

        except Exception as error:
            return {'error': error}
