from flask import Flask,redirect,request,render_template,url_for,jsonify,flash

import pyrebase
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate("eltern-ea0e3-firebase-adminsdk-pwxqq-cf5a31503b.json")
firebase_admin.initialize_app(cred)



app=Flask(__name__)
app.secret_key='MyFlaskApp'


config = {
  "apiKey": os.getenv('apiKey'),
  "authDomain": os.getenv('authDomain'),
  "databaseURL": os.getenv('databaseURL'),
  "storageBucket": "PASTE_HERE"
}


#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#to keep session data for client or lawyer
provider = {"is_logged_in": False, "name": "", "email": "", "lid": "","phone":""}
client = {"is_logged_in": False, "name": "", "email": "", "lid": ""}


@app.route("/")
def landing():
    #session out for both client or lawyer
    client["is_logged_in"] = False
    client["email"] = ""
    client["name"] = ""
    client["uid"] = ""
    provider["is_logged_in"] = False
    provider["email"] = ""
    provider["name"] = ""
    return render_template("Landing.html")

@app.route("/provider_register",methods=['GET','POST'])
def provider_register():

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pswd']
        phone = request.form['phone']
        email = request.form['email']
       
        
        
        try:

            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            law = auth.sign_in_with_email_and_password(email, password)
            client["is_logged_in"] = True
            client["email"] = law["email"]
            client["name"] = username
            client["phone"]=phone
            client["uid"] = law["localId"]
            print(client)
            db.child('Provider').child('Names').update({phone:username})
            # db.child("LegalSathi").child("token").update({fullname:50})
            flash("Account Created Successfully")
            return redirect(url_for('providerHome'))
             #If there is any error, redirect back to login
        # flash("Account not Created")
        # return redirect(url_for('client_register'))
        except:
            flash("Account not Found Please Register")
            return redirect("provider_login") 

        
        
        
        
    else:
        return render_template('AuthenticationProvider.html')
    



@app.route("/client_register",methods=['GET','POST'])
def client_register():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pswd']
        phone = request.form['phone']
        email = request.form['email']
       
        
        
        try:

            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            law = auth.sign_in_with_email_and_password(email, password)
            client["is_logged_in"] = True
            client["email"] = law["email"]
            client["name"] = username
            client["phone"]=phone
            client["uid"] = law["localId"]
            print(client)
            db.child('Client').child('Names').update({phone:username})
            # db.child("LegalSathi").child("token").update({fullname:50})
            flash("Account Created Successfully")
            return redirect(url_for('clientHome'))
             #If there is any error, redirect back to login
        # flash("Account not Created")
        # return redirect(url_for('client_register'))
        except:
            flash("Account not Found Please Register")
            return redirect("client_login") 

        
        
        
        
    else:
        return render_template('Authentication.html')
    
@app.route("/client_login",methods=['GET','POST'])
def client_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']        
        phone=request.form['phone']
        try:
            law=auth.sign_in_with_email_and_password(email, password)
            fullname = db.child('Client').child('Names').child(phone).get().val()
            client["is_logged_in"] = True
            client["email"] = law["email"]
            client["name"] = fullname
            flash("Client Logged In Successfully")
            return redirect(url_for('clientHome'))
        except:
            flash("Account not Found Please Register")
            return redirect("client_login")    
      
        
        
        
        
        
    else:
        return render_template("Authentication.html")  
@app.route("/provider_login",methods=['GET','POST'])
def provider_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']        
        phone=request.form['phone']
        try:
            law=auth.sign_in_with_email_and_password(email, password)
            fullname = db.child('Provider').child('Names').child(phone).get().val()
            client["is_logged_in"] = True
            client["email"] = law["email"]
            client["name"] = fullname
            flash("Provider Logged In Successfully")
            return redirect(url_for('providerHome'))
        except:
            flash("Account not Found Please Register")
            return redirect("provider_login")    
      
        
        
        
        
        
    else:
        return render_template("AuthenticationProvider.html") 

    

@app.route("/clienthome", methods=["POST","GET"])
def clientHome():
    
    return render_template("index.html")

@app.route("/providerhome", methods=["POST","GET"])
def providerHome():
    data=db.child("Orders").get().val()
    l=[]
    print(data)
    for datas in data:
        
        
        service=db.child("Orders").child(datas).child('service').get().val()
        Address=db.child("Orders").child(datas).child('Address').get().val()
        date=db.child("Orders").child(datas).child('date').get().val()
        Pname=db.child("Orders").child(datas).child('Pname').get().val()
        Cname=db.child("Orders").child(datas).child('Cname').get().val()
        Pphone=db.child("Orders").child(datas).child('Pphone').get().val()
        Approve=db.child("Orders").child(datas).child('Approve').get().val()
        
        if Approve==False:
            l.append([service,Address,date,Pname,Pphone,Cname])

    return render_template("Providerindex.html",info=l)


@app.route('/Porder',methods=['POST','GET'])
def porder():
    data=db.child('Client-Provider').child(provider["name"]).get().val()
    return render_template('porder.html',data=data)





@app.route('/services',methods=['POST','GET'])
def services():
    return render_template('services.html')

@app.route('/request',methods=['GET','POST'])
def req():
    
    if request.method == "POST":
        Cname=request.form['Cname']
        date=request.form['date']
        service=request.form['service']
        Pname=request.form['Pname']
        Pphone=request.form['Pphone']
        addr=request.form['addr']
        
        db.child('Orders').child(client["name"]).update({"Cname":Cname,"date":date,"service":service,"Pname":Pname,"Pphone":Pphone,"Address":addr,"Cemail":client["email"],"Approve":False})
        flash("Thank you for trusting us. Your Service is placed and is under process")
        return redirect(url_for("req"))


    return render_template('request.html')

@app.route('/orders',methods=['GET','POST'])
def orders():
    data=db.child("Orders").child(client["name"]).get().val()
    return render_template('order.html',data=data)


@app.route('/approve',methods=['POST','GET'])
def approve():
    if request.method == 'POST':
        name= request.args.get('name')
        service=db.child("Orders").child(name).child('service').get().val()
        Address=db.child("Orders").child(name).child('Address').get().val()
        date=db.child("Orders").child(name).child('date').get().val()
        Pname=db.child("Orders").child(name).child('Pname').get().val()
        Cname=db.child("Orders").child(name).child('Cname').get().val()
        Pphone=db.child("Orders").child(name).child('Pphone').get().val()
        Approve=db.child("Orders").child(name).child('Approve').get().val()
        db.child('Orders').child(name).update({'Approve':True})
        db.child('Client-Provider').child(provider["name"]).update({'Cname':Cname,'Address':Address,"date":date,"Pname":Pname,"Service":service,"Pphone":Pphone,})
        return redirect(url_for('providerHome'))
        

        

        

    

         

             

    

    



        

    
if __name__=="__main__":
    
    app.run(debug=True)