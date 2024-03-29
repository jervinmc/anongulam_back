from flask import Response
from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api
from flask_cors import CORS
from datetime import datetime
import smtplib
from Database import Database
import boto3
import jwt
import os
import schedule
import time
import string
import random
from decouple import config
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
now = datetime.now().date()
print("nice")

from apscheduler.schedulers.background import BackgroundScheduler
# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))



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
            self.db.insert(f"INSERT INTO users(email,password) values('{data.get('email')}','{data.get('password')}','{data.get('fullname')}')")
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
            if(data.get('category')=='keto'):
                self.db.insert(f"UPDATE users set health_condition='{data.get('health_condition')}',isany='no',isketo='yes',isvegetarian='no',isnopork='no',ispaleo='no',ispescatarian='no',email='{data.get('email')}',fullname='{data.get('fullname')}' where id={pk}")
            if(data.get('category')=='any'):
                self.db.insert(f"UPDATE users set health_condition='{data.get('health_condition')}',isany='yes',isketo='no',isvegetarian='no',isnopork='no',ispaleo='no',ispescatarian='no',email='{data.get('email')}',fullname='{data.get('fullname')}' where id={pk}")
            if(data.get('category')=='paleo'):
                self.db.insert(f"UPDATE users set health_condition='{data.get('health_condition')}',isany='no',isketo='no',isvegetarian='no',ispaleo='yes',isnopork='no',ispescatarian='no',email='{data.get('email')}',fullname='{data.get('fullname')}' where id={pk}")
            if(data.get('category')=='vegetarian'):
                self.db.insert(f"UPDATE users set health_condition='{data.get('health_condition')}',isany='no',isketo='no',isvegetarian='yes',isnopork='no',ispaleo='no',ispescatarian='no',email='{data.get('email')}',fullname='{data.get('fullname')}' where id={pk}")
            if(data.get('category')=='pescatarian'):
                self.db.insert(f"UPDATE users set health_condition='{data.get('health_condition')}',isany='no',isketo='no',isvegetarian='no',ispaleo='no',ispescatarian='yes',email='{data.get('email')}',fullname='{data.get('fullname')}' where id={pk}")
            if(data.get('category')=='no pork'):
                self.db.insert(f"UPDATE users set health_condition='{data.get('health_condition')}',isany='no',isketo='no',isvegetarian='no',ispaleo='no',isnopork='yes',ispescatarian='no',email='{data.get('email')}',fullname='{data.get('fullname')}' where id={pk}")
            diettype = data.get('category')
            self.db.insert(f"delete from weekly_meals where user_id={pk}")
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
            setWeeklyMeals(pk,diettype,'breakfast')
            setWeeklyMeals(pk,diettype,'lunch')
            setWeeklyMeals(pk,diettype,'dinner')
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
                return {"id":res[0][0],"email":res[0][1],"email":res[0][1],"password":res[0][2],"isketo":res[0][4],"allergy":res[0][9],"ispescatarian":res[0][7],"ispaleo":res[0][6],"isvegetarian":res[0][5],"password":res[0][2],"fullname":res[0][10],"health_condition":res[0][8],"isnopork":res[0][11],"status":201}
            
        except Exception as e:
            print(e)
            return {"status":"Failed Input"}



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
            res = self.db.insert(f"""INSERT INTO users values(default,'{data.get('email')}','{data.get('password')}','{data.get('isany')}','{data.get('isketo')}','{data.get('isvegetarian')}','{data.get('ispaleo')}','{data.get('ispescatarian')}','{data.get('health_condition')}','{str(data.get('allergy')).replace('[','').replace(']','').replace("'",'')}','{data.get('fullname')}','{data.get('isnopork')}')""")
            id = self.db.query("select max(id) from users""")
            if(id[0][0]==None):
                id=0
            else:
                id=id[0][0]
            diettype=''
            if(data.get('isketo')=='yes'):
                diettype='keto'
            if(data.get('isvegetarian')=='yes'):
                diettype='vegetarian'
            if(data.get('ispaleo')=='yes'):
                diettype='paleo'
            if(data.get('ispescatarian')=='yes'):
                diettype='pescatarian'
            if(data.get('isnopork')=='yes'):
                diettype='no pork'
            if(data.get('isany')=='yes'):
                diettype='any'
            categorizedItem = self.db.query(f"select * from menu_list where diettype='{diettype}'  order by random() limit 6")
            print(categorizedItem)
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            setWeeklyMeals(id,diettype,'breakfast')
            setWeeklyMeals(id,diettype,'lunch')
            setWeeklyMeals(id,diettype,'dinner')
            return Response({"status":"Success"},status=201)
            
        except Exception as e:
            print(e)
            return {"status":"Failed Input"}

def setWeeklyMealsAll():
    db=Database()
    db.insert(f"delete from weekly_meals")
    data_users = db.query(f"select * from users")
    for i in data_users:
        data_fetch = db.query(f"select * from menu_list where diettype='keto'  order by random() limit 1")
        print(i[0])
        for x in data_fetch:
            # print(x)
            db.insert(f"INSERT INTO weekly_meals values(default,{x[0]},{i[0]})")
    pass

def setWeeklyMeals(id,diettype,categorytime):
    db=Database()
    data_fetch = db.query(f"select * from menu_list where diettype='{diettype}' and categorytime='{categorytime}'  order by random() limit 1")
   
    for x in data_fetch:
        print(x)
        db.insert(f"INSERT INTO weekly_meals values(default,{x[0]},{id})")
    pass



# scheduler = BackgroundScheduler()
# scheduler.add_job(func=setWeeklyMealsAll, trigger="interval", seconds=30)
# scheduler.start()

class UserMeals(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,diettype=None,user_id=None):
        data_fetch = self.db.query(f"SELECT * FROM menu_list where user_id={user_id}")
        return data_fetch


class MenuList(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,diettype=None,categorytime=None,allergy=None):
        print(allergy)
        if(allergy!=''):
            data_fetch = self.db.query(f"SELECT * FROM menu_list where categorytime='{categorytime}' and diettype='{diettype}' and foodtype!='{allergy}'")
            print(data_fetch)
        else:
            data_fetch = self.db.query(f"SELECT * FROM menu_list where categorytime='{categorytime}' and diettype='{diettype}' ")
            print(data_fetch)
        return data_fetch
        
    def post(self,pk=None,categorytime='',diettype='',allergy=None):
        data = request.get_json()
        id = self.db.query("select max(id)+1 from menu_list")
        print(id)
        if(id[0][0]==None):
            id=0
        else:
            id=id[0][0]
        try:
            res = self.db.insert(f"INSERT INTO menu_list values(default,'{data.get('name')}','{data.get('image')}','{data.get('categorytime')}','{data.get('diettype')}','{data.get('foodtype')}',{data.get('user_id')},'{data.get('calories')}')")
            print(res)
            id = self.db.query("select max(id) from menu_list")
            if(id[0][0]==None):
                id=0
            else:
                id=id[0][0]
            for x in data.get('recipe'):
                print(x)
                self.db.insert(f"INSERT INTO recipe values(default,{id},'{x}')")
            counter = 0
            print(data)
            for x in data.get('ingredients'):
                self.db.insert(f"INSERT INTO ingredients values(default,{id},'{x}',{data.get('quantity')[counter]},'{data.get('sizelabel')[counter]}')")
                counter= +1

            return {"data":id}
            
            # if(res==[]):  
            #     print(res)
            #     return Response({"status":"Wrong Credentials"},status=404)
            # else:
            #     result_data = self.db.query(f"SELECT SUM(total) FROM receipt where user_id = '{data.get('id')}'")
            #     result_settings = self.db.query(f"SELECT totalAmount from users where id = {data.get('id')}")
            #     id = self.db.query(f"select max(id) from receipt")
            #     if(int(result_data[0][0])>=(result_settings[0][0])):     
            #         print(result_settings[0][0])``
            #         return {"status":"exceed","id":id[0][0]}
            #     else:
            #         return {"status":"less","id":id[0][0]}
        
        except Exception as e:
            print(e)
            return {"status":f"{e}"}


