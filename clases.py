from pymongo import MongoClient
from getpass import getpass
import string
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
            print(f"nombre invalido: {e}")
            raise

    def ping(self):
        self.mongodb_client.admin.command('ping')

    def ver_collecion(self, nombre_collecion):  
        return self.basededatos[nombre_collecion]

    def find(self, nombre_collecion, filter={}, limit=0):
        collection = self.basededatos[nombre_collecion]
        return list(collection.find(filter=filter, limit=limit))
    
class AtlasCliente(AtlasBase):
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

        collecion = self.basededatos['Equipamiento']  # Corrección: Usar la colección de equipamiento
        self.equipamiento_personaje = {
            "Cabeza": "",
            "Mano Izquierda": "",
            "Mano Derecha": "",
            "Torso": "",
            "Piernas": "",
            "Pies": ""
        }

        while True:
            print("Si desea agregar equipamiento, ingrese primero el nombre y descripcion del Equipamiento.")
            nombre = input("Ingrese el nombre: ")
            descripcion = input("Ingrese la descripción: ")
            Ranura = ""
            Terminado = False
    
            while True:
                print("┌────────────────────────────┐")
                print("│          Ranuras           │")
                print("└────────────────────────────┘")
                print("          |  O                ")
                print("          +--|---|            ")
                print("             |   |            ")
                print("            / \\              ")
                print("          _/   \\_             ")
    
                equipamiento_mod = list(self.equipamiento_personaje.keys())
                for i, equipameinto in enumerate(equipamiento_mod):
                    print(f"{i+1}. {equipameinto}")
    
                while Terminado == False:
                    try:
                        destino = int(input("En que ranura desea agregar el equipamiento? (Escribe un número): ")) - 1
                        if 0 <= destino < len(equipamiento_mod):
                            Ranura = equipamiento_mod[destino]
                            print(Ranura)
                            Terminado = True
                        else:
                            print("Número inválido. Inténtalo de nuevo.")
                    except ValueError:
                        print("Ingresa un número válido.")
    
                datos_ingreso = {"Nombre": nombre, "Descripcion": descripcion, "Ranura": Ranura}
                resultado = collecion.insert_one(datos_ingreso)
                print(f"Datos Ingresado con ID {resultado.inserted_id}")
                break
    
    
            continuar = input("¿Desea agregar otro Equipamiento? (s/n): ")
            if continuar.lower() != 's':
                break
    def AgregarRaza(self):
        coleccion = self.basededatos['Razas']
        while True:
            print("Ingrese Nombre y Descripcion de la Raza que va a ingresar")
            nombre = input("Nombre:")
            Descripcion = input("Descripcion:")

            datos_ingreso = {'Nombre': nombre, 'Descripcion': Descripcion}
            resultado = coleccion.insert_one(datos_ingreso)
            print(f"Estado Ingresado con la Siguiente ID: {resultado.inserted_id}")
            continuar = input("¿Desea agregar otro estado? (s/n): ")
            if continuar.lower() !='s':
                break
    def Modificar(self, Objeto):
        match Objeto:
            case "Estado":
                coleccion = self.basededatos["Estados"]
                Estados = list(coleccion.find({}, {"_id": 1, "Nombre": 1}))
    
                print("Estados Existentes: (Seleccione el numero que va a modificar)")
                for i, estado in enumerate(Estados):
                    print(f"{i+1}. {estado['Nombre']}")
    
                while True:
                    try:
                        eleccion_estado = int(input()) - 1
                        if 0 <= eleccion_estado < len(Estados):  
                            estado_seleccionado = Estados[eleccion_estado]  # Get the entire state document
                            id_estado = estado_seleccionado["_id"]
                            break
                        else:
                            print("Opción inválida. Por favor, elija un número de la lista.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
    
                Decision = input("Desea modificar \n1). Nombre \n 2). Descripcion \n 3).Ambos?")
                if Decision == '3':  # Use string comparison for input
                    nuevonombre = input("Nuevo Nombre: ")
                    nuevadescripcion = input("Nueva Descripcion: ")
                    resultado = coleccion.update_one({"_id": id_estado},
                                                     {"$set": {"Nombre": nuevonombre, "Descripcion": nuevadescripcion}})
                    print("Estado Actualizado")
                elif Decision == '2': 
                    nuevadescripcion = input("Nueva Descripcion: ")
                    resultado = coleccion.update_one({"_id": id_estado},
                                 {"$set": {"Descripcion": nuevadescripcion}})
                    print("Estado Actualizado")
                elif Decision == '1':
                    nuevonombre = input("Nuevo Nombre: ")
                    resultado = coleccion.update_one({"_id":id_estado}, {"set" : {"Nombre": nuevonombre}})
                    print("Estado Actualizado")

            case "Poder":
                coleccion = self.basededatos["Razas"]
                razas = list(coleccion.find({},{"Nombre":1}))
                collecion = self.basededatos["Poderes"]
                Poderes = list(collecion.find({},{"_id":1,"Nombre": 1}))
                print("Poderes Existentes: (Seleccione el numero que va a modificar)")
                for i, poder in enumerate(Poderes):
                    print(f"{i+1}. {poder['Nombre']}")
                while True:
                    try:
                        eleccion_poder = int(input()) -1
                        if 0 <= eleccion_poder < len(Poderes):
                            poder_seleccionado = Poderes[eleccion_poder]
                            id_poder = poder_seleccionado["_id"]
                            break
                        else: 
                            print("Eleccion Invalida, por favor elija un poder valido ")
                    except ValueError:
                        print("Por favor, ingrese un numero valido")
                Decision = input("Desea modificar  \n 1).Nombre \n 2.) Descripcion 3). Raza 4) Todo? ")
                if Decision == "4":
                    nuevonombre = input("Ingrese el nuevo Nombre:")
                    nuevadescripcion = input("Ingrese la nueva descripcion")
                    for i, raza in enumerate(razas):
                        print(f"{i+1}. {raza['Nombre']}")
                    
                    while True: 
                        try:
                            eleccion_raza = int(input("Elija la raza a la que va a pertenecer el poder")) - 1
                            if 0 <= eleccion_raza < len(razas) or eleccion_raza == -1:
                                break  
                            else:
                                print("Opción inválida. Intente de nuevo.")
                        except ValueError:
                            print("Por favor, ingrese un número.")
                    
                    resultado = collecion.update_one({"_id":id_poder}, {"$set": {"Nombre": nuevonombre, "Descripcion": nuevadescripcion,"Raza": razas[eleccion_raza]['_id'] }})
                    print("Poder Actualizado:")
                elif Decision == "3":
                    for i, raza in enumerate(razas):
                        print(f"{i+1}. {raza['Nombre']}")
                    
                        while True: 
                            try:
                                eleccion_raza = int(input("Elija la raza a la que va a pertenecer el poder")) - 1
                                if 0 <= eleccion_raza < len(razas) or eleccion_raza == -1:
                                    break  
                                else:
                                    print("Opción inválida. Intente de nuevo.")
                            except ValueError:
                                print("Por favor, ingrese un número.")
                    resultado = collecion.update_one({"_id": id_poder}, {"$set" : {"Raza" : razas[eleccion_raza]['_id']} })
                elif Decision == '2':
                    nuevadescripcion = input("Ingrese la nueva Descripcion: ")
                    resultado = collecion.update_one({"_id": id_poder}, {"$set": {"Descripcion" : nuevadescripcion} })
                    print("Poder Actualizado")
                elif Decision == '1':
                    nuevonombre = input("Ingrese el nombre: ")
                    resultado = collecion.update_one({"_id" : id_poder}, {'$set' : {"Nombre" : nuevonombre} } )
                    print("Poder Actualizado")




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
GameMaster1.user.Modificar("Poder")