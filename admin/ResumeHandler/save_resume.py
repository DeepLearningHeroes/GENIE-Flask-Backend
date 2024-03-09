from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS

class SaveResumeToDatabase(Resource):
    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}
        
