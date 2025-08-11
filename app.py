from flask import Flask, render_template, request
from accesodb import AccesoDB

app = Flask(__name__)

colores = ['azul', 'verde', 'rojo', 'rosa', 'violeta', 'blanco']

acceso_db = AccesoDB("127.0.0.1", "root", "", "agenda")

@app.route("/")
def home():
    return render_template("index.html", titulo="Hola desde Flask", colores=colores)

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
    return render_template("index.html", titulo="Hola desde Flask", colores=colores, nuevo=True)




if __name__ == "__main__":
    app.run()
