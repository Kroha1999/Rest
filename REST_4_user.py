from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

applications = [

]

plans =[

]


#Wellcome pages----------------------------------------------------------------
@app.route("/",methods=["GET"])
def wellcome():
    return "Вітаємо в системі житлово-комунального підприємства!\n\n"+"Щоб увійти як користувач скористайтесь тегом '\\user'\n"+"Для перегляду заявок скористайтесь тегом '\\applications'\n"+"Для перегляду планів робіт скористайтесь тегом '\\plans'"

@app.route("/user",methods=["GET"])
def user():
    return "Вітаємо в системі житлово-комунального підприємства!\n\n"+"Для написання заявки скористайтесь тегом POST '\\user\\write'\n"+"1. У заявці потрібно вказати імя (параметр 'name')\n"+"2. Вид робіт('type')\n3. Масштаб робіт ('value')\n"+"4.Час робіт('time)'\n\n"+"Для перегляду заявок скористайтесь тегом '\\applications'\n"+"Для перегляду планів робіт скористайтесь тегом '\\plans'"

#Дістаємо заявки---------------------------------------------------------------
@app.route("/applications",methods=["GET"])
def getApplications():

    with open('applications', 'rb') as f:
        applications = pickle.load(f)

    return jsonify(applications)

@app.route("/applications/<id>",methods=["GET"])
def getApplication(id):
    with open('applications', 'rb') as f:
        applications = pickle.load(f)

    id = int(id)-1
    return jsonify(applications[id])

#Дістаємо плани робіт----------------------------------------------------------
@app.route("/plans",methods=["GET"])
def getPlans():
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)
    return jsonify(plans)

@app.route("/plans/<id>",methods=["GET"])
def getPlan(id):
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)

    id = int(id)-1
    return jsonify(plans[id])

#Створюємо заявки--------------------------------------------------------------
@app.route("/user/write",methods=["POST"])
def addApplication():
    with open('applications', 'rb') as f:
        applications = pickle.load(f)

    name = request.json['name']
    type = request.json['type']
    value = request.json['value']
    time = request.json['time']
    number = len(applications)
    if(number>0):
        number = applications[-1]['number']+1
    data = {'number':number,'name':name,'type':type,'value':value,'time':time}
    applications.append(data)

    with open('applications', 'wb') as f:
        pickle.dump(applications, f)
    return jsonify(data)


#Видаляємо Заявку---------------------------------------------------------------
@app.route("/applications/<id>",methods=["DELETE"])
def deleteApplication(id):
    with open('applications', 'rb') as f:
        applications = pickle.load(f)

    id = int(id)
    app =  -1
    for a in applications:
        if (a["number"] == id):
            app = a
            break
    if(app==-1):
        return "No such application found"
    applications.remove(app)

    with open('applications', 'wb') as f:
        pickle.dump(applications, f)

    return jsonify(app)



if __name__ == "__main__":
    with open('applications', 'wb') as f:
        pickle.dump(applications, f)
    with open('plans', 'wb') as fb:
        pickle.dump(plans, fb)

    with open('applications', 'rb') as f:
        applications = pickle.load(f)
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)


    app.run(port = 5000)
