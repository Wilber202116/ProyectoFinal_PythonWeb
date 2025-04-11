import json
import os
#ruta del archivo json
USERS_FILE = os.path.join("data", "users.json")

#funcion para cargar el archivo json
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return []

def getUsersBycui(cui):
    users = load_users()
    return next((u for u in users if u["cui"] == cui), None)

#funcion para guardar los usuarios

def save_users(users):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)

def register_users(nameCUI, name, email, password, dateBorn, picturepath):
    users = load_users()
    if getUsersBycui(nameCUI):
        return False
    
    newuser = {
            'cui':nameCUI,
            'name':name,
            'email': email,
            'password': password,
            'dateborn': dateBorn,
            'profilePicture': picturepath
        }

    users.append(newuser)
    save_users(users)
    return True
    