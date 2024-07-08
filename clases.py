from pymongo import MongoClient
from getpass import getpass
url = "mongodb+srv://<username>:<password>@cluster0.rlqm0qg.mongodb.net/"

class TypeAccount:
    def __init__(self):
        print("┌────────────────────────────┐")
        print("│ 🧙‍♂️ Prototipo Juego Rol  ⚔️ │")
        print("└────────────────────────────┘")
        while True:
            print("Iniciar Sesión como:")
            print("1. Jugador")
            print("2. GameMaster")
            tipo_cuenta = input("Elige una opción (1 o 2): ")

            if tipo_cuenta == "1":
                AtlasCliente(url, dbname="sample_flix")
                break
            elif tipo_cuenta == "2":
                AtlasGameMaster(url, dbname="sample_flix")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")  

class AtlasCliente:
    def __init__(self, url, dbname):
        print("┌────────────────────────────┐")
        print("│  🧙‍♂️ Welcome, Player     ⚔️ │")
        print("└────────────────────────────┘")

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


class AtlasGameMaster:
    def __init__(self, url, dbname):
        print("┌────────────────────────────┐")
        print("│  🧙‍♂️ Welcome, GameMaster ⚔️ │")
        print("└────────────────────────────┘")

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
