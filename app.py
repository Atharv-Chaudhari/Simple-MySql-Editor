from flask import Flask, request, url_for, redirect, render_template
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="atharv"
)


@app.route('/')
def database():
    return render_template("index.html")


@app.route('/display', methods=['POST', 'GET'])
def display():
    mycursor = mydb.cursor()
    try:
        int_features = [x for x in request.form.values()]
        
        if(int_features[0].split()[0].lower()=='select'):
            if(int_features[0].split()[1]=='*'):
                mycursor.execute(int_features[0])
                myresult = mycursor.fetchall()
                names="SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+int_features[0].split()[-1]+"' ORDER BY ORDINAL_POSITION"
                mycursor.execute(names)
                columns = mycursor.fetchall()
                column=[]
                for i in columns:
                    column.append(i[3])
                return render_template("output.html", output=myresult,n=len(myresult[0]),col=column,query=int_features[0])
            else:
                return render_template("error.html",error="Please Use Queries which Fetch Whole Table...!!!",query=int_features[0])
        else:
            mycursor.execute(int_features[0])
            mydb.commit()
            return render_template("index.html")
    except:
        return render_template("error.html",error="Please Check your Query...!!!",query=int_features[0])

if __name__ == '__main__':
    app.run(debug=True)
