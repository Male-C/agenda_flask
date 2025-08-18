from flask import Flask, render_template, request
from accesodb import AccesoDB

app = Flask(__name__)

colores = ['azul', 'verde', 'rojo', 'rosa', 'violeta', 'blanco']

acceso_db = AccesoDB("127.0.0.1", "root", "", "agenda")

@app.route("/")
def home():
    return render_template("index.html")

def guardar_datos(nombre, mail, telefono, ig):
    acceso_db.crear("datos", {"nombre":nombre, "mail":mail, "telefono":telefono, "ig":ig})

@app.route("/nuevo", methods=['POST'])
def nuevo_contacto():
    nom = request.form['nombre']
    mail = request.form['mail']
    tel = request.form['telefono']
    ig = request.form['ig']
    print(nom, mail, tel, ig)
    guardar_datos(nom, mail, tel, ig)
    return render_template("index.html",nuevo=True)


@app.route("/buscar", methods=['POST'])
def consultar_contacto():
    nom = request.form['nombre']
    resultado = acceso_db.consulta_generica(f"SELECT * FROM datos WHERE nombre LIKE '%{nom}%'")
    for contacto in resultado:
        print(contacto)

    return render_template("index.html",  contactos=resultado)

@app.route("/editarborrar", methods=['POST'])
def borrar_contacto():
    if request.form['action'] == 'Borrar':
        acceso_db.borrar("datos", ("ID",request.form["id"]))
        return render_template("index.html", borrado=True)
    elif request.form['action'] == 'Editar':
        query = "UPDATE datos SET "
        query += f"nombre = '{request.form['nombre']}',"
        query += f"telefono = '{request.form['telefono']}',"
        query += f"mail = '{request.form['mail']}',"
        query += f"ig = '{request.form['ig']}' "
        query += f"WHERE (ID = '{request.form['id']}')"
        print(query)
        acceso_db.modificacion_generica(query)
        return render_template("index.html", modificado=True)
    else:
        return render_template("index.html", error=True)

if __name__ == "__main__":
    app.run()
