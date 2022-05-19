from flask import Flask, render_template, request
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] ='mysecret'
cors = CORS(app)



@app.route("/game", methods = ['POST', 'GET', "PUT"])
def game():
    if request.method == "POST":
        conn = sqlite3.connect('database.db')
        data = request.get_json()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO game (score, date) VALUES ({data['score']}, \'{data['date']}\')")
        conn.commit()
        return data
    if request.method == "GET":
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM game ORDER BY score DESC LIMIT 10")
        scores = cur.fetchall()
        print(scores)
        return {'scores': scores}

if __name__ == '__main__':
    app.run()





