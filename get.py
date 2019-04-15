from flask import Flask, jsonify, request

app = Flask(__name__)

accounts = [
    {"name":"Billy", 'balance':457.74},
    {"name":"Renesmee", 'balance':-150.0},
    {"name":"Edward", 'balance':4156.9},
    {"name":"Marla", 'balance':321.31},
    {"name":"Andrew", 'balance':-120.1},
    {"name":"Roxane", 'balance':-10.2},
    {'name':'Kelly','balance':250.0}
]

groups =[
    {"name":"Positive", "members":[]},
    {"name":"Negative","members":[]}
]

def groupsFormat():
    i = 0
    for gr in groups:
        gr['members']=[]

    for person in accounts:
        if person['balance']>=0:
            groups[0]['members'].append(i)
        else:
            groups[1]['members'].append(i)
        i += 1

@app.route("/",methods=["GET"])
def wellcome():
    return "Wellcome to banking system"

@app.route("/accounts",methods=["GET"])
def getAccounts():
    return jsonify(accounts)

@app.route("/accounts/<id>",methods=["GET"])
def getAccount(id):
    id = int(id)-1
    return jsonify(accounts[id])

@app.route("/accounts/<id>",methods=["DELETE"])
def deleteAccount(id):
    id = int(id)-1
    ac = accounts[id]
    accounts.remove(ac)
    groupsFormat()
    return jsonify(ac)


@app.route("/accounts",methods=["POST"])
def addAccounts():
    name = request.json['name']
    balance = float(request.json['balance'])
    data = {'name':name,'balance':balance}
    accounts.append(data)

    groupsFormat()

    return jsonify(data)

@app.route("/accounts",methods=["PUT"])
def changeAccount():
    name = request.json['name']
    balance = float(request.json['balance'])
    data = {'name':name,'balance':balance}
    for acc in accounts:
        if acc['name'] == name:
            acc['balance'] = balance
            return jsonify(data)


    groupsFormat()

    return "No such name"

@app.route("/groups",methods=["GET"])
def getGroups():
    change_groups = []
    for g in groups:
        change_groups.append({"name":g["name"]})
        for acc in g["members"]:
            #str = "member"+str(acc)
            change_groups[-1].update({"member"+str(acc):accounts[acc]})
    return jsonify(change_groups)

if __name__ == "__main__":
    groupsFormat()
    app.run(port = 8080)
