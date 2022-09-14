import re

import pymongo
from flask import (Flask, flash, redirect, render_template, request, session,url_for)

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'jweghdfuyomeg78t8jksab'


@app.route('/', methods=['GET', 'POST'])
def home():
    s = ''
    auth = False
    if "name" in session:
        name = session["name"]
        s = "Hello " + name
        auth = True
    return render_template("home.html", **locals())
    # else:
    #     print("not in session")
    #     return redirect('/login')

    # if request.method == 'POST':
    #         return render_template("home.html", **locals())

    # return render_template("home.html" , **locals())


@app.route('/regi', methods=['GET', 'POST'])
def regi():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    s = ""
    nameMsg = ""
    emailMsg = ""
    passMsg = ""
    successMsg = ""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["CoffeeTalesDatabase"]
    myregis = mydb["myregi"]

    if request.method == "POST":
        d = dict()
        d["name"] = request.form["name"]
        d["email"] = request.form["email"]
        d["password1"] = request.form["password1"]
        d["password2"] = request.form["password2"]

        if d["password1"] == d["password2"] and re.fullmatch(regex, d["email"]) and len(d["name"]) >= 3 and len(d["password1"]) >= 4:
            successMsg = "Registration Successful"
            myregis.insert_one(d)
            return render_template("reg.html", successMsg=successMsg)
        elif len(d["name"]) <= 3:
            nmeMsg = "name should be greater than 3 character"
            return render_template("reg.html", nameMsg=nmeMsg)
        elif len(d["password1"]) <= 4:
            passMsg = "password should be greater than 3 character"
            return render_template("reg.html", passMsg=passMsg)
        elif d["password1"] != d["password2"]:
            passMsg = "Password Are not same ,please enter same password"
            return render_template("reg.html", passMsg=passMsg)
        else:
            emailMsg = "please enter correct email"
            return render_template("reg.html", emailMsg=emailMsg)

    return render_template("reg.html", **locals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('home'))
    s = ""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["CoffeeTalesDatabase"]
    myregis = mydb["myregi"]
    d = request.form["email"]
    p = request.form["password"]
    user = myregis.find_one({"email": d})
    if not user:
        flash('Login Unsuccessful', 'danger')
    elif p == user["password1"]:
        flash('Login successful', 'success')
        session["email"] = d
        session["name"] = user["name"]
    elif p != user["password1"]:
        flash('Login Unsuccessful', 'danger')
    else:
        flash('user not found', 'danger')
    return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
def logout():
    logoutMsg = "You are logged out"
    # session.clear()
    session.pop("email", None)
    session.pop("name", None)
    return render_template('home.html', logoutMsg=logoutMsg)


@app.route('/about-us-read-more', methods=['GET'])
def about_us_read_more():
    s = ''
    auth = False
    if "name" in session:
        name = session["name"]
        s = "Hello " + name
        auth = True
    return render_template('about_us_read_more.html', **locals())


@app.route('/menu-read-more', methods=['GET'])
def menu_read_more():
    s = ''
    auth = False
    if "name" in session:
        name = session["name"]
        s = "Hello " + name
        auth = True
    return render_template('menu_read_more.html', **locals())

@app.route('/blogs', methods=['GET'])
def blogs():
    s = ''
    auth = False
    if "name" in session:
        name = session["name"]
        s = "Hello " + name
        auth = True
    return render_template('blogs.html', **locals())


@app.route('/post_tales', methods=['GET','POST'])
def post_tales():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["CoffeeTalesDatabase"]
    post_tales = mydb["post_tales"]

    if request.method == "POST":
        d = dict()
        d["name"] = request.form["name"]
        d["story"] = request.form["story"]

        post_tales.insert_one({'name' : d["name"] , 'story': d["story"] , 'complete' : False})

    nw = post_tales.find()
    return render_template("post_tales.html", **locals())



@app.route('/order', methods=['GET','POST'])
def order():
    #sucMsg = ""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["CoffeeTalesDatabase"]
    order_cfe = mydb["order_cfe"]

    if request.method == "POST":
        d = dict()
        d["fname"] = request.form["fname"]
        d["cfe"] = request.form["cfe"]
        d["num"] = request.form["num"]
        d["adrs"] = request.form["adrs"]

        if request.form.getlist('quantity'):
            d["quantity"]='1'

        order_cfe.insert_one({'fname' : d["fname"] , 'cfe': d["cfe"] , 'num' : d["num"] , 'adrs': d["adrs"], 'quantity': d["quantity"] })
    #order_cfe.insert_one(d)
    #sucMsg = "Order Successful"
    return render_template('order.html', **locals())


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    #delMsg=""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["CoffeeTalesDatabase"]
    order_cfe = mydb["order_cfe"]

    if request.method =="POST":
        d= request.form["fname"]
        p=order_cfe.delete_many({"fname":d})
        print(p)
    #delMsg = "Delete Successful"
    return render_template('del.html', **locals())


if __name__ == '__main__':
    app.run(debug=True)
