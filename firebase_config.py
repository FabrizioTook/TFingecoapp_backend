import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore


def firebase_init():
    # Verificar si Firebase ya está inicializado
    if not firebase_admin._apps:
        # Si no está inicializado, inicializamos Firebase con las credenciales
        cred = credentials.Certificate("privateKey.json")
        firebase_admin.initialize_app(cred)
    else:
        # Si Firebase ya está inicializado, no hacemos nada
        print("Firebase ya está inicializado.")

    # Acceder a la base de datos Firestore
    db = firestore.client()
    return db


def firebase_auth():
    config = {
        "apiKey": "AIzaSyBcGkGLCbGJn3YMhd_A5SpAM-sKS0D7dPE",
        "authDomain": "tf-finanzas-32fd6.firebaseapp.com",
        "projectId": "tf-finanzas-32fd6",
        "storageBucket": "tf-finanzas-32fd6.firebasestorage.app",
        "messagingSenderId": "549253212164",
        "appId": "1:549253212164:web:a323f1247df46a57946d51",
        "databaseURL": "",
    }

    # Inicializamos Firebase con Pyrebase
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    return auth
