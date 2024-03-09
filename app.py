from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

from admin.ResumeHandler import save_resume
SaveResumeToDatabaseInstance = save_resume.SaveResumeToDatabase

class Home(Resource):
    def get(self):
        return 'Welcome to, Test App API!'

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return "Data received", 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}
        

api.add_resource(Home,'/')
api.add_resource(SaveResumeToDatabaseInstance,'/admin/save_resume_to_database')

if __name__ == "__main__":
    port = int(5000)
    app.run(host='0.0.0.0', port=port) 