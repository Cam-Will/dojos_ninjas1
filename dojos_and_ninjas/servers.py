from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/dojos")
def index():
    mysql = connectToMySQL('dojos_and_ninjas') # call the function, passing in the name of our db
    query = "SELECT * FROM dojos_and_ninjas.dojos;"
    dojos = mysql.query_db(query)  # call the query_db function, pass in the query as a string
    print(dojos)
    return render_template("dojos.html", dojos = dojos)
            

@app.route("/dojos", methods=["POST"]) 
def add_dojo_to_db():
    mysql = connectToMySQL("dojos_and_ninjas")
    query = "INSERT INTO `dojos_and_ninjas`.`dojos` (`name`) VALUES (%(dn)s);"
    data = {
        "dn": request.form["dname"],
    }
    dojo = mysql.query_db(query, data)
    print(dojo)
    return redirect("/dojos")

@app.route("/ninjas", methods=["POST"])
def create_new():
    mysql = connectToMySQL("dojos_and_ninjas")
    query = "INSERT INTO `dojos_and_ninjas`.`ninjas` (first_name, last_name, age, dojo_id) VALUES (%(fn)s, %(ln)s, %(age)s, %(dojo_id)s);"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "age":request.form["age"],
        "dojo_id": request.form["dojo"]
    }
    ninja = mysql.query_db(query,data)
    print(ninja)
    return redirect("/dojos/"+request.form["dojo"])

@app.route("/ninjas")
def select_dojo():
    mysql = connectToMySQL("dojos_and_ninjas")
    query = "SELECT * FROM dojos_and_ninjas.dojos;"
    dojo = mysql.query_db(query)
    print(dojo)
    return render_template("new_ninja.html", dojo = dojo)

@app.route("/dojos/<id>")
def show_dojo(id):
    mysql = connectToMySQL("dojos_and_ninjas")
    query = "SELECT * FROM dojos_and_ninjas.ninjas WHERE dojo_id = %(dojo_id)s;"
    data = {
        "dojo_id": id
    }
    ninja = mysql.query_db(query,data)
    mysql = connectToMySQL("dojos_and_ninjas")
    query = "SELECT * FROM dojos_and_ninjas.dojos WHERE id = %(dojo)s;"
    data = {
        "dojo": id
    }
    dojo = mysql.query_db(query,data)
    print(ninja)
    return render_template("dojo_show.html", ninja = ninja, dojo = dojo)

if __name__ == "__main__":
    app.run(debug=True)