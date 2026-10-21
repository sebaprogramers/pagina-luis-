from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import webbrowser
from threading import Timer
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_motos'

DB_NAME = 'motos_database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `Tabla-de-cuchu` (
            `id moto` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Moto` TEXT NOT NULL,
            `modelo` TEXT NOT NULL,
            `km` TEXT NOT NULL,
            `precio` TEXT NOT NULL
        )
    ''')
    # Datos de ejemplo iniciales si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM `Tabla-de-cuchu`")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO `Tabla-de-cuchu` (`Moto`, `modelo`, `km`, `precio`)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Yamaha YBR', '125', '15000', '1200000'),
            ('Honda Titan', '150', '22000', '1500000')
        ])
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 1. CONSULTAR
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        motos = conn.execute("SELECT `id moto`, `Moto`, `modelo`, `km`, `precio` FROM `Tabla-de-cuchu`").fetchall()
        conn.close()
        return render_template('index.html', motos=motos)
    except Exception as e:
        return f"Error en la base de datos: {str(e)}"

# 2. ALTA
@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        moto = request.form['moto']
        modelo = request.form['modelo']
        km = request.form['km']
        precio = request.form['precio']

        conn = get_db_connection()
        conn.execute("INSERT INTO `Tabla-de-cuchu` (`Moto`, `modelo`, `km`, `precio`) VALUES (?, ?, ?, ?)",
                     (moto, modelo, km, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

# 3. MODIFICACIÓN
@app.route('/editar', methods=['POST'])
def editar():
    if request.method == 'POST':
        id_moto = request.form['id_moto']
        moto = request.form['moto']
        modelo = request.form['modelo']
        km = request.form['km']
        precio = request.form['precio']

        conn = get_db_connection()
        conn.execute("UPDATE `Tabla-de-cuchu` SET `Moto`=?, `modelo`=?, `km`=?, `precio`=? WHERE `id moto`=?",
                     (moto, modelo, km, precio, id_moto))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

# 4. BAJA
@app.route('/eliminar/<int:id_moto>')
def eliminar(id_moto):
    conn = get_db_connection()
    conn.execute("DELETE FROM `Tabla-de-cuchu` WHERE `id moto` = ?", (id_moto,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    init_db()
    Timer(1.5, open_browser).start()
    app.run(port=5000)