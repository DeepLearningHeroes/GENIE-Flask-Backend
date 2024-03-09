from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS

class SaveResumeToDatabase(Resource):
    def parse_resume_text(self,resume_text):
        keywords = []
        # pass resume_data through ml model to get keywords here
        return keywords
    
    def handle_user_data(self,first_name,last_name,resume_text,keywords):
        try:
            # make an api call here to create user document in mongodb collection
            return {"data":"User data saved to database.","user_id":"user's id from the database"}
        except Exception as error:
            return {'error':error}

    def post(self):
        try:
            value = request.get_json()
            first_name=value['first_name'];
            last_name=value['last_name'];
            resume_text=value['resume_text'];   
            if(value):
                keywords = self.parse_resume_text(resume_text)
                response = self.handle_user_data(first_name,last_name,resume_text,keywords)
                # once this response is sent back to the user, the frontend must make another call to use these keywords to find jobs over the internet 
                return response, 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}
        