class Ingredients(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,menu_id=None):
        data_fetch = self.db.query(f"SELECT * FROM ingredients where menu_id='{menu_id}'")
        return data_fetch
    def post(self,menu_id):
        data = request.get_json()
        for x in data.get('ingredients'):
                print(x)
                self.db.insert(f"INSERT INTO ingredients values(default,{data.get('menu_id')},'{x}',1)")
        for x in data.get('recipes'):
                print(x)
                self.db.insert(f"INSERT INTO recipe values(default,{data.get('menu_id')},'{x}')")
        return ""
class Pantry(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,user_id=None):
        data_fetch = self.db.query(f"SELECT * FROM pantry where user_id='{user_id}'")
        return data_fetch

    def post(self,user_id=None):
        res = request.get_json()
        data_fetch = self.db.insert(f"INSERT INTO pantry values(default,'{res.get('name')}',{res.get('user_id')},{res.get('quantity')})")
        return

class Likes(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,menu_id=None):
        res = request.get_json()
        data_fetch = self.db.insert(f"INSERT INTO likes values(default,'{res.get('menu_id')}',{res.get('user_id')})")
        return
    
    def put(self,menu_id=None):
        res = request.get_json()
        print(res)
        s = self.db.query(f"select * from likes where menu_id={res.get('menu_id')} and user_id={res.get('user_id')}")
        print(len(s))
        if(len(s)>0):
            return True
        else:
            return False
        # data_fetch = self.db.insert(f"INSERT INTO likes values(default,'{res.get('menu_id')}',{res.get('user_id')})")
        return

class Weekly(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,user_id=None):
        try:
            listitems = []
            # print(user_id)
            data_fetch = self.db.query(f"SELECT * FROM weekly_meals where user_id={user_id}")
            for x in data_fetch:
                # print(x[1])
                data_meals = self.db.query(f"SELECT * FROM menu_list where id={x[1]}")
                if(len(data_meals)!=0):
                    print(data_meals[0])
                    listitems.append(data_meals[0])
            return listitems
        except Exception as e:
            print(e)
            return {"data":""}

class GroceryPantry(Resource):
    def __init__(self):
        self.db=Database()

    def post(self):
        res = request.get_json()
        for x in res['listitem']:
            data = self.db.query(f"select * from pantry where name='{x['name']}' and user_id={res['user_id']}")
            if(len(data)==0 and x['quantity']!=None):
                data_fetch = self.db.insert(f"INSERT INTO pantry values(default,'{x['name']}',{res['user_id']},{x['quantity']})")
            else:
                data_fetch = self.db.insert(f"UPDATE pantry set quantity=quantity+1 where user_id={res['user_id']} and name='{x['name']}'" )
        return "okay"

class Groceries(Resource):
    def __init__(self):
        self.db=Database()
    def get(self,user_id=None):
        print("yesss")
        pantry_list = self.db.query(f"SELECT * FROM pantry where user_id={user_id}")
        weekly_list = self.db.query(f"SELECT * FROM weekly_meals where user_id={user_id}")
        ingredients_list = []
        grocery_list=[]
        list_weekly = []
        menu_list = []
        for x in weekly_list:
            menu_list.append(str(x[1]))
        #for error handling
        if(menu_list==[]):
            print("ye")
            return []
        data_ingredients = self.db.query(f"select ingredients_name, sum(quantity) from ingredients where menu_id in ({', '.join(menu_list)}) group by ingredients_name;")
        # for x in weekly_list:
        #     data_ingredients = self.db.query(f"SELECT * FROM ingredients where menu_id={x[1]}")
        #     for i in data_ingredients:
        #         if(len(i)!=0):
        #             ingredients_list.append(i[2])
        # pantry_list = [['2 cups of chilled white rice', 1], ['5 pieces of longanisa\n', 1], ['salt', 1], ['1 cup of water for cooking longanisa', 1], ['2-3 eggs, cooked sunny side up\n', 1], ['oil', 1], ['1 tablespoon cooking oil\n', 1], ['1⁄2 teaspoon of salt', 1], ['ingredients test', 1], ['egg', 1]]
        data_ingredients = convertToList(data_ingredients)
        # for i in convertToList(data_ingredients):
        #     print(i)
        # print(data_ingredients)
        for (x,y) in enumerate(data_ingredients):
            for (i,j) in enumerate(pantry_list):
                if(y[0]==j[1]):
                    # print(j[0])
                    if(y[1]-j[3]<=0):
                        # data_ingredients.remove()
                        data_ingredients[x]=None
                        pantry_list.remove(j)
                        # pantry_list.remove(j)
                    else:
                        data_ingredients[x][1]=y[1]-j[3]
                    isAdd = False
        # data_ingredients.append(['egg',1])
        print(list(filter(None,data_ingredients)))
        
        return list(filter(None,data_ingredients))


def convertToList(list_data):
    listitem = []
    for x in list_data:
         listitem.append(list(x))
    return listitem





class Meal(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,menu_id=None):
        listitem = {"menu_id":menu_id,"ingredients":[],"recipes":[]}
        ingredients_list = self.db.query(f"SELECT * FROM ingredients where menu_id={menu_id}")
        recipe_list = self.db.query(f"SELECT * FROM recipe where menu_id={menu_id}")
        for x in ingredients_list:
            listitem['ingredients'].append(x[2])
        for x in recipe_list:
            print("okayyy")
            listitem['recipes'].append(x[2])
        return listitem

    def put(self,menu_id=None):
        data = request.get_json()
        self.db.insert(f"DELETE from menu_list where id={data.get('id')}")
        return ''

    def post(self,menu_id=None):
        data = request.get_json()
        # id = self.db.query("select max(id)+1 from menu_list")
        # print(id)
        # if(id[0][0]==None):
        #     id=0
        # else:
        #     id=id[0][0]
        try:
            # res = self.db.insert(f"INSERT INTO menu_list values(default,'{data.get('name')}','{data.get('image')}','{data.get('categorytime')}','{data.get('diettype')}','{data.get('foodtype')}',{data.get('user_id')})")
            # print(res)
            # id = self.db.query("select max(id) from menu_list")
            # if(id[0][0]==None):
            #     id=0
            # else:
            #     id=id[0][0]
            self.db.insert(f"update menu_list set categorytime='{data.get('categorytime')}',diettype='{data.get('diettype')}' where id={data.get('id')}")
            self.db.insert(f"DELETE from ingredients where menu_id={data.get('id')}")
            self.db.insert(f"DELETE from recipe where menu_id={data.get('id')}")
            for x in data.get('recipe'):
                print(x)
                self.db.insert(f"INSERT INTO recipe values(default,{data.get('id')},'{x}')")
            for x in data.get('ingredients'):
                print(x)
                self.db.insert(f"INSERT INTO ingredients values(default,{data.get('id')},'{x}',1)")
            return ""
        except:
            return {""}

class Recipe(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,menu_id=None):
        data_fetch = self.db.query(f"SELECT * FROM recipe where menu_id={menu_id}")
        return data_fetch

    def post(self,user_id=None):
        res = request.get_json()
        data_fetch = self.db.insert(f"INSERT INTO recipe values(default,'{res.get('name')}',{res.get('user_id')},1)")
        return


class Recommend(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,user_id=None,diettype=None):
        list_id = []
        listitems=[]
        data_results=[]
        data_fetch = self.db.query(f"SELECT * FROM likes where user_id={user_id}")
        
        # list_id.append(data_fetch[0][1])
        # for x in data_fetch:
        #     x = self.db.query(f"SELECT * FROM ingredients where menu_id={x[1]}")
        #     if(len(x)!=0):  
        #         data_results.append(x[0])
        for x in data_fetch:
            y = self.db.query(f"SELECT * FROM ingredients where menu_id={x[1]}")
            for i in y:
                data_results.append(i)
        listitems=[]
        # print(data_results)
        ingredients_list_data=[]
        for x in data_results:
            ingredients_list_data.append(f"'{x[2]}'")
        if(len(ingredients_list_data)!=0):
            print(', '.join(ingredients_list_data))
            data_ingredients = self.db.query(f"SELECT menu_id FROM ingredients where ingredients_name in ({', '.join(ingredients_list_data)}) group by menu_id;")
            menu_list=[]
            for i in data_ingredients:
                menu_list.append(str(i[0]))
            listitems = self.db.query(f"SELECT * FROM menu_list where id in ({', '.join(menu_list)}) and diettype='{diettype}' ")
            print(listitems)
        # print(menu_list)
        # for x in data_results:
        #     get_same = self.db.query(f"SELECT * FROM ingredients where ingredients_name LIKE '%{x[2]}%'  ")
        #     print(x[2])
        #     if(len(get_same)!=0):
        #         if(get_same[0][1] in list_id):
        #             pass
        #         else:
        #             list_id.append(get_same[0][1])
        #         pass
        # # print(list_id)
        # for x in list_id:
        #     l = self.db.query(f"SELECT * FROM menu_list where id={x}")
        #     listitems.append(l[0])
        #     get_same = self.db.query(f"SELECT * FROM recipe where ")
        # print(tuple(list_id[1]))
        # print(listitems)
        return listitems
        
    

