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
provider = {"is_logged_in": False, "name": "", "email": "", "lid": ""}
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
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
             #Try signing in the user with the given information
        try:

            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global client
            client["is_logged_in"] = True
            client["email"] = user["email"]
            client["name"] = username
            client["uid"] = user["localId"]
            flash("Logged In Successfully")
            return redirect(url_for('clientHome'))
        
            #If there is any error, redirect back to login
            # return redirect(url_for('client_register'))
        except:
            #If there is any error, redirect back to login
            flash("Login not Successful")
            return redirect(url_for('client_register'))
        
 
    else:
        return render_template("AuthenticationProvider.html")
    



@app.route("/client_register",methods=['GET','POST'])
def client_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pswd']
        email = request.form['email']
       
        
        
        
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            law = auth.sign_in_with_email_and_password(email, password)
            provider["is_logged_in"] = True
            provider["email"] = law["email"]
            provider["name"] = username
            provider["uid"] = law["localId"]
            # db.child("LegalSathi").child("lawyers").child(fullname).update({'address':address,'email':email,'bio':bio,'experience':experience,'name':fullname,'phone':phno,'qualification':qualification,'speciality':speciality,'token':50,'rate':rate})
            # db.child("LegalSathi").child("token").update({fullname:50})
            flash("Account Created Successfully")
            return redirect(url_for('clientHome'))
        except:
            #If there is any error, redirect back to login
            flash("Account not Created")
            return redirect(url_for('lawyer_register'))
        
        
        
        
    else:
        return render_template('Authentication.html')
    
@app.route("/client_login",methods=['GET','POST'])
def client_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']        
        # fullname = request.form['username']
        try:
            law=auth.sign_in_with_email_and_password(email, password)
            provider["is_logged_in"] = True
            provider["email"] = law["email"]
            # provider["name"] = fullname
            flash("Lawyer Logged In Successfully")
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
        password = request.form['pass']        
        fullname = request.form['username']
        try:
            law=auth.sign_in_with_email_and_password(email, password)
            provider["is_logged_in"] = True
            provider["email"] = law["email"]
            provider["name"] = fullname
            flash("Lawyer Logged In Successfully")
            return redirect(url_for('lawyerprofile'))
        except:
            flash("Account not Found Please Register")
            return redirect("provider_login")    
      
        
        
        
        
        
    else:
        return render_template("AuthenticationProvider.html") 

    

@app.route("/clienthome", methods=["POST","GET"])
def clientHome():
    
    return render_template("index.html")

@app.route("/profile", methods=["POST","GET"])
def lawyerprofile():
    data=data=db.child("LegalSathi").child("lawyers").child(provider["name"]).get()
    return render_template("profile.html",data=data.val())




# @app.route("/leaderboard")
# def leaderboard():
#     data=db.child("LegalSathi").child("token").get().val()
#     print(client['email'])
#     sortedDict = sorted(data.items(), key=lambda x:x[1])
#     name =[]
#     token=[]
#     for i in range(len(sortedDict)-1,-1,-1):
#           f = sortedDict[i]
#           name.append(f[0])
#           token.append(f[1])
          
    
#     return render_template("leaderBoard.html",board=zip(name,token),lawyer=provider['name'])


@app.route('/services',methods=['POST','GET'])
def services():
    return render_template('services.html')

@app.route('/request',methods=['GET','POST'])
def req():
    return render_template('forms.html')
         

             

    

    

# @app.route('/chat',methods=['POST','GET'])
# def chat():
#     if request.method == 'POST':
#         return redirect('http://localhost:3000')


@app.route('/probono',methods=['POST','GET'])
def probono():
    # if request.method == 'POST':
    #     return redirect('http://localhost:3000')
    return

@app.route('/postcase',methods=['POST','GET'])
def postacase():
    # if request.method == 'POST':
    #     return redirect('http://localhost:3000')
    return

@app.route('/payments',methods=['POST','GET'])
def payment():
    # if request.method == 'POST':
    #     return redirect('http://localhost:3000')
    return

        

    
if __name__=="__main__":
    
    app.run(debug=True)