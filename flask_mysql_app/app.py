from flask import Flask, render_template, request
import mysql.connector
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Parsear URL de conexión MySQL de Railway
url = urlparse(os.environ.get("DATABASE_URL"))

db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],
    port=url.port
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT nombre FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template("index.html", usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
    db.commit()
    return "Usuario agregado correctamente"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
