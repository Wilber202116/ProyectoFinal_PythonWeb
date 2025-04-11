from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import getUsersBycui, save_users, register_users, load_users
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

auth_bp = Blueprint("auth", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = "static/uploads"
 

#"a" in "arbol" = TRUE
#"." in "arbol" = FALSE
#Esta funcion va a validar el .png o jpg de las imagenes
def allowed_picture(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nameCUI = request.form['cui']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dateBorn = request.form['dateborn']
        profilePicture = request.files['profilePicture']

        filename = None
        if profilePicture:
            filename = secure_filename(profilePicture.filename)
            profilePicture.save(os.path.join(UPLOAD_FOLDER, filename))
        
        path = UPLOAD_FOLDER + "/" + filename
        '''
        users = load_users()
        #validar si el usuario existe en la database
        if any(u["email"] == email for u in users):
            flash("El email ya esta registrado", "danger")
            return redirect(url_for("register"))
        

        if profilePicture and allowed_picture(profilePicture.filename):
            picturename = secure_filename(f"{nameCUI}_{profilePicture.name}")
            picturepath = os.path.join(app.config["UPLOAD_FOLDER"], picturename)
            profilePicture.save(picturepath)
        else:
            flash("formato de la imagen no valido", "danger")
            return redirect(url_for("register"))
        '''
        if register_users(nameCUI, name, email, password, dateBorn, path):
            flash("Registro exitoso", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("El usuario ya existe", "danger")
            return redirect(url_for("auth.register"))

    return render_template('register.html')

@auth_bp.route("/", methods=[ "GET", "POST"])
def login():
    if request.method == "POST":
        cui = request.form['cui']
        password = request.form['password']
        #users = load_users()#carga la lista que esta en json
        user = getUsersBycui(cui)
        '''
        ya no se va a utilizar este codigo
        for user in users: #recorre la lista de usuarios
            # simulacion de autenticacion
            if user["email"] == correo and user["password"] == password:
                username = user["username"]
                session["user"] = username
                
                return redirect(url_for("home"))'
        '''
        if user and user["password"] == password:
            session["cui"] = user["cui"]
            return redirect(url_for("catalog.products"))
        else:
            flash("Credenciales incorrectas, intentalo de nuevo", "danger")
    
    return render_template('index.html')

#metodo GET
@auth_bp.route("/home")
def home():
    cui = session.get("cui")

    if not cui:
        flash("Debes iniciar sesion", "danger")
        return redirect(url_for("auth.login"))
    
    # obtenemos el usuario que se va a ingresar
    user = getUsersBycui(cui)

    if not user:
        flash("Usuario no encontrado", "danger")
        session.pop("cui", None)
        return redirect(url_for("auth.login"))
    
    return render_template("home2.html", user = user, session = session)
    '''
    if "cui" not in session:
        flash()
        return redirect(url_for("auth.login"))
    return render_template('home2.html', username = session["cui"])
            #return render_template('home2.html', email = email, password = password)
        #else:
            #flash('credenciales incorrectas, intenta de nuevo')
            #return redirect(url_for('login'))'
    '''

# metodo get es por defecto
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesion cerrada correctamente", "success")
    return redirect(url_for("auth.login"))
