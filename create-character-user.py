import string
from pymongo import MongoClient


url = "mongodb+srv://GameMaster:qh20Fpw4QAeX0uhd@cluster0.rlqm0qg.mongodb.net/"
dbname='JuegodeRol'

class AtlasBase:  # Common base class for both types
    def __init__(self, url, dbname):
        self.mongodb_client = MongoClient(url)
        try:
            self.mongodb_client.admin.command('ping')
            self.basededatos = self.mongodb_client[dbname]
            print("Autenticacion Exitosa!")
        except Exception as e:
            print(f"nombre invalido: {e}")
            raise

    def ping(self):
        self.mongodb_client.admin.command('ping')

    def ver_collecion(self, nombre_collecion):  
        return self.basededatos[nombre_collecion]

    def find(self, nombre_collecion, filter={}, limit=0):
        collection = self.basededatos[nombre_collecion]
        return list(collection.find(filter=filter, limit=limit))
 

class FormularioCreacion(AtlasBase):
    def ObteneridJugador(self):
        pass
    def obtener_nombre(self):
        while True:
            nombre = input("Ingrese el nombre de su personaje: ")
            #la primera condicion de este if sirve para que el nombre ingresado no tenga
            #caracteres especiales como '_' , '+', '*' etc 
            if any(caracter in string.punctuation for caracter in nombre):
                print("No se permiten caracteres especiales.")
            else:
                print(f"El nombre '{nombre}' está correcto.")
                return nombre
    def obtener_raza(self):
        razadisponible = ['humano', 'elfo', 'semi elfo', 'enano', 'draconido', 'gnomo', 'mediano', 'semi orco', 'tiflin']
        while True:
            print("\nRazas Disponibles:")
            for raza in razadisponible:
                print(f"- {raza}") 
            raza = input("Ingrese el nombre de la raza que quiere: ").lower()
            if raza in razadisponible:
                print(f"Ha seleccionado la raza '{raza}'.")
                return raza
            else:
                print("Ingrese una raza válida.")
    def obtener_habilidades(self):
        equipamientodisponible = ['correr', 'reir', 'saltar', 'dormir', 'comer']
        habilidades_escogidas = []
        while len(habilidades_escogidas) < 2: #maximo de habilidades
            print("\nHabilidades Disponibles:")
            for habilidad in equipamientodisponible:
                print(f"- {habilidad}")
            habilidad = input(f"Ingrese el la habilidad número {len(habilidades_escogidas) + 1}: ").lower()
            if habilidad in equipamientodisponible and habilidad not in habilidades_escogidas:
                habilidades_escogidas.append(habilidad)
                print(f"Has escogido la habilidad '{habilidad}'.")
            else:
                print("Ingrese una habilidad válida y que no hayas escogido antes.")
        print(f"Estas son tus habilidades: {', '.join(habilidades_escogidas)}")  
        return habilidades_escogidas    
    def obtener_equipamiento(self):
        equipamientodisponible = ['casco de oro','casco de metal', 'peto de oro','peto de metal', 'pantalones', 'zapatos']
        equipamiento_escogidas = []
        while len(equipamiento_escogidas) < 1: #maximo de equipamiento
            print("\nEquipamientos Disponibles:")
            for equipameinto in equipamientodisponible:
                print(f"- {equipameinto}")
            equipameinto = input(f"Ingrese el equipamiento n{len(equipamiento_escogidas) + 1}: ").lower()
            if equipameinto in equipamientodisponible and equipameinto not in equipamiento_escogidas:
                equipamiento_escogidas.append(equipameinto)
                print(f"Has escogido un'{equipameinto}'.")
            else:
                print("Ingrese una habilidad válida y que no hayas escogido antes.")
        print(f"Estas son tus habilidades: {', '.join(equipamiento_escogidas)}")  
        return equipamiento_escogidas    
    def obtener_poderes(self):
        poderesdisponible = ['kamehameha','genkidama', 'bigban attack',]
        poderes_escogidos = []
        while len(poderes_escogidos) < 1: #maximo de poder
            print("\nPoderes Disponibles:")
            for poder in poderesdisponible:
                print(f"- {poder}")
            poder = input(f"Ingrese el poder n{len(poderes_escogidos) + 1}: ").lower()
            if poder in poderesdisponible and poder not in poderes_escogidos:
                poderes_escogidos.append(poder)
                print(f"Has escogido un'{poder}'.")
            else:
                print("Ingrese un poder válido y que no hayas escogido antes.")
        print(f"Estos son tus poderes: {', '.join(poderes_escogidos)}")  
        return poderes_escogidos
    def obtener_atributos(self):
        atributos = {
            "carisma": 0,
            "fuerza": 0,
            "salto": 0,
            "administracion": 0
        }
        puntos_mejora = 30

        while puntos_mejora > 0:
            print("\nValores actuales de los atributos:")
            for atributo, valor in atributos.items():
                print(f"{atributo} = {valor}")

            print(f"Puntos de mejora disponibles: {puntos_mejora}")
            atributo_a_mejorar = input("Ingrese el atributo a mejorar: ").lower()

            if atributo_a_mejorar not in atributos:
                print("Atributo inválido. Intente de nuevo.")
                continue

            while True:
                try:
                    puntos_a_asignar = int(input(f"Puntos a asignar a {atributo_a_mejorar}: "))
                    if 0 < puntos_a_asignar <= puntos_mejora:
                        atributos[atributo_a_mejorar] += puntos_a_asignar
                        puntos_mejora -= puntos_a_asignar
                        break
                    else:
                        print(f"Valor inválido. Debe ser entre 1 y {puntos_mejora}.")
                except ValueError:
                    print("Ingrese un número válido.")

        print("\nAsignación de atributos finalizada.")
        return atributos
    def DatosPersonaje(self):
        print("\n============================")
        print("Datos del Personaje:")
        print(f"Nombre: {self.nombre}")
        print(f"Raza: {self.raza}")
        print(f"Habilidades: {', '.join(self.habilidad)}")
        print(f"Equipamiento: {', '.join(self.equipamiento)}")
        print(f"Poderes: {', '.join(self.poder)}")
        print("Atributos:")
        for atributo, valor in self.atributos_disponibles.items():
            print(f"  - {atributo}: {valor}") 
        print("============================")
    def Guardar(self,obtener_nombre,obtener_raza,obtener_habilidades,obtener_equipamiento,obtener_poderes,obtener_atributos):
        coleccion = self.basededatos['Personaje']
        #Ingreso Nombre a Base de Datos
        datos_ingreso = {
            'Nombre':obtener_nombre,
            'Raza': obtener_raza,
            'Habilidades':obtener_habilidades,
            'Equipamiento': obtener_equipamiento,
            'Poderes':obtener_poderes,
            'Atributos':obtener_atributos
            }
        coleccion.insert_one(datos_ingreso)
        print("Datos Ingresados")
        
        

        
        


formulario1 = FormularioCreacion(url,dbname="JuegodeRol")
formulario1.Guardar(obtener_nombre='victor',obtener_raza='elfo',obtener_habilidades='reir',obtener_equipamiento='Espada de Diamante',obtener_poderes='Kamehameha',obtener_atributos='Administracion = 0')
