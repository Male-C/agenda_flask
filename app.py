from flask import Flask, render_template, request, session, redirect
from accesodb import AccesoDB

app = Flask(__name__)

colores = ['azul', 'verde', 'rojo', 'rosa', 'violeta', 'blanco']

acceso_db = AccesoDB("127.0.0.1", "root", "", "agenda")
app.secret_key = 'supersecreta'

@app.route("/")
def home():
    if 'user' in session:
        return render_template("index.html", username=session['user'])
    if 'saludo' not in session:
        session['saludo'] = False
    if 'error' not in session:
        session['error'] = False
    return render_template("login.html", error=session['error'], saludo=session['saludo'])


@app.route("/login", methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    busqueda_user = acceso_db.consulta_generica(f"SELECT * FROM usuarios WHERE usuario = '{username}' AND `password` = '{password}'")
    if busqueda_user:
        session['user'] = username
        session['user_id'] = busqueda_user[0]['ID']
        if username == "admin":
            return render_template("admin.html")    
        return redirect("/")
    session['error'] = True
    return redirect("/")

@app.route("/logout", methods = ['POST'])
def logout():
    session.clear()
    session['saludo'] = True
    return redirect("/")

def guardar_datos(nombre, mail, telefono, ig, user_id):
    acceso_db.crear("datos", {"nombre":nombre, "mail":mail, "telefono":telefono, "ig":ig, "user_id":user_id})

@app.route("/nuevo", methods=['POST'])
def nuevo_contacto():
    nom = request.form['nombre']
    mail = request.form['mail']
    tel = request.form['telefono']
    ig = request.form['ig']
    user_id = session['user_id']
    print(nom, mail, tel, ig, user_id)
    guardar_datos(nom, mail, tel, ig, user_id)
    return render_template("index.html",nuevo=True)

@app.route("/nuevo_usuario", methods=['POST'])
def nuevo_usuario():
    nom = request.form['nombre']
    contrasena = request.form['contrasena']
    user_id = int
    print(nom, contrasena, user_id)
    guardar_datos(nom, contrasena, user_id)
    return render_template("admin.html",nuevo_usuario=True)

@app.route("/buscar", methods=['POST'])
def consultar_contacto():
    nom = request.form['nombre']
    resultado = acceso_db.consulta_generica(f"SELECT * FROM datos WHERE nombre LIKE '%{nom}%' AND user_id = '{session['user_id']}'")
    for contacto in resultado:
        print(contacto)
    return render_template("index.html",  contactos=resultado)

@app.route("/buscar_usuario", methods=['POST'])
def consultar_usuario():
    nom = request.form['usuario']
    resultado = acceso_db.consulta_generica(f"SELECT * FROM usuarios WHERE usuario LIKE '%{nom}%'")
    for usuario in resultado:
        print(usuario)
    return render_template("admin.html",  usuarios=resultado)

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
