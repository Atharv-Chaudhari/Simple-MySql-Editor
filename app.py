from flask import Flask, request, url_for, redirect, render_template
from flask_mysqldb import MySQL
import mysql.connector
import html
import collections
import logging
import traceback

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="2gzE8eN5aw",
    password="jySrN6RaPx",
    database="2gzE8eN5aw"
    )

@app.route('/')
def database():
    mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="2gzE8eN5aw",
    password="jySrN6RaPx",
    database="2gzE8eN5aw"
    )
    mycursor = mydb.cursor()
    tables_names="SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='2gzE8eN5aw'"
    mycursor.execute(tables_names)
    tables = mycursor.fetchall()
    myresult=[]
    columns=[]
    for i in tables:
        names="SELECT * FROM "+i[0]
        mycursor.execute(names)
        myresult.append(mycursor.fetchall())
        names="SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+i[0]+"' ORDER BY ORDINAL_POSITION"
        mycursor.execute(names)
        columns.append(mycursor.fetchall())
    return render_template('index.html',table=tables,column=columns,data=myresult,n=len(tables))

@app.route('/display', methods=['POST', 'GET'])
def display():
    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="2gzE8eN5aw",
        password="jySrN6RaPx",
        database="2gzE8eN5aw"
    )
    mycursor = mydb.cursor()
    try:
        try:
            int_features = [x for x in request.form.values()]
            if(len(int_features[0])==0):
                return render_template("error.html",error="Please Enter Query",query="")
            if(int_features[0].split()[0].lower()=='drop' and int_features[0].split()[1].lower()=='database'):
                return render_template("error.html",error="Drop Database Not Allowed...!!!",query="")
            if(int_features[0].split()[0].lower()=='select'):
                if(int_features[0].split()[1]=='*'):
                    mycursor.execute(int_features[0])
                    myresult = mycursor.fetchall()
                    if(len(myresult)==0):
                        return render_template("error.html",error="Table is Empty..!!!",query=int_features[0])
                    names="SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+int_features[0].split()[-1]+"' ORDER BY ORDINAL_POSITION"
                    mycursor.execute(names)
                    columns = mycursor.fetchall()
                    column=[]
                    for i in columns:
                        column.append(i[3])
                    return render_template("output.html", output=myresult,n=len(myresult[0]),col=column,query=int_features[0])
                else:
                    tables_names="SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='2gzE8eN5aw'"
                    mycursor.execute(tables_names)
                    tables = mycursor.fetchall()
                    columns=[]
                    for i in tables:
                        names="SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+i[0]+"' ORDER BY ORDINAL_POSITION"
                        mycursor.execute(names)
                        columns.append(mycursor.fetchall())
                    column=[]
                    a=int_features[0].lower().index('from')
                    temp=int_features[0].lower()[:a]
                    d=dict()                    
                    for i in columns:
                        for j in i:
                            if j[3].lower() in temp:                           
                                t=temp.replace(","," ")
                                t=t.replace("."," ")
                                if ' as ' in temp:
                                    if (t.split()[t.split().index(j[3])+1].lower()=='as'):
                                        d[temp.index(j[3])]=t.split()[t.split().index(j[3])+2]
                                else:
                                    d[temp.index(j[3])]=j[3]
                                temp=temp.replace(j[3].lower()," "*len(j[3].lower()),1)
                    d=dict(collections.OrderedDict(sorted(d.items())))
                    column=list(d.values())                    
                    mycursor.execute(int_features[0])
                    myresult = mycursor.fetchall()
                    if(len(myresult)==0):
                        return render_template("error.html",error="No Data Avaiable...!!!",query=int_features[0])
                    return render_template("output.html", output=myresult,n=len(myresult[0]),col=column,query=int_features[0])
            elif(int_features[0].split()[0].lower()=='show'):
                mycursor.execute(int_features[0])
                myresult = mycursor.fetchall()
                if(len(myresult)==0):
                    return render_template("error.html",error="Table is Empty..!!!",query=int_features[0])
                names="SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+int_features[0].split()[-1]+"' ORDER BY ORDINAL_POSITION"
                mycursor.execute(names)
                columns = mycursor.fetchall()
                column=[]
                for i in columns:
                    column.append(i[3])
                return render_template("output.html", output=myresult,n=len(myresult[0]),col=column,query=int_features[0])
            else:
                mycursor.execute(int_features[0])
                mydb.commit()
                tables_names="SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='2gzE8eN5aw'"
                mycursor.execute(tables_names)
                tables = mycursor.fetchall()
                myresult=[]
                columns=[]
                for i in tables:
                    names="SELECT * FROM "+i[0]
                    mycursor.execute(names)
                    myresult.append(mycursor.fetchall())
                    names="SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+i[0]+"' ORDER BY ORDINAL_POSITION"
                    mycursor.execute(names)
                    columns.append(mycursor.fetchall())
                return render_template('index.html',table=tables,column=columns,data=myresult,n=len(tables))
        except mysql.connector.Error as e:
            e=str(e)
            html.unescape(e)
            e=e.replace("2gzE8eN5aw.","")
            return render_template("error.html",error=e,query=int_features[0])
    except Exception as ex:
        log_traceback(ex)
        return render_template("error.html",error="Something Went Wrong...!!!",query=int_features[0])

if __name__ == '__main__':
    app.run(debug=True)
