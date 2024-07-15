from pymongo import MongoClient
from getpass import getpass
import bcrypt
import string
from bson.binary import Binary
from bson.objectid import ObjectId
url = "mongodb+srv://<username>:<password>@cluster0.rlqm0qg.mongodb.net/"
url1 = "mongodb+srv://JugadoresPorFavorFunciona:4fmRjvvCxji3QllQ@cluster0.rlqm0qg.mongodb.net/"
class AtlasBase:  # Common base class for both types
    def __init__(self, url, dbname):
        print(f"┌────────────────────────────┐\n│ {'🧙‍♂️ Benvenuto, ' + self.__class__.__name__ + ' ⚔️'} │\n└────────────────────────────┘")
        if url != url1:
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
        else:
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
    
class AtlasCliente(AtlasBase):
    Id_Usuario = ""
    Nombre_usuario=""
    def login(self):
        coleccion = self.basededatos["Cuenta-User"]

        print("Ingrese su Nombre de Usuario Y Contraseña")
        usuario = input("Ingrese su nombre de Usuario: ")
        contraseña = getpass("Ingrese su contraseña: ")

        # Obtener documento segun el Nombre del Usuario
        user_document = coleccion.find_one({"Nombre": usuario}) 
        if user_document:
            # Recuperar la contraseña hasheada en (BSON binary)
            stored_hashed_password_binary = user_document["contraseña"]
            # Comparar las contraseñas.
            if bcrypt.checkpw(contraseña.encode(), stored_hashed_password_binary):
                self.Id_Usuario = ObjectId(user_document["_id"])
                self.Id_Usuario = ObjectId(self.Id_Usuario)
                
                self.Nombre_usuario = usuario
                print(self.Id_Usuario)
                print("Autenticación exitosa como Jugador")
                return 
            else:
                print("Contraseña incorrecta")
                exit
        else:
            print("Usuario no encontrado")   
    def FichasPersonajes(self):
        coleccion = self.basededatos["Personajes"]
        Personajes = list(coleccion.find({"ID_Jugador": self.Id_Usuario} ,{"Nombre": 1}))
        print("Sus Personajes: ")
        for i,personaje in enumerate(Personajes):
            print(f"{i+1}. {personaje["Nombre"]}")
        while True:
            try:
                eleccion_personaje = int(input("Elija un poder: ")) - 1
                if 0 <= eleccion_personaje < len(Personajes):
                    personaje_seleccionado = Personajes[eleccion_personaje]
                    id_personaje = personaje_seleccionado["_id"]
                    self.VerFichasPersonajes(id_personaje)
                    break
                else:
                    print("Elección inválida. Por favor elija un personaje válido.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
            self.VerFichasPersonajes(id_personaje)

    def obtener_nombres_por_ids(self, nombre_coleccion, lista_ids):
        if isinstance(lista_ids, ObjectId):  # Revisar si es una instancia de ObjectId
            lista_ids = [lista_ids]  # convertir a la lista
        elif isinstance(lista_ids, str):  # Revisar si es una string
            lista_ids = [ObjectId(lista_ids)]  # Convertir la string a object id para la lista
        else:  
            lista_ids = [ObjectId(id) for id in lista_ids]  # Convertir toda las ids en la lista a ObjectId
        coleccion = self.basededatos[nombre_coleccion]
        resultado = coleccion.find({"_id": {"$in": lista_ids}}, {"Nombre": 1})  # query para conseguir el nombre correspondiente
        return {str(r["_id"]): r["Nombre"] for r in resultado}

    def reemplazar_ids_por_nombres(self, documento, mapeo_ids_a_nombres):
        for clave, valor in documento.items():
            if isinstance(valor, str) and ObjectId.is_valid(valor):  # Revisar por string validas 
                documento[clave] = mapeo_ids_a_nombres.get(valor, valor)  # Reemplazar por si es valida
            elif isinstance(valor, list):
                documento[clave] = [self.reemplazar_ids_por_nombres(item, mapeo_ids_a_nombres) if isinstance(item, dict) else
                                    mapeo_ids_a_nombres.get(item, item) if ObjectId.is_valid(item) else item for item in valor]
            elif isinstance(valor, dict):
                documento[clave] = self.reemplazar_ids_por_nombres(valor, mapeo_ids_a_nombres)
        return documento


    def VerFichasPersonajes(self, id_personaje):
        coleccion = self.basededatos["Personajes"]
        personaje = coleccion.find_one({"_id": id_personaje}, {"_id": 0})

        # Mapeos de IDs a nombres
        mapeo_razas = self.obtener_nombres_por_ids("Razas", personaje["Raza"])
        mapeo_estados = self.obtener_nombres_por_ids("Estados", personaje["Estado_ID"])
        mapeo_habilidades = self.obtener_nombres_por_ids("Habilidades", personaje["Habilidad_ID"])
        mapeo_equipamiento = self.obtener_nombres_por_ids("Equipamiento", personaje["Equipamiento_ID"])
        mapeo_poderes = self.obtener_nombres_por_ids("Poderes", personaje["Poderes_ID"])
        # Unir todos los mapeos en uno solo
        mapeo_ids_a_nombres = {**mapeo_estados, **mapeo_habilidades, **mapeo_equipamiento, **mapeo_poderes, **mapeo_razas}

        # Reemplazar IDs en el personaje
        personaje_con_nombres = self.reemplazar_ids_por_nombres(personaje, mapeo_ids_a_nombres)

        # Imprimir el personaje con los nombres
        for clave, valor in personaje_con_nombres.items():
            if isinstance(valor, list) and valor:
                print(f"{clave}:")
                for item in valor:
                    print(f"  - {item}")
            else:
                print(f"{clave}: {valor}")
    def ModificarEquipamiento(self):
        coleccion_personajes = self.basededatos["Personajes"]
        coleccion_equipamiento = self.basededatos["Equipamiento"]
    
        # Mostrar la lista de personajes a elegir
        Personajes = list(coleccion_personajes.find({"ID_Jugador": self.Id_Usuario}, {"Nombre": 1, "Equipamiento_ID": 1}))
        print("Sus Personajes:")
        for i, personaje in enumerate(Personajes):
            print(f"{i+1}. {personaje['Nombre']}")
    
        while True:
            try:
                eleccion_personaje = int(input("Elija un personaje: ")) - 1
                if 0 <= eleccion_personaje < len(Personajes):
                    personaje_seleccionado = Personajes[eleccion_personaje]
                    id_personaje = personaje_seleccionado["_id"]
                    break
                else:
                    print("Elección inválida. Por favor elija un personaje válido.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        equipamiento_actual = personaje_seleccionado.get("Equipamiento_ID", [])
        # Decision para equipar o Desequipar
        while True:
            decision = input("\n¿Qué desea hacer?\n1. Equipar\n2. Desequipar\n")
            if decision in ["1", "2"]:
                break
            else:
                print("Opción inválida. Elija 1 para equipar o 2 para desequipar.")
    
        if decision == "1":  # Equip
            # Filtro para excluir equipamiento ya equipado
            lista_equipamiento = list(coleccion_equipamiento.find(
                {"_id": {"$nin": [ObjectId(equip_id) for equip_id in equipamiento_actual]}},  
                {"Nombre": 1}
            ))
    
            if not lista_equipamiento:
                print("No hay más equipamiento disponible para equipar.")
            else:
                print("\nEquipamiento disponible:")
                for i, equip in enumerate(lista_equipamiento):
                    print(f"{i+1}. {equip['Nombre']}")
    
                while True:
                    try:
                        eleccion_equipamiento = int(input("Elija un equipamiento: ")) - 1
                        if 0 <= eleccion_equipamiento < len(lista_equipamiento):
                            equipamiento_seleccionado = lista_equipamiento[eleccion_equipamiento]
                            id_equipamiento = str(equipamiento_seleccionado["_id"])
                            equipamiento_actual.append(id_equipamiento)
                            break
                        else:
                            print("Elección inválida. Por favor elija un equipamiento válido.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
        elif decision == "2":  # Unequip
            # Mostrar equipamiento ya equipado
            if not equipamiento_actual:
                print("El personaje no tiene ningún equipamiento.")
            else:
                nombres_equipamiento = self.obtener_nombres_por_ids("Equipamiento", equipamiento_actual)
                print("\nEquipamiento del personaje:")
                for i, equip_id in enumerate(equipamiento_actual):
                    print(f"{i+1}. {nombres_equipamiento.get(equip_id, equip_id)}")
    
                while True:
                    try:
                        eleccion_desequipar = int(input("Elija un equipamiento para desequipar: ")) - 1
                        if 0 <= eleccion_desequipar < len(equipamiento_actual):
                            equipamiento_actual.pop(eleccion_desequipar)  # Remover equipamiento ya ocupado
                            break
                        else:
                            print("Elección inválida. Por favor elija un equipamiento válido.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
    
               # Update la coleccion
        coleccion_personajes.update_one(
            {"_id": id_personaje},
            {"$set": {"Equipamiento_ID": equipamiento_actual}}
        )
        print("Equipamiento modificado con éxito.")
        
    def CrearPersonaje(self):
        coleccion_personajes = self.basededatos["Personajes"]
        coleccion_razas = self.basededatos["Razas"]
        coleccion_equipamiento = self.basededatos["Equipamiento"]
        coleccion_poderes = self.basededatos["Poderes"]
        coleccion_habilidades = self.basededatos["Habilidades"]
        lista_razas = list(coleccion_razas.find({}, {"Nombre": 1}))
        lista_equipamiento = list(coleccion_equipamiento.find({}, {"Nombre": 1}))

        while True:
            nombre = input("Ingrese el nombre del Personaje: ")
            #la primera condicion de este if sirve para que el nombre ingresado no tenga
            #caracteres especiales como '_' , '+', '*' etc 
            if any(caracter in string.punctuation for caracter in nombre):
                print("No se permiten caracteres especiales.")
            else:
                print(f"El nombre '{nombre}' está correcto.")
                break
    
        print("\nRazas disponibles:")
        for i, raza in enumerate(lista_razas):
            print(f"{i+1}. {raza['Nombre']}")
    
        while True:
            try:
                eleccion_raza = int(input("Elija la raza a la que va a pertenecer su personaje: ")) - 1
                if 0 <= eleccion_raza < len(lista_razas) or eleccion_raza == -1:
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    
        # Conseguir id de la raza
        id_raza_seleccionada = lista_razas[eleccion_raza]["_id"]
    
        # Hacer Query para filtrar habilidades y poderes segun la raza seleccionada
        filtro_habilidades = (
            {"$or": [{"Raza": id_raza_seleccionada}, {"Raza": {"$exists": False}}]}
            if id_raza_seleccionada
            else {}
        )
        filtro_poderes = (
            {"$or": [{"Raza": id_raza_seleccionada}, {"Raza": {"$exists": False}}]}
            if id_raza_seleccionada
            else {}
        )
    
        lista_poderes = list(coleccion_poderes.find(filtro_poderes, {"Nombre": 1}))
        lista_habilidades = list(coleccion_habilidades.find(filtro_habilidades, {"Nombre": 1}))
    
        # Mostrar Poderes
        print("\nPoderes disponibles:")
        for i, poder in enumerate(lista_poderes):
            print(f"{i+1}. {poder['Nombre']}")
    
        while True:
            try:
                eleccion_poder = int(input("Elija un poder: ")) - 1
                if 0 <= eleccion_poder < len(lista_poderes):
                    poder_seleccionado = lista_poderes[eleccion_poder]
                    id_poder = poder_seleccionado["_id"]
                    break
                else:
                    print("Elección inválida. Por favor elija un poder válido.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    
        # Visualizacion y seleccion de habilidades
        print("\nHabilidades disponibles:")
        for i, habilidad in enumerate(lista_habilidades):
            print(f"{i+1}. {habilidad['Nombre']}")
    
        habilidades_seleccionadas = []  # Lista para almacenar las habilidades

        print("\nHabilidades disponibles:")
        for i in range(2):  # For loop para elegir 2 habilidades
            for j, habilidad in enumerate(lista_habilidades):
                print(f"{j+1}. {habilidad['Nombre']}")
    
            while True:
                try:
                    eleccion_habilidad = int(input("Elija una habilidad: ")) - 1
                    if 0 <= eleccion_habilidad < len(lista_habilidades):
                        habilidades_seleccionadas.append(lista_habilidades.pop(eleccion_habilidad))  
                        break
                    else:
                        print("Elección inválida. Por favor elija una habilidad válida.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
    
            if i == 0:
                print("\nHabilidad seleccionada. Elija otra habilidad:")
            else:
                print("\nSegunda habilidad seleccionada.")
    
        id_habilidades = [habilidad["_id"] for habilidad in habilidades_seleccionadas]
        print("\nEquipamiento Disponible: ")

                    
        for i, equipamiento in enumerate(lista_equipamiento):
            print(f"{i+1}. {equipamiento['Nombre']}")
        while True:
            try:
                eleccion_equipamiento = int(input()) -1
                if 0 <= eleccion_equipamiento < len(lista_equipamiento):
                    equipamiento_seleccionado = lista_equipamiento[eleccion_equipamiento]
                    id_equipamiento = equipamiento_seleccionado["_id"]
                    break
                else: 
                    print("Eleccion Invalida, por favor elija una habilidad valida ")
            except ValueError:
                print("Por favor, ingrese un numero valido")
        
        puntos_disponibles = 10
        atributos = {"STR": 0, "DEX": 0, "CON": 0, "WIS": 0, "INT": 0, "CHA": 0}
    
        print("\nDistribución de Atributos (10 puntos disponibles):")
        while puntos_disponibles > 0:
            print("\nPuntos restantes:", puntos_disponibles)
            for atributo, valor in atributos.items():
                print(f"{atributo}: {valor}")
    
            while True:
                try:
                    atributo_elegido = input("Elija un atributo para aumentar (o 'listo' para terminar): ").upper()
                    if atributo_elegido == 'LISTO' and all(valor > 0 for valor in atributos.values()):  # ver si todos los atributos tienen almenos un punto
                        break
                    elif atributo_elegido in atributos:
                        puntos_a_asignar = int(input("¿Cuántos puntos desea asignar? "))
                        if 1 <= puntos_a_asignar <= puntos_disponibles:
                            atributos[atributo_elegido] += puntos_a_asignar
                            puntos_disponibles -= puntos_a_asignar
                            break
                        else:
                            print(f"Puntos inválidos. Debe asignar entre 1 y {puntos_disponibles} puntos.")
                    else:
                        print("Atributo inválido. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
    
        # Insertar personaje en la Base de Datos
        datos_ingreso = {
            "Nombre": nombre,
            "ID_Jugador": self.Id_Usuario,
            "Nombre_Jugador": self.Nombre_usuario,
            "HitPoints": 10,
            "Raza": str(id_raza_seleccionada) if id_raza_seleccionada else None,
            "Nivel": 1,
            "Estado_ID": "6694921ac4c85e562c0522d0",
            "Habilidad_ID": [str(id) for id in id_habilidades],
            "Equipamiento_ID": [str(id_equipamiento)],
            "Poderes_ID": [str(id_poder)],
            "Atributos": atributos  # Include the attributes in the insert
        }
        coleccion_personajes.insert_one(datos_ingreso)
        print("¡Personaje creado con éxito!")
 




class AtlasGameMaster(AtlasBase):
    def AgregarEstado(self):
        coleccion = self.basededatos['Estados']
        while True: 
            print("Si desea agregar un estado, ingrese primero el nombre y descripcion del estado.")
            while True:
                nombre = input("Ingrese el nombre: ")
                if any(caracter in string.punctuation for caracter in nombre):
                    print("No se permiten caracteres especiales.")
                else:
                    print(f"El nombre '{nombre}' está correcto.")
                    break
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
            while True:
                nombre = input("Ingrese el nombre: ")
                if any(caracter in string.punctuation for caracter in nombre):
                    print("No se permiten caracteres especiales.")
                else:
                    print(f"El nombre '{nombre}' está correcto.")
                    break
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
            while True:
                nombre = input("Ingrese el nombre: ")
                if any(caracter in string.punctuation for caracter in nombre):
                    print("No se permiten caracteres especiales.")
                else:
                    print(f"El nombre '{nombre}' está correcto.")
                    break
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
            while True:
                nombre = input("Ingrese el nombre: ")
                if any(caracter in string.punctuation for caracter in nombre):
                    print("No se permiten caracteres especiales.")
                else:
                    print(f"El nombre '{nombre}' está correcto.")
                    break
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
            while True:
                nombre = input("Ingrese el nombre: ")
                if any(caracter in string.punctuation for caracter in nombre):
                    print("No se permiten caracteres especiales.")
                else:
                    print(f"El nombre '{nombre}' está correcto.")
                    break
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
                        eleccion_estado = int(input("Que desea modificar:")) - 1
                        if 0 <= eleccion_estado < len(Estados):  
                            estado_seleccionado = Estados[eleccion_estado]  # Get the entire state document
                            id_estado = estado_seleccionado["_id"]
                            break
                        else:
                            print("Opción inválida. Por favor, elija un número de la lista.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                while True:
                    Decision = input("Desea modificar \n1. Nombre \n2. Descripcion \n3. Ambos?\nQue desea modificar?: ")
                    if Decision == '3':  # Use string comparison for input
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
                        nuevadescripcion = input("Nueva Descripcion: ")
                        resultado = coleccion.update_one({"_id": id_estado},
                                                        {"$set": {"Nombre": nuevonombre, "Descripcion": nuevadescripcion}})
                        print("Estado Actualizado")
                        break
                    elif Decision == '2': 
                        nuevadescripcion = input("Nueva Descripcion: ")
                        resultado = coleccion.update_one({"_id": id_estado},
                                    {"$set": {"Descripcion": nuevadescripcion}})
                        print("Estado Actualizado")
                        break
                    elif Decision == '1':
                        nuevonombre = input("Nuevo Nombre: ")
                        resultado = coleccion.update_one({"_id":id_estado}, {"set" : {"Nombre": nuevonombre}})
                        print("Estado Actualizado")
                        break
                    else:
                        print("Ingrese un numero valido (1,2,3)")

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
                while True:
                    Decision = input("Desea modificar  \n1. Nombre \n2. Descripcion \n3. Raza \n4. Todo? \n Que desea modificar?: ")
                    if Decision == "4":
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
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
                        break
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
                        break
                    elif Decision == '2':
                        nuevadescripcion = input("Ingrese la nueva Descripcion: ")
                        resultado = collecion.update_one({"_id": id_poder}, {"$set": {"Descripcion" : nuevadescripcion} })
                        print("Poder Actualizado")
                        break
                    elif Decision == '1':
                        nuevonombre = input("Ingrese el nombre: ")
                        resultado = collecion.update_one({"_id" : id_poder}, {'$set' : {"Nombre" : nuevonombre} } )
                        print("Poder Actualizado")
                        break
                    else:
                        print("Ingrese un Numero Valido")

            case "Habilidades":
                coleccion = self.basededatos["Razas"]
                razas = list(coleccion.find({},{"Nombre":1}))
                collecion = self.basededatos["Habilidades"]
                Habilidades = list(collecion.find({},{"_id":1,"Nombre": 1}))
                print("Habilidades Existentes: (Seleccione el numero que va a modificar)")
                for i, habilidad in enumerate(Habilidades):
                    print(f"{i+1}. {habilidad['Nombre']}")
                while True:
                    try:
                        eleccion_habilidad = int(input()) -1
                        if 0 <= eleccion_habilidad < len(Habilidades):
                            habilidad_seleccionada = Habilidades[eleccion_habilidad]
                            id_habilidad = habilidad_seleccionada["_id"]
                            break
                        else: 
                            print("Eleccion Invalida, por favor elija una habilidad valida ")
                    except ValueError:
                        print("Por favor, ingrese un numero valido")
                while True:
                    Decision = input("Desea modificar  \n 1. Nombre \n 2. Descripcion 3. Raza 4. Todo? \nQue desea modificar?: ")
                    if Decision == "4":
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
                        nuevadescripcion = input("Ingrese la nueva descripcion")
                        for i, raza in enumerate(razas):
                            print(f"{i+1}. {raza['Nombre']}")
                        
                        while True: 
                            try:
                                eleccion_raza = int(input("Elija la raza a la que va a pertenecer la habilidad")) - 1
                                if 0 <= eleccion_raza < len(razas) or eleccion_raza == -1:
                                    break  
                                else:
                                    print("Opción inválida. Intente de nuevo.")
                            except ValueError:
                                print("Por favor, ingrese un número.")
                        
                        resultado = collecion.update_one({"_id":id_habilidad}, {"$set": {"Nombre": nuevonombre, "Descripcion": nuevadescripcion,"Raza": razas[eleccion_raza]['_id'] }})
                        print("Habilidad Actualizada:")
                        break
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
                        resultado = collecion.update_one({"_id": id_habilidad}, {"$set" : {"Raza" : razas[eleccion_raza]['_id']} })
                        break
                    elif Decision == '2':
                        nuevadescripcion = input("Ingrese la nueva Descripcion: ")
                        resultado = collecion.update_one({"_id": id_habilidad}, {"$set": {"Descripcion" : nuevadescripcion} })
                        print("Habilidad Actualizada")
                        break
                    elif Decision == '1':
                        nuevonombre = input("Ingrese el nombre: ")
                        resultado = collecion.update_one({"_id" : id_habilidad}, {'$set' : {"Nombre" : nuevonombre} } )
                        print("Habilidad Actualizada")
                        break
                    else:
                        print("Ingrese un numero valido")

            case "Razas":
                coleccion = self.basededatos["Razas"]
                razas = list(coleccion.find({}, {"_id": 1, "Nombre": 1}))
    
                print("Razas existentes: (Seleccione el numero que va a modificar)")
                for i, raza in enumerate(razas):
                    print(f"{i+1}. {raza['Nombre']}")
    
                while True:
                    try:
                        eleccion_raza = int(input()) - 1
                        if 0 <= eleccion_raza < len(razas):  
                            raza_seleccionada = razas[eleccion_raza]  # Get the entire state document
                            raza_id = raza_seleccionada["_id"]
                            break
                        else:
                            print("Opción inválida. Por favor, elija un número de la lista.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                while True:
                    Decision = input("Desea modificar \n1. Nombre \n2. Descripcion \n3. Ambos? \nQue desea modificar?")
                    if Decision == '3':  # Use string comparison for input
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
                        nuevadescripcion = input("Nueva Descripcion: ")
                        resultado = coleccion.update_one({"_id": raza_id},
                                                        {"$set": {"Nombre": nuevonombre, "Descripcion": nuevadescripcion}})
                        print("Raza Actualizada")
                        break
                    elif Decision == '2': 
                        nuevadescripcion = input("Nueva Descripcion: ")
                        resultado = coleccion.update_one({"_id": raza_id},
                                    {"$set": {"Descripcion": nuevadescripcion}})
                        print("Raza Actualizada")
                        break
                    elif Decision == '1':
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
                        resultado = coleccion.update_one({"_id":raza_id}, {"set" : {"Nombre": nuevonombre}})
                        print("Raza Actualizada")
                        break
                    else:
                        print("Ingrese un numero valido")

            case "Equipamiento":
                self.equipamiento_personaje = {
                        "Cabeza": "",
                        "Mano Izquierda": "",
                        "Mano Derecha": "",
                        "Torso": "",
                        "Piernas": "",
                        "Pies": ""
                    }
                equipamiento_mod = list(self.equipamiento_personaje.keys())
                collecion = self.basededatos["Equipamiento"]
                Equipamientos = list(collecion.find({},{"_id":1,"Nombre": 1}))
                print("Habilidades Existentes: (Seleccione el numero que va a modificar)")
                for i, equipamiento in enumerate(Equipamientos):
                    print(f"{i+1}. {equipamiento['Nombre']}")
                while True:
                    try:
                        eleccion_equipamiento = int(input()) -1
                        if 0 <= eleccion_equipamiento < len(Equipamientos):
                            equipamiento_seleccionado = Equipamientos[eleccion_equipamiento]
                            id_equipamiento = equipamiento_seleccionado["_id"]
                            break
                        else: 
                            print("Eleccion Invalida, por favor elija una habilidad valida ")
                    except ValueError:
                        print("Por favor, ingrese un numero valido")
                while True:
                    Decision = input("Desea modificar  \n 1). Nombre \n 2. Descripcion \n3. Ranura \n4. Todo?\nQue desea Modificar?: ")
                    if Decision == "4":
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
                        nuevo_descripcion = input("Ingrese la nueva Descripcion ")

                        equipamiento_mod = list(self.equipamiento_personaje.keys())
                        for i, equipameinto in enumerate(equipamiento_mod):
                            print(f"{i+1}. {equipameinto}")

                        while True:
                            try:
                                destino = int(input("Elija la Ranura a la que va a pertenecer el equipamiento? (Escribe un número): ")) - 1
                                if 0 <= destino < len( equipamiento_mod):
                                    Ranura = equipamiento_mod[destino]
                                    break
                                else:
                                    print("Número inválido. Inténtalo de nuevo.")
                            except ValueError:
                                print("Ingresa un número válido.")
                        resultado = collecion.update_one({"_id":id_equipamiento}, {"$set": {"Nombre": nuevonombre, "Descripcion": nuevo_descripcion,"Ranura": Ranura }})
                        print("Equipamiento Actualizado:")
                    elif Decision == "3":
                        equipamiento_mod = list(self.equipamiento_personaje.keys())
                        for i, equipameinto in enumerate(equipamiento_mod):
                            print(f"{i+1}. {equipameinto}")

                        while True:
                            try:
                                destino = int(input("Elija la Ranura a la que va a pertenecer el equipamiento? (Escribe un número): ")) - 1
                                if 0 <= destino < len( equipamiento_mod):
                                    Ranura = equipamiento_mod[destino]
                                    break
                                else:
                                    print("Número inválido. Inténtalo de nuevo.")
                            except ValueError:
                                print("Ingresa un número válido.")
                        resultado = collecion.update_one({"_id": id_equipamiento}, {"$set" : {"Ranura" : Ranura} })
                    elif Decision == '2':
                        nuevadescripcion = input("Ingrese la nueva Descripcion: ")
                        resultado = collecion.update_one({"_id": id_equipamiento}, {"$set": {"Descripcion" : nuevadescripcion} })
                        print("Habilidad Actualizada")
                    elif Decision == '1':
                        while True:
                            nuevonombre = input("Ingrese el nombre: ")
                            if any(caracter in string.punctuation for caracter in nuevonombre):
                                print("No se permiten caracteres especiales.")
                            else:
                                print(f"El nombre '{nuevonombre}' está correcto.")
                                break
                        resultado = collecion.update_one({"_id" : id_equipamiento}, {'$set' : {"Nombre" : nuevonombre} } )
                        print("Habilidad Actualizada")  
                    else:
                        print("Ingrese un numero valido")    

    def Eliminar(self,Objeto):
    
        match Objeto:
            case "Estado":
                coleccion = self.basededatos["Estados"]
                Estados = list(coleccion.find({}, {"_id": 1, "Nombre": 1}))
    
                print("Estados Existentes: (Seleccione el estado que va a eliminar)")
                for i, estado in enumerate(Estados):
                    print(f"{i+1}. {estado['Nombre']}")
    
                while True:
                    try:
                        eleccion_estado = int(input("Cual desea eliminar: ")) - 1
                        if 0 <= eleccion_estado < len(Estados):  
                            estado_seleccionado = Estados[eleccion_estado]  # Get the entire state document
                            id_estado = estado_seleccionado["_id"]
                            break
                        else:
                            print("Opción inválida. Por favor, elija un número de la lista.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                eliminacion = coleccion.delete_one({"_id" : id_estado})
                print("El estado se ha eliminado")
            case "Poder":
                collecion = self.basededatos["Poderes"]
                Poderes = list(collecion.find({},{"_id":1,"Nombre": 1}))
                print("Poderes Existentes: (Seleccione el numero que va a modificar)")
                for i, poder in enumerate(Poderes):
                    print(f"{i+1}. {poder['Nombre']}")
                while True:
                    try:
                        eleccion_poder = int(input("Cual desea eliminar: ")) -1
                        if 0 <= eleccion_poder < len(Poderes):
                            poder_seleccionado = Poderes[eleccion_poder]
                            id_poder = poder_seleccionado["_id"]
                            break
                        else: 
                            print("Eleccion Invalida, por favor elija un poder valido ")
                    except ValueError:
                        print("Por favor, ingrese un numero valido")
                eliminacion = coleccion.delete_one({"_id" : id_poder})
                print("El poder se ha eliminado")
            case "Habilidades":
                collecion = self.basededatos["Habilidades"]
                Habilidades = list(collecion.find({},{"_id":1,"Nombre": 1}))
                print("Habilidades Existentes: (Seleccione el numero que va a modificar)")
                for i, habilidad in enumerate(Habilidades):
                    print(f"{i+1}. {habilidad['Nombre']}")
                while True:
                    try:
                        eleccion_habilidad = int(input("Cual desea eliminar: ")) -1
                        if 0 <= eleccion_habilidad < len(Habilidades):
                            habilidad_seleccionada = Habilidades[eleccion_habilidad]
                            id_habilidad = habilidad_seleccionada["_id"]
                            break
                        else: 
                            print("Eleccion Invalida, por favor elija una habilidad valida ")
                    except ValueError:
                        print("Por favor, ingrese un numero valido")
                    eliminacion = coleccion.delete_one({"_id" : id_habilidad})
                print("La habilidad se ha eliminado")
            case "Razas":
                coleccion = self.basededatos["Razas"]
                razas = list(coleccion.find({}, {"_id": 1, "Nombre": 1}))
    
                print("Razas existentes: (Seleccione el numero que va a modificar)")
                for i, raza in enumerate(razas):
                    print(f"{i+1}. {raza['Nombre']}")
    
                while True:
                    try:
                        eleccion_raza = int(input("Cual desea eliminar: ")) - 1
                        if 0 <= eleccion_raza < len(razas):  
                            raza_seleccionada = razas[eleccion_raza]  # Get the entire state document
                            raza_id = raza_seleccionada["_id"]
                            break
                        else:
                            print("Opción inválida. Por favor, elija un número de la lista.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                eliminacion = coleccion.delete_one({"_id" : raza_id})
                print("La raza se ha eliminado")
            case "Equipamiento":
                coleccion = self.basededatos["Equipamiento"]
                Equipamientos = list(coleccion.find({}, {"_id": 1, "Nombre": 1}))
    
                print("Equipamiento existente Razas existentes: (Seleccione el numero que va a modificar)")
                for i, equipo in enumerate(Equipamientos):
                    print(f"{i+1}. {equipo['Nombre']}")
    
                while True:
                    try:
                        eleccion_equipamiento = int(input("Cual desea eliminar: ")) - 1
                        if 0 <= eleccion_equipamiento < len(Equipamientos):  
                            equipamiento_seleccionado = Equipamientos[eleccion_equipamiento]  # Get the entire state document
                            raza_equipamiento = equipamiento_seleccionado["_id"]
                            break
                        else:
                            print("Opción inválida. Por favor, elija un número de la lista.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                eliminacion = coleccion.delete_one({"_id" : raza_equipamiento})
    def obtener_nombres_por_ids(self, nombre_coleccion, lista_ids):
        if isinstance(lista_ids, ObjectId):
            lista_ids = [lista_ids]
        elif not isinstance(lista_ids, list):  # Check if it's NOT a list
            lista_ids = [lista_ids] 
        coleccion = self.basededatos[nombre_coleccion]
        resultado = coleccion.find({"_id": {"$in": [ObjectId(id) for id in lista_ids]}}, {"Nombre": 1}) 
        return {str(r["_id"]): r["Nombre"] for r in resultado}
    
    def reemplazar_ids_por_nombres(self, documento, mapeo_ids_a_nombres):
        for clave, valor in documento.items():
            if isinstance(valor, ObjectId):
                documento[clave] = mapeo_ids_a_nombres.get(str(valor), valor)
            elif isinstance(valor, list):
                documento[clave] = [self.reemplazar_ids_por_nombres(item, mapeo_ids_a_nombres) if isinstance(item, dict) else
                                    mapeo_ids_a_nombres.get(str(item), item) if isinstance(item, ObjectId) else item for item in valor]
            elif isinstance(valor, dict):
                documento[clave] = self.reemplazar_ids_por_nombres(valor, mapeo_ids_a_nombres)
        return documento

    def modificar_personaje(self):

        coleccion_personajes = self.basededatos["Personajes"]
        personajes = list(coleccion_personajes.find({}, {"_id": 1, "Nombre": 1}))
    
        print("Personajes existentes:")
        for i, personaje in enumerate(personajes):
            print(f"{i+1}. {personaje['Nombre']}")
    
        while True:
            try:
                eleccion_personaje = int(input("Elija un personaje para modificar: ")) - 1
                if 0 <= eleccion_personaje < len(personajes):
                    personaje_seleccionado = personajes[eleccion_personaje]
                    id_personaje = personaje_seleccionado["_id"]
                    break
                else:
                    print("Opción inválida. Elija un número de la lista.")
            except ValueError:
                print("Ingrese un número válido.")
    
        personaje = coleccion_personajes.find_one({"_id": id_personaje})
    
        # Mapeos de IDs a nombres
        mapeo_razas = self.obtener_nombres_por_ids("Razas", personaje["Raza"])
        mapeo_estados = self.obtener_nombres_por_ids("Estados", personaje["Estado_ID"])
        mapeo_habilidades = self.obtener_nombres_por_ids("Habilidades", personaje["Habilidad_ID"])
        mapeo_equipamiento = self.obtener_nombres_por_ids("Equipamiento", personaje["Equipamiento_ID"])
        mapeo_poderes = self.obtener_nombres_por_ids("Poderes", personaje["Poderes_ID"])
    
        # Unir todos los mapeos en uno solo
        mapeo_ids_a_nombres = {**mapeo_razas, **mapeo_estados, **mapeo_habilidades, **mapeo_equipamiento, **mapeo_poderes}
    
        # Reemplazar IDs en el personaje
        personaje_con_nombres = self.reemplazar_ids_por_nombres(personaje, mapeo_ids_a_nombres)
    
        # Mostrar campos modificables
        campos_modificables = ["Raza", "Nivel", "HitPoints", "Estado_ID", "Habilidad_ID", "Equipamiento_ID", "Poderes_ID", "Atributos"]
        print("\nCampos que puedes modificar:")
        for campo in campos_modificables:
                print(f"- {campo}")
        
    def modificar_personaje(self):
        coleccion_personajes = self.basededatos["Personajes"]
        personajes = list(coleccion_personajes.find({}, {"_id": 1, "Nombre": 1}))
    
        print("Personajes existentes:")
        for i, personaje in enumerate(personajes):
            print(f"{i+1}. {personaje['Nombre']}")
    
        while True:
            try:
                eleccion_personaje = int(input("Elija un personaje para modificar: ")) - 1
                if 0 <= eleccion_personaje < len(personajes):
                    personaje_seleccionado = personajes[eleccion_personaje]
                    id_personaje = personaje_seleccionado["_id"]
                    break
                else:
                    print("Opción inválida. Elija un número de la lista.")
            except ValueError:
                print("Ingrese un número válido.")
    
        personaje = coleccion_personajes.find_one({"_id": id_personaje})
    
        # Mapeos de IDs a nombres
        mapeo_razas = self.obtener_nombres_por_ids("Razas", personaje["Raza"])
        mapeo_estados = self.obtener_nombres_por_ids("Estados", personaje["Estado_ID"])
        mapeo_habilidades = self.obtener_nombres_por_ids("Habilidades", personaje["Habilidad_ID"])
        mapeo_equipamiento = self.obtener_nombres_por_ids("Equipamiento", personaje["Equipamiento_ID"])
        mapeo_poderes = self.obtener_nombres_por_ids("Poderes", personaje["Poderes_ID"])
    
        # Unir todos los mapeos en uno solo
        mapeo_ids_a_nombres = {**mapeo_razas, **mapeo_estados, **mapeo_habilidades, **mapeo_equipamiento, **mapeo_poderes}
    
        # Reemplazar IDs en el personaje
        personaje_con_nombres = self.reemplazar_ids_por_nombres(personaje, mapeo_ids_a_nombres)
    
        # Mostrar campos modificables
        campos_modificables = ["Raza", "Nivel", "HitPoints", "Estado_ID", "Habilidad_ID", "Equipamiento_ID", "Poderes_ID", "Atributos"]
        print("\nCampos que puedes modificar:")
        for campo in campos_modificables:
            print(f"- {campo}")
    
        while True:
            campo_a_modificar = input("Elija un campo para modificar (o 'listo' para terminar): ")
            if campo_a_modificar.lower() == 'listo':
                break
    
            elif campo_a_modificar in campos_modificables:
                valor_actual = personaje_con_nombres[campo_a_modificar]
    
                if isinstance(valor_actual, list):
                    print(f"\nValores actuales de {campo_a_modificar}:")
                    for i, item in enumerate(valor_actual):
                        # Reemplazar IDs por nombres en la lista de valores actuales
                        if campo_a_modificar != "Atributos":  # Excluir atributos de manipulacion de ID
                            item_nombre = mapeo_ids_a_nombres.get(item, item)
                            print(f"{i+1}. {item_nombre}")
                        else:
                            print(f"{i+1}. {item}")  # Mostrar nombre de atributos
    
                    while True:  # Loop para las acciones a o e
                        accion = input(
                            f"Desea agregar (a) o eliminar (e) en {campo_a_modificar}? (o 'listo' para volver): "
                        )
                        if accion.lower() == 'listo':
                            break
                        elif accion.lower() in ['a', 'e']:
                            if (
                                campo_a_modificar == "Habilidad_ID"
                                and accion.lower() == 'e'
                                and i < 2
                            ):
                                print("No puedes eliminar las dos primeras habilidades.")
                                continue
                            elif (
                                campo_a_modificar in ["Equipamiento_ID", "Poderes_ID"]
                                and accion.lower() == 'e'
                                and i == 0
                            ):
                                print("No puedes eliminar el primer elemento.")
                                continue
    
                            if accion.lower() == 'a':
                                # Mostrar lista de opciones para campos ID y Raza
                                if campo_a_modificar in ["Estado_ID", "Habilidad_ID", "Equipamiento_ID", "Poderes_ID", "Raza"]:
                                    coleccion_opciones = self.basededatos[campo_a_modificar[:-3]] if campo_a_modificar != "Raza" else self.basededatos[campo_a_modificar]
                                    opciones = list(coleccion_opciones.find({}, {"Nombre": 1, "Descripcion": 1}))
    
                                    print(f"\nOpciones disponibles para {campo_a_modificar}:")
                                    for j, opcion in enumerate(opciones):
                                        print(f"{j+1}. {opcion['Nombre']}: {opcion['Descripcion']}")
    
                                    while True:
                                        try:
                                            eleccion_opcion = int(input("Elija una opción: ")) - 1
                                            if 0 <= eleccion_opcion < len(opciones):
                                                personaje[campo_a_modificar].append(str(opciones[eleccion_opcion]['_id'])) if isinstance(personaje[campo_a_modificar], list) else personaje.__setitem__(campo_a_modificar, str(opciones[eleccion_opcion]['_id']))
                                                break
                                            else:
                                                print("Opción inválida.")
                                        except ValueError:
                                            print("Ingrese un número válido.")
    
                            elif accion.lower() == 'e':
                                try:
                                    indice = int(input("Ingrese el índice del elemento a eliminar: ")) - 1
                                    if 0 <= indice < len(personaje[campo_a_modificar]):
                                        del personaje[campo_a_modificar][indice]
                                    else:
                                        print("Índice inválido.")
                                except ValueError:
                                    print("Ingrese un número válido.")
    
                            # Insertar cambios a la base de datos
                            coleccion_personajes.update_one({"_id": id_personaje}, {"$set": {campo_a_modificar: personaje[campo_a_modificar]}})
                            print(f"{campo_a_modificar} modificado con éxito.")
                            break  # Salir del loop
    
                        else:
                            print("Acción inválida. Elija 'a', 'e', o 'listo'.")
    
                else:  # Manejo para campos que no son listas
                    # Mostrar lista de opciones para el campo Raza o Estado_ID
                    if campo_a_modificar in ["Raza", "Estado_ID"]:
                        coleccion_opciones = self.basededatos["Estados"] if campo_a_modificar == "Estado_ID" else self.basededatos["Razas"]
                        opciones = list(coleccion_opciones.find({}, {"Nombre": 1, "Descripcion": 1}))
    
                        print(f"\nOpciones disponibles para {campo_a_modificar}:")
                        for j, opcion in enumerate(opciones):
                            print(f"{j+1}. {opcion['Nombre']}: {opcion['Descripcion']}")
    
                        while True:
                            try:
                                eleccion_opcion = int(input("Elija una opción: ")) - 1
                                if 0 <= eleccion_opcion < len(opciones):
                                    personaje[campo_a_modificar] = str(opciones[eleccion_opcion]['_id'])  # Reemplazar con la seleccion de ID
                                    break
                                else:
                                    print("Opción inválida.")
                            except ValueError:
                                print("Ingrese un número válido.")
    
                        # Insertar cambios a la base de datos
                        coleccion_personajes.update_one({"_id": id_personaje}, {"$set": {campo_a_modificar: personaje[campo_a_modificar]}})
                        print(f"{campo_a_modificar} modificado con éxito.")
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
                self.user = AtlasCliente(url1, dbname="JuegodeRol")  #
                break
            elif tipo_cuenta == "2":
                self.user = AtlasGameMaster(url, dbname="JuegodeRol")  
                break  
            else:
                print("Opción inválida. Intenta de nuevo.")


Usuario = TypeAccount()
Usuario.user.modificar_personaje()
