from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Creación de la base de datos y tabla
def init_database():
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos")
def productos():
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos/index.html", productos=productos)

@app.route("/productos/create")
def create():
    return render_template("productos/create.html")

@app.route("/productos/create/save", methods=['POST'])
def productos_save():
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)", (descripcion, cantidad, precio))
    
    conn.commit()
    conn.close()
    return redirect('/productos')

@app.route("/productos/edit/<int:id>")
def productos_edit(id):
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?", (id,))
    
    producto = cursor.fetchone()
    conn.close()
    return render_template("productos/edit.html", producto=producto)

@app.route("/productos/update", methods=['POST'])
def productos_update():
    id = request.form['id']
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?", (descripcion, cantidad, precio, id))
    
    conn.commit()
    conn.close()
    return redirect("/productos")

@app.route("/productos/delete/<int:id>")
def productos_delete(id):
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')

if __name__ == "__main__":
    app.run(debug=True)
