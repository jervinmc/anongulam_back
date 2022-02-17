from flask import Response
from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api
from flask_cors import CORS
from datetime import datetime
from Database import Database
import boto3
import jwt
import os
from decouple import config
now = datetime.now().date()
app=Flask(__name__)
CORS(app)
api=Api(app)

def verificationToken(token):
    try:
        object = jwt.decode(token, "secret", algorithms=["HS256"])
        print(object)

        return True
    except:
        return False
    

class Usermanagement(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        data = request.get_json()
        try:
            self.db.insert(f"INSERT INTO users(email,password) values('{data.get('email')}','{data.get('password')}')")
            return {"status":"success"}
        except Exception as e:
            print(e)
            return {"status":"Failed Input"}

    def get(self,pk=None):
        if pk==None:
            res = self.db.query('SELECT * FROM users')
        else:
            res = self.db.query(f'SELECT * FROM users where id={pk}')
        return {"data":res}

    def delete(self,pk):
        try:
            self.db.insert(f'DELETE FROM users where id={pk}')
            return {"data":"success"}
        except:
            return {"status":"Failed"}

    def get(self,pk=None):
        if pk==None:
            res = self.db.query('SELECT * FROM users')
        else:
            res = self.db.query(f'SELECT * FROM users where id={pk}')
        return {"data":res}

    def delete(self,pk):
        try:
            self.db.insert(f'DELETE FROM users where id={pk}')
            return {"data":"success"}
        except:
            return {"status":"Failed"}
    
    def put(self,pk):
        data = request.get_json()
        try:
            self.db.insert(f"UPDATE users set email='{data.get('email')}',password='{data.get('password')}' where id={pk}")
            return {"status":"Success"}
        except Exception as e:
            return {"status":"Failed"}

class Login(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        data = request.get_json()
        print(data)
        try:
            res = self.db.query(f"SELECT * FROM users where email='{data.get('email')}' and password='{data.get('password')}'")
            if(res==[]):
                print(res)
                return {"status":400}
            else:
                print(res[0][0])
                return {"id":res[0][0],"email":res[0][1],"password":res[0][2],"status":201}
            
        except Exception as e:
            print(e)
            return {"status":"Failed Input"}

class UploadTest(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        file = request.files['file']
        file_path=os.path.join('', file.filename) # path where file can be saved
        file.save(file_path)
        client = boto3.client('s3',aws_access_key_id=config("AWS_ACCESS_ID"),aws_secret_access_key=config("AWS_SECRET_ID"))
        client.upload_file(f'{file.filename}','acnes012022',f'{file.filename}')
        return {"filename":f"https://acnes012022.s3.us-east-2.amazonaws.com/{file.filename}"}


class Register(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        data = request.get_json()
        print(data)
        data_fetch = self.db.query(f"select * from users where email='{data.get('email')}'")
        
        if(len(data_fetch)>0):
            return {"status":"Failed Input"}
        try:
            id = self.db.query("select max(id)+1 from users")
            res = self.db.insert(f"INSERT INTO users values(default,'{data.get('email')}','{data.get('password')}','{data.get('isany')}','{data.get('isketo')}','{data.get('isvegetarian')}','{data.get('ispaleo')}','{data.get('ispescatarian')}')")
            return Response({"status":"Success"},status=201)
            
        except Exception as e:
            print(e)
            return {"status":"Failed Input"}



# api.add_resource(Verification,'/api/v1/verify/<string:token>')
api.add_resource(Register,'/api/v1/register')
api.add_resource(Usermanagement,'/api/v1/users/<int:pk>')
api.add_resource(Login,'/api/v1/login')
# api.add_resource(UploadTest,'/api/v1/uploadtest')
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port="5001")