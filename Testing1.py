# Ojala funcione esto
from pymongo import MongoClient
url = "mongodb+srv://GameMaster:qh20Fpw4QAeX0uhd@cluster0.rlqm0qg.mongodb.net/"
class AtlasCliente ():
    def __init__(self, atlasurl,dbname) :
        self.mongodb_client = MongoClient(atlasurl)
        self.basededatos = self.mongodb_client[dbname]
    def ping (self):
        self.mongodb_client.admin.command('ping')
    def ver_collecion (self, nombre_collecion):
        collection = self.database[nombre_collecion]
        return collection
    def find (self, nombre_collecion, filter = {} , limit=0) :
        collection = self.basededatos[nombre_collecion]
        items = list(collection.find(filter=filter, limit=limit))
        return items
Nombre_BaseDatos = 'sample_mflix'
Nombre_collecion = 'embedded_movies'
Cliente1 = AtlasCliente(url, Nombre_BaseDatos)
Cliente1.ping()

movies = Cliente1.find (nombre_collecion=Nombre_collecion, limit=5)
print (f"Found {len (movies)} movies")