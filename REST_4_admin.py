from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

applications = []

plans =[]


def groupsFormat():
    with open('applications', 'rb') as f:
        applications = pickle.load(f)
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)

    numb = plans[-1]["app"]
    for i in applications:
        if(i['number']==numb):
            plans[-1]["app"] = i

    with open('plans', 'wb') as fb:
        pickle.dump(plans, fb)

    return jsonify(plans[-1])

#Wellcome pages----------------------------------------------------------------
@app.route("/",methods=["GET"])
def wellcome():
    return "Вітаємо в системі житлово-комунального підприємства!\n\n"+"Щоб увійти як адміністратор скористайтесь тегом '\\admin'\n\n"+"Для перегляду заявок скористайтесь тегом '\\applications'\n"+"Для перегляду планів робіт скористайтесь тегом '\\plans'"

@app.route("/admin",methods=["GET"])
def admin():
    return "Вітаємо в системі житлово-комунального підприємства!\n\n"+"Для перегляду заявок скористайтесь тегом '\\applications'\n"+"Для написання плану робіт скористайтесь тегом POST '\\admin\\write'\n"+"1. У плані потрібно вказати дату (параметр 'date')\n"+"2. Кількість виділених людей ('numb')\n3.  Інструменти ('tools')\n"+"4. Номер заявки('app')\n"+"5. Вартість('Value')\n\n"+"Для перегляду планів робіт скористайтесь тегом '\\plans'"

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


#Створюємо план--------------------------------------------------------------
@app.route("/admin/write",methods=["POST"])
def addPlan():
    with open('applications', 'rb') as f:
        applications = pickle.load(f)
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)

    date = request.json['date']
    numb = int(request.json['numb'])
    tools = request.json['tools']
    value = float(request.json['value'])
    app = int(request.json['app'])

    id = len(plans)
    if(id>0):
        id = plans[-1]['id']+1

    data = {'date':date,'numb':numb,'tools':tools,'value':value,'app':app,'id':id}
    plans.append(data)

    with open('plans', 'wb') as fb:
        pickle.dump(plans, fb)

    plan = groupsFormat()


    return plan #jsonify(data)


#Видаляємо План---------------------------------------------------------------
@app.route("/plans/<id>",methods=["DELETE"])
def deletePlan(id):
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)
    id = int(id)
    pl =  -1
    for p in plans:
        if (p["id"] == id):
            pl = p
            break
    if(pl==-1):
        return "No account found"

    plans.remove(pl)

    with open('plans', 'wb') as fb:
        pickle.dump(plans, fb)
    return jsonify(pl)

if __name__ == "__main__":

    with open('applications', 'rb') as f:
        applications = pickle.load(f)
    with open('plans', 'rb') as fb:
        plans = pickle.load(fb)
    app.run(port = 8080)
