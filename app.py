from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def crear_bd():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT,
            mensaje TEXT
        )
    """)

    conn.commit()
    conn.close()

crear_bd()

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        cursor.execute(
            "INSERT INTO contactos (nombre, email, mensaje) VALUES (?, ?, ?)",
            (nombre, email, mensaje)
        )
        conn.commit()

    cursor.execute("SELECT * FROM contactos ORDER BY id DESC")
    mensajes = cursor.fetchall()

    conn.close()

    return render_template('contacto.html', mensajes=mensajes)

if __name__ == '__main__':
    app.run(debug=True)