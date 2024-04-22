from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Akhilesh1977'
app.config['MYSQL_DB'] = 'dcc'

mysql = MySQL(app)

@app.route('/', methods = ["POST", "GET"])
def main_page():
    return render_template("index.html") 
@app.route('/pp_search', methods = ["POST", "GET"])
def pp_search():
    if request.method == "POST":
        selected_option = request.form.get("myDropdown")
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `eb_pp` WHERE `{selected_option}` = %s", (request.form["pp_box"],))

        data = cursor.fetchall()

        cursor.close()
        return render_template("PP.html", pp_search_t = data)
    
    return render_template('Q3.html')
@app.route('/indi_search', methods = ["POST", "GET"])
def indi_search():
    if request.method == "POST":
        selected_option = request.form.get("myDropdown")
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `eb_indi` WHERE `{selected_option}` = %s", (request.form["pp_box"],))

        data = cursor.fetchall()

        cursor.close()
        return render_template("INDI.html", pp_search_t = data)
    
    return render_template('Q4.html')
@app.route('/Q2_search', methods = ["POST", "GET"])
def Q2_search():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT YEAR(`Date of Purchase`) AS purchase_year, COUNT(`Bond Number`) AS number_of_bonds, SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10, 2))) FROM eb_indi WHERE(`Name of the Purchaser`= %s) GROUP BY YEAR(`Date of Purchase`)", (request.form["pp_box"],))

        data = cursor.fetchall()

        cursor.close()
        return render_template("INDI_Q2.html", pp_search_t = data)
    
    return render_template('Q2.html')   
@app.route('/Q3_search', methods = ["POST", "GET"])
def Q3_search():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT YEAR(`Date of Encashment`) AS purchase_year, COUNT(`Bond Number`) AS number_of_bonds, SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10, 2))) FROM eb_pp WHERE(`Name of the Political Party`=%s) GROUP BY YEAR(`Date of Encashment`)", (request.form["pp_box"],))

        data = cursor.fetchall()

        cursor.close()
        return render_template("PP_Q3.html", pp_search_t = data)
    
    return render_template('Q3_ag.html')
@app.route('/Q5_search', methods = ["POST", "GET"])
def Q5_search():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT `Name of the Political Party`,`Bond Number`,Denominations FROM eb_pp WHERE `Bond Number` IN (SELECT `Bond Number` FROM eb_indi WHERE `Name of the Purchaser`= %s)", (request.form["pp_box"],))

        data = cursor.fetchall()

        cursor.close()
        return render_template("Q5.html", pp_search_t = data)
    
    return render_template('Q5_ag.html')   
@app.route('/Q4_search', methods = ["POST", "GET"])
def Q4_search():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT `Name of the Purchaser`,`Bond Number`,Denominations FROM eb_indi WHERE `Bond Number` IN (SELECT `Bond Number` FROM eb_pp WHERE `Name of the Political Party` = %s)", (request.form["pp_box"],))

        data = cursor.fetchall()

        cursor.close()
        return render_template("Q4_pp.html", pp_search_t = data)
    
    return render_template('Q4_ag.html')
@app.route('/Q6_search', methods = ["POST", "GET"])
def Q6_search():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT `Name of the Political Party`,SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10, 2))) FROM eb_pp GROUP BY(`Name of the Political Party`)")

    data = cursor.fetchall()

    cursor.close()
    return render_template('Q6_pp.html',pp_search_t = data)
    





# @app.route('/a_2', methods = ["POST", "GET"])
# def a_2():
#     if request.method == "POST":
#         cursor = mysql.connection.cursor()
#         cursor.execute("select title from movie join genre on movie.id = genre.movie_id where genre = %s limit 10", (request.form["box"],))

#         data = cursor.fetchall()

#         cursor.close()
        
#     return render_template("index.html", a_2_data = data) 


# @app.route('/a_3', methods = ["POST", "GET"])
# def a_3():
#     if request.method == "POST":
#         cursor = mysql.connection.cursor()
#         cursor.execute("select title from movie where id in (select movie_id from director_mapping where name_id in (select id from `names` where `name` like %s)) limit 5;", (request.form["box"],))

#         data = cursor.fetchall()

#         cursor.close()
    
#     if len(data) == 0:
#         return render_template("index.html", a_3_data = [["Not Found !!!"]]) 

#     return render_template("index.html", a_3_data = data) 

# @app.route('/a_4', methods = ["POST", "GET"])
# def a_4():
#     if request.method == "POST":
#         cursor = mysql.connection.cursor()
#         cursor.execute("select `name` from `names` where id in (select name_id from director_mapping where movie_id = (select id from movie where title like %s)) LIMIT 1", (request.form["box"],))

#         data = cursor.fetchall()

#         cursor.close()
    
#     if len(data) == 0:
#         return render_template("index.html", a_4_data = [["Not Found !!!"]]) 

#     return render_template("index.html", a_4_data = data)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80", debug = True) 
