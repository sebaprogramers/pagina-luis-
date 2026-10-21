from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_motos'

def get_db_connection():
    return mysql.connector.connect(
        host='da5.toservers.com',
        port=3306,
        user='luissecr_alumno',
        password='root',
        database='luissecr_educacion'
    )

# 1. CONSULTAR
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT `id moto`, `Moto`, `modelo`, `km`, `precio` FROM `Tabla-de-cuchu`")
        motos = cursor.fetchall()
        cursor.close()
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
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `Tabla-de-cuchu` (`Moto`, `modelo`, `km`, `precio`) VALUES (%s, %s, %s, %s)",
                       (moto, modelo, km, precio))
        conn.commit()
        cursor.close()
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
        cursor = conn.cursor()
        cursor.execute("UPDATE `Tabla-de-cuchu` SET `Moto`=%s, `modelo`=%s, `km`=%s, `precio`=%s WHERE `id moto`=%s",
                       (moto, modelo, km, precio, id_moto))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

# 4. BAJA
@app.route('/eliminar/<int:id_moto>')
def eliminar(id_moto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `Tabla-de-cuchu` WHERE `id moto` = %s", (id_moto,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000)
