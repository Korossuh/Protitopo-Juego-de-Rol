# Ojala funcione esto
from pymongo import MongoClient
from getpass import getpass  # For secure password input

url = "mongodb+srv://<username>:<password>@cluster0.rlqm0qg.mongodb.net/"

class AtlasCliente:
    def __init__(self, url, dbname):
        nombreusuario = input("Username: ")
        contrasena = getpass("Password: ")  
        updated_url = url.replace("<username>:<password>", f"{nombreusuario}:{contrasena}")
        
        self.mongodb_client = MongoClient(updated_url)
        try:
            self.mongodb_client.admin.command('ping')
            self.basededatos = self.mongodb_client[dbname]
            print("Authentication successful!")
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise
    def ping (self):
        self.mongodb_client.admin.command('ping')
    def ver_collecion (self, nombre_collecion):
        collection = self.database[nombre_collecion]
        return collection
    def find (self, nombre_collecion, filter = {} , limit=0) :
        collection = self.basededatos[nombre_collecion]
        items = list(collection.find(filter=filter, limit=limit))
        return items
Cliente1 = AtlasCliente(url,dbname="sample_flix")
