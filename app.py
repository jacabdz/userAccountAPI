from flask import Flask, request, jsonify
import datetime
import copy

app = Flask(__name__)

userList = [
    {
        "id": 1,
        "userName": "Jose",
        "balance": {},
        "transactions": []
    },
    {
        "id": 2,
        "userName": "Vee",
        "balance": {},
        "transactions": []
    },
    {
        "id": 3,
        "userName": "Josh",
        "balance": {},
        "transactions": []
    },
]

# Calculates how far back transactions still have relevancy, and return and int that show oldest relevant transaction
# a relevant transaction is one that is still shown in the balance set
def calPointAge(transactions, balance):
    i = 0
    tmp = copy.deepcopy(balance)
    for tran in transactions:
        total = balanceSum(tmp)
        if total <= 0:
            return i
        tmp[tran['payer']] -= tran['points']
        i += 1

    return i

# Helper method, helps find sum of a balance
def balanceSum(balance):
    total = 0
    for payer in balance:
        total += balance[payer]
    return total

# Takes a list of transactions and the end (pointer to last relevant transaction),
# and returns a working list that is just payer: points
# The working list merges transaction that are negative into positive ones to make
# a cohesive list of just how many points can be used, sorted from newest to oldest.
def workingList(transactions, end):
    i = 0
    tmp = -1
    workingList = []
    while(i <= end):
        if (transactions[i]['points'] < 0):
            tmp = i
        elif ( (transactions[i]['payer'] == transactions[tmp]['payer']) and (tmp>-1) ):
            obj = {
                "payer": transactions[i]['payer'],
                "points": (transactions[i]['points'] + transactions[tmp]['points'])
            }
            workingList.append(obj)
            tmp = -1
        else:
            obj = {
                "payer": transactions[i]['payer'],
                "points": transactions[i]['points']
            }
            workingList.append(obj)
        i += 1

    return workingList

# addTransaction route is a PUT method that takes an id, a payer and an amount of points to add a
# transaction. it auto calculates time at the time of input into the transaction  
@app.route('/addTransactions/', methods=['PUT'])
def addTransactions():
    if ( (request.form['id'] == '') or (request.form['payer'] == '') or (request.form['points'] == '') ):
        return "Error, form not filled out", 400
    for user in userList:
        if int(user['id']) == int(request.form['id']):
            payer = request.form['payer']
            points = int(request.form['points'])
            newTran = {
                "payer": payer,
                "points": points,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }

            if payer in user['balance']:
                user['balance'][payer] += points
            else:
                user['balance'][payer] = points
            user['transactions'].insert(0, newTran)
            return jsonify (user), 200
    return 'Error, incorrect form data', 400

@app.route('/checkBalance/', methods=['GET'])
def checkBalance():
    for user in userList:
        if user['id'] == int(request.form['id']):
            return jsonify(user['balance']), 200
    else:
        return "Error, user not found", 400

# spend route takes a PUT method with the id and amount of points to use for that user. 
# return an error if the user attempts to use more points than owned, 
# if the user has enough points it will remove them according to accountings rules and
#  returns a JSON of how many points were removed from each spender
@app.route('/spend/', methods=['PUT'])
def spend():
    for user in userList:
        if user['id'] == int(request.form['id']):
            if ( 0 > (balanceSum(user['balance'])- int(request.form['points'])) ):
                return "Error, balance not high enough", 400
            
            else:
                changes = []
                flag = 0
                pointsToUse = int(request.form['points'])
                wList = workingList(user['transactions'], calPointAge(user['transactions'], user['balance']) - 1)
                i = len(wList) - 1
                while(pointsToUse > 0):
                    if( (pointsToUse >= wList[i]['points']) ):
                        for change in changes:
                            if wList[i]['payer'] == change['payer']:
                                change['points'] -= wList[i]['points']
                                flag = 1
                        
                        if (flag < 1):
                            obj = {
                                'payer': wList[i]['payer'],
                                'points': -(wList[i]['points'])
                                }   
                            changes.append(obj)
                        
                        tmp = wList[i]['points']
                        user['balance'][wList[i]['payer']] -= tmp
                        pointsToUse -= tmp
                        flag = 0
                    else:
                        obj = {
                            'payer': wList[i]['payer'], 
                            'points' : -(pointsToUse)
                        }
                        changes.append(obj)
                        user['balance'][wList[i]['payer']] -= pointsToUse
                        pointsToUse -= pointsToUse
                    i -= 1

                return jsonify(changes), 200
        else: return "Error, ID does not correspond to user", 400

if __name__ == '__main__':
    app.run()