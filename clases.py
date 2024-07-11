from pymongo import MongoClient
from getpass import getpass
url = "mongodb+srv://<username>:<password>@cluster0.rlqm0qg.mongodb.net/"

class AtlasBase:  # Common base class for both types
    def __init__(self, url, dbname):
        print(f"┌────────────────────────────┐\n│ {'🧙‍♂️ Benvenuto, ' + self.__class__.__name__ + ' ⚔️'} │\n└────────────────────────────┘")

        Nombredeusuario = input("Nombre De Usuario: ")
        contraseña = getpass("contraseña: ")
        updated_url = url.replace("<username>:<password>", f"{Nombredeusuario}:{contraseña}")

        self.mongodb_client = MongoClient(updated_url)
        try:
            self.mongodb_client.admin.command('ping')
            self.basededatos = self.mongodb_client[dbname]
            print("Autenticacion Exitosa!")
        except Exception as e:
            print(f"Eres gay: {e}")
            raise

    def ping(self):
        self.mongodb_client.admin.command('ping')

    def ver_collecion(self, nombre_collecion):  
        return self.basededatos[nombre_collecion]

    def find(self, nombre_collecion, filter={}, limit=0):
        collection = self.basededatos[nombre_collecion]
        return list(collection.find(filter=filter, limit=limit))
    
class AtlasCliente(AtlasBase):
    pass

class AtlasGameMaster(AtlasBase):
    def AgregarEstado(self):
        coleccion = self.basededatos['Estados']
        while True: 
            print("Si desea agregar un estado, ingrese primero el nombre y descripcion del estado.")
            nombre = input("Ingrese el nombre: ")
            descripcion = input("Ingrese la descripción: ")
            
            datos_ingreso = {'Nombre': nombre, 'Descripcion': descripcion}
            result = coleccion.insert_one(datos_ingreso)  # Store the result of the insert operation
            print(f"Estado agregado con ID: {result.inserted_id}")
            continuar = input("¿Desea agregar otro estado? (s/n): ")
            if continuar.lower() != 's':
                break
    def AgregarPoder(self):
        collecion = self.basededatos['Razas']
        razas = list(collecion.find({},{"Nombre":1}))
        coleccion = self.basededatos['Poderes']
        while True: 
            print("Si desea agregar un estado, ingrese primero el nombre y descripcion del estado.")
            nombre = input("Ingrese el nombre: ")
            descripcion = input("Ingrese la descripción: ")
            
            print("\nRazas disponibles:")
            for i, raza in enumerate(razas):
                print(f"{i+1}. {raza['Nombre']}")
            
            while True: 
                try:
                    eleccion_raza = int(input("Elija la raza a la que pertenece el poder (o 0 si no aplica): ")) - 1
                    if 0 <= eleccion_raza < len(razas) or eleccion_raza == -1:
                        break  
                    else:
                        print("Opción inválida. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número.")
            datos_ingreso = {'Nombre': nombre, 'Descripcion': descripcion}
            if eleccion_raza != -1:  
                datos_ingreso['Raza'] = razas[eleccion_raza]['_id'] 
    
            resultado = coleccion.insert_one(datos_ingreso)
            print(f"Poder agregado con ID: {resultado.inserted_id}")

            continuar = input("¿Desea agregar otro poder? (s/n): ")
            if continuar.lower() != 's':
                break
    def AgregarHabilidades(self):
        collecion = self.basededatos['Razas']
        razas = list(collecion.find({},{"Nombre":1}))
        coleccion = self.basededatos['Habilidades']
        while True: 
            print("Si desea agregar una habilidad, ingrese primero el nombre y descripcion de la habilidad.")
            nombre = input("Ingrese el nombre: ")
            descripcion = input("Ingrese la descripción: ")
            
            print("\nRazas disponibles:")
            for i, raza in enumerate(razas):
                print(f"{i+1}. {raza['Nombre']}")
            
            while True: 
                try:
                    eleccion_raza = int(input("Elija la raza a la que pertenece el poder (o 0 si no aplica): ")) - 1
                    if 0 <= eleccion_raza < len(razas) or eleccion_raza == -1:
                        break  
                    else:
                        print("Opción inválida. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número.")
            datos_ingreso = {'Nombre': nombre, 'Descripcion': descripcion}
            if eleccion_raza != -1:  
                datos_ingreso['Raza'] = razas[eleccion_raza]['_id'] 
    
            resultado = coleccion.insert_one(datos_ingreso)
            print(f"Poder agregado con ID: {resultado.inserted_id}")

            continuar = input("¿Desea agregar otro poder? (s/n): ")
            if continuar.lower() != 's':
                break
    def AgregarEquipamiento(self):
        collecion = self.basededatos['Razas']
        razas = list(collecion.find({},{"Nombre":1}))
        coleccion = self.basededatos['Equipamiento']
        while True: 
            print("Si desea agregar equipamiento, ingrese primero el nombre y descripcion del estado.")
            nombre = input("Ingrese el nombre: ")
            descripcion = input("Ingrese la descripción: ")
            Ranuras = []
            Slots_disponibles=['Mano Derecha','Brazo Derecho','Mano Izquierda',
                                'Brazo Izquierdo','Pie Derecho','Rodilla Derecha','Pie Izquierdo','Rodilla Izquierda',
                                'Pecho','Cara','Cabeza']
            while True:
                for i,Slots_disponibles in enumerate(Slots_disponibles):
                    print(f"{i+1}, {Slots_disponibles}")
                    break;

            
            print("\nRazas disponibles:")
            for i, raza in enumerate(razas):
                print(f"{i+1}. {raza['Nombre']}")
            
            while True: 
                try:
                    eleccion_raza = int(input("Elija la raza a la que pertenece el poder (o 0 si no aplica): ")) - 1
                    if 0 <= eleccion_raza < len(razas) or eleccion_raza == -1:
                        break  
                    else:
                        print("Opción inválida. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número.")
            datos_ingreso = {'Nombre': nombre, 'Descripcion': descripcion}
            if eleccion_raza != -1:  
                datos_ingreso['Raza'] = razas[eleccion_raza]['_id'] 
    
            resultado = coleccion.insert_one(datos_ingreso)
            print(f"Poder agregado con ID: {resultado.inserted_id}")

            continuar = input("¿Desea agregar otro poder? (s/n): ")
            if continuar.lower() != 's':
                break

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
                self.user = AtlasCliente(url, dbname="sample_flix")  #
                break
            elif tipo_cuenta == "2":
                self.user = AtlasGameMaster(url, dbname="JuegodeRol")  
                break  
            else:
                print("Opción inválida. Intenta de nuevo.")
      
GameMaster1 = TypeAccount()
GameMaster1.user.AgregarEquipamiento()