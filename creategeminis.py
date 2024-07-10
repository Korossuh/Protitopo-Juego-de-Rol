import string

#Este codigo lo genero el geminis cuando le pase mi codigo para ver que cosas me aconsejaba realizar 
#con mi codigo asi que si sirve seguimos con este o ahí vemos que onda :D ya que este es mas 
#corto y mejor xd pero eso :D

class FormularioCreacion:
    def __init__(self):
        self.nombre = self.obtener_nombre()
        self.raza = self.obtener_raza()
        self.habilidad = self.obtener_habilidades()
        self.equipamiento = self.obtener_equipamiento()
        self.poder = self.obtener_poderes()

    def obtener_nombre(self):
        while True:
            nombre = input("Ingrese el nombre de su personaje: ")
            #la primera condicion de este if sirve para que el nombre ingresado no tenga
            #caracteres especiales como '_' , '+', '*' etc 
            if any(caracter in string.punctuation for caracter in nombre):
                print("No se permiten caracteres especiales.")
            elif nombre.lower() in ["homosexual", "gei"]:
                print("No seas Gey")
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
        carisma = 0
        fuerza = 0 
        salto = 0
        administracion = 0
        atributosdisponibles = [carisma,fuerza,salto,administracion]

        ban = True
        while ban == True:
            print("\nQue atributos deseas modificar:")
            for atributo in atributosdisponibles:
                print(f"- {atributo}")
        

    def DatosPersonaje(self):
        print("\n============================")
        print("Datos del Personaje:")
        print(f"Nombre: {self.nombre}")
        print(f"Raza: {self.raza}")
        print(f"Habilidades: {', '.join(self.habilidad)}")
        print(f"Equipamiento: {', '.join(self.equipamiento)}")
        print(f"Poderes: {', '.join(self.poder)}")  
        print("============================")


formulario = FormularioCreacion()
formulario.DatosPersonaje()