class Upload(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        print(pk)
        imageFile=request.files['image']
        print(imageFile.filename)
        file_path=os.path.join('', imageFile.filename) # path where file can be saved
        imageFile.save(file_path)
        client = boto3.client('s3',aws_access_key_id=config("AWS_ACCESS_ID"),aws_secret_access_key=config("AWS_SECRET_ID"))
        client.upload_file(f'{imageFile.filename}','chatmind',f'{imageFile.filename}')
        self.db.insert(f"UPDATE menu_list set image='https://chatmind.s3.ap-southeast-1.amazonaws.com/uploads/{imageFile.filename}' where id={pk} ")
        return {"status":"Successful"}

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ResetPassword(Resource):
    def __init__(self):
        self.db=Database()
        
    def post(self):
        res = request.get_json()
        pw = id_generator()
        print(res)
        isValid = self.db.query(f"select * from users where email='{res.get('email')}' ")
        if(len(isValid) > 0):
            self.db.insert(f"UPDATE users set password='{pw}' where email='{res.get('email')}' ")
            msg = MIMEMultipart()
            msg.add_header('Content-Type', 'text/html')
            msg['To'] = str(res.get('email'))
            msg['Subject'] = "Reset password from Anongulam app"
            part1=MIMEText("""\
                <html>
                    <body>
                        Here's your new password : """+pw+"""
                    </body>
                </html>
                
                """,'html')

            msg.attach(part1)
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login('somersalt69@gmail.com', "Stayalive4me")
            # send the message via the server.
            server.sendmail('somersalt69@gmail.com', msg['To'], msg.as_string())
            server.quit()
            print("successfully sent email to %s:" % (msg['To']))
            return {"status":"success"}
        else:
            print("invalid")
            return {"status":"invalid"}

# api.add_resource(Verification,'/api/v1/verify/<string: token>')
api.add_resource(Upload,'/api/v1/upload/<int:pk>')
api.add_resource(Register,'/api/v1/register')   
api.add_resource(Usermanagement,'/api/v1/users/<int:pk>')
api.add_resource(Login,'/api/v1/login')
api.add_resource(MenuList,'/api/v1/menu_list/<string:categorytime>/<string:diettype>/<string:allergy>')
api.add_resource(Pantry,'/api/v1/pantry/<int:user_id>')
api.add_resource(Recipe,'/api/v1/recipe/<int:menu_id>')
api.add_resource(Ingredients,'/api/v1/ingredients/<int:menu_id>')
api.add_resource(Recommend,'/api/v1/recommend/<int:user_id>/<string:diettype>')
api.add_resource(Weekly,'/api/v1/weekly/<int:user_id>')
api.add_resource(Likes,'/api/v1/likes/<int:menu_id>')
api.add_resource(UserMeals,'/api/v1/user_meals/<int:user_id>')
api.add_resource(Meal,'/api/v1/meals/<int:menu_id>')
api.add_resource(Groceries,'/api/v1/groceries/<int:user_id>')
api.add_resource(GroceryPantry,'/api/v1/grocerypantry')
api.add_resource(ResetPassword,'/api/v1/reset_password')
# api.add_resource(UploadTest,'/api/v1/uploadtest')
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port="5000")
    # app.run(debug=True,host='localhost',port="5001")
