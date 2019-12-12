import sqlite3
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


def get_db():
    db = sqlite3.connect('mydb.db')
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/weather", methods=["GET", "POST"])
def weather():
    if request.method == "GET":
        res = query_db("SELECT * FROM weather WHERE id <= 6")  # 不妨设定：第一次只返回6个数据
    elif request.method == "POST":
        res = query_db("SELECT * FROM weather WHERE id = (?)", args=(int(request.form['id']) + 1,))  # 以后每次返回1个数据
        # res = query_db("SELECT * FROM weather WHERE id = 13") # 一个不存在的记录

    return jsonify(month=[x[1] for x in res],
                   evaporation=[x[2] for x in res],
                   precipitation=[x[3] for x in res])  # 返回json格式


if __name__ == "__main__":
    app.run(debug=True)