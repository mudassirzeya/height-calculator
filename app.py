from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector'
# app.config['SQLALCHEMY_DATABASE_URI']='postgres://orgyloxjhkipbf:c437796ae82507100925bc1cd5e0861aeb705a3593cc18df513032f237c747aa@ec2-3-213-106-122.compute-1.amazonaws.com:5432/d8b6eklod5f37d'    
db= SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id= db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self,email_,height_): 
        self.email_ = email_
        self.height_ = height_



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    if request.method=='POST':
        email= request.form['email_name']
        height= request.form['height_name']
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data= Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height= round(average_height,1)
            count= db.session.query(Data.height_).count()
            send_email(email, height,average_height,count)
            return render_template("success.html")
        return render_template("index.html", text="seems like we have that email already!")

if __name__ == "__main__":
    app.debug=True
    app.run()