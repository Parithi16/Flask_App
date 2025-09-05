from flask import Flask, request,jsonify
app = Flask(__name__)

@app.route('/sum', methods=['GET'])
def sum():
    a=int(request.args.get('a',default=0,type=int))
    b=int(request.args.get('b',default=0,type=int))
    return "The sum of "+str(a)+" and "+ str(b)+ " is "+ str(a+b)

@app.route('/bank',methods=['POST'])
def cal_amount():
    data=request.get_json()
    balance=data["net_amount"]
    mode=data["mode"]
    amount=data["amount"]

    if mode=="deposit":
        balance=balance+amount
        return jsonify({"Balance":balance})
    
    if mode=="withdraw":
        if (balance<amount):
            return jsonify({"Error":"Insufficient balance"})
        else:
            balance=balance-amount
            return jsonify({"Balance":balance})

if __name__=="__main__":
     app.run(debug=True)