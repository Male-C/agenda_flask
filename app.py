from flask import Flask, render_template, request, session, redirect
from accesodb import AccesoDB

app = Flask(__name__)

acceso_db = AccesoDB("127.0.0.1", "root", "", "agenda")
app.secret_key = 'supersecreta'

@app.route("/")
def home():
    if 'user' in session:
        if session['user'] == "admin":
            return render_template("admin.html", username="admin")
        else:
            return render_template("index.html", username=session['user'])
    if 'saludo' not in session:
        session['saludo'] = False
    if 'error' not in session:
        session['error'] = False
    return render_template("login.html", error=session['error'], saludo=session['saludo'])


@app.route("/login", methods = ['POST'])
def login():
    username = request.form['username']
    contrasenia = request.form['contrasenia']
    busqueda_user = acceso_db.consulta_generica(f"SELECT * FROM usuarios WHERE usuario = '{username}' AND `contrasenia` = '{contrasenia}'")
    if busqueda_user:
        session['user'] = username
        session['user_id'] = busqueda_user[0]['ID']
        if session['user'] == "admin":
            return render_template("admin.html")
    session['error'] = True
    return redirect("/")

@app.route("/logout", methods = ['POST'])
def logout():
    session.clear()
    session['saludo'] = True
    return redirect("/")

def guardar_datos(nombre, mail, telefono, ig, user_id):
    acceso_db.crear("datos", {"nombre":nombre, "mail":mail, "telefono":telefono, "ig":ig, "user_id":user_id})

def guardar_contactos(usuario, contrasenia):
    acceso_db.crear("usuarios", {"usuario":usuario, "contrasenia":contrasenia})

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
    nom = request.form['usuario']
    contrasenia = request.form['contrasenia']
    print(nom, contrasenia)
    guardar_contactos(nom, contrasenia)
    return render_template("admin.html",nuevo_usuario=True)

@app.route("/buscar", methods=['POST'])
def consultar_contacto():
    nom = request.form['nombre']
    resultado = acceso_db.consulta_generica(f"SELECT * FROM datos WHERE nombre LIKE '%{nom}%' AND user_id = '{session['user_id']}'")
    for contacto in resultado:
        print(contacto)
    return render_template("index.html",  contactos=resultado)

@app.route("/buscar_usuarios", methods=['POST'])
def consultar_usuario():
    nom = request.form['usuario']
    print("Nombre recibido:", nom)
    resultado = acceso_db.consulta_generica(f"SELECT * FROM usuarios WHERE usuario LIKE '%{nom}%' AND ID != 0")
    print("SQL ejecutada:", resultado)
    print("Resultado:", resultado)

    for usuario in resultado:
        print("rter",usuario)
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
    

@app.route("/editarborrar_usuarios", methods=['POST'])
def borrar_usuario():
    user_id = int(request.form['id'])

    if user_id == 0:
        return render_template("admin.html", error="No se puede modificar ni borrar el admin")

    if request.form['action'] == 'Borrar':
        acceso_db.borrar("usuarios", ("ID", user_id))
        return render_template("admin.html", borrado=True)

    elif request.form['action'] == 'Editar':
        query = "UPDATE usuarios SET "
        query += f"usuario = '{request.form['usuario']}', "
        query += f"contrasenia = '{request.form['contrasenia']}' "
        query += f"WHERE ID = '{user_id}'"
        print("Query:", query)
        acceso_db.modificacion_generica(query)
        return render_template("admin.html", modificado=True)


if __name__ == "__main__":
    app.run()
