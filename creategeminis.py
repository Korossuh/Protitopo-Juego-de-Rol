import string

#Este codigo lo genero el geminis cuando le pase mi codigo para ver que cosas me aconsejaba realizar 
#con mi codigo asi que si sirve seguimos con este o ahí vemos que onda :D ya que este es mas 
#corto y mejor xd pero eso :D

class FormularioCreacion:
    def __init__(self):
        self.nombre = self.obtener_nombre()
        self.raza = self.obtener_raza()
        self.habilidad = self.obtener_habilidades()

    def obtener_nombre(self):
        while True:
            nombre = input("Ingrese el nombre de su personaje: ")
            if any(caracter in string.punctuation for caracter in nombre):
                print("No se permiten caracteres especiales.")
            elif nombre.lower() in ["homosexual", "gei"]:  # Evitar palabras ofensivas
                print("Por favor, elige un nombre apropiado.")
            else:
                print(f"El nombre '{nombre}' está correcto.")
                return nombre

    def obtener_raza(self):
        razadisponible = ['humano', 'elfo', 'semi elfo', 'enano', 'draconido', 'gnomo', 'mediano', 'semi orco', 'tiflin']
        while True:
            print("\nRazas Disponibles:")
            for raza in razadisponible:
                print(f"- {raza}")  # Formato más claro
            raza = input("Ingrese el nombre de la raza que quiere: ").lower()
            if raza in razadisponible:
                print(f"Ha seleccionado la raza '{raza}'.")
                return raza
            else:
                print("Ingrese una raza válida.")

    def obtener_habilidades(self):
        habilidaddisponible = ['correr', 'reír', 'saltar', 'dormir', 'comer']
        habilidades_escogidas = []
        while len(habilidades_escogidas) < 3:
            print("\nHabilidades Disponibles:")
            for habilidad in habilidaddisponible:
                print(f"- {habilidad}")
            habilidad = input(f"Ingrese la habilidad número {len(habilidades_escogidas) + 1}: ").lower()
            if habilidad in habilidaddisponible and habilidad not in habilidades_escogidas:
                habilidades_escogidas.append(habilidad)
                print(f"Has escogido la habilidad '{habilidad}'.")
            else:
                print("Ingrese una habilidad válida y que no hayas escogido antes.")
        print(f"Estas son tus habilidades: {', '.join(habilidades_escogidas)}")  # Mejor formato
        return habilidades_escogidas

    def DatosPersonaje(self):
        print("\n============================")
        print("Datos del Personaje:")
        print(f"Nombre: {self.nombre}")
        print(f"Raza: {self.raza}")
        print(f"Habilidades: {', '.join(self.habilidad)}")  # Mejor formato
        print("============================")


formulario = FormularioCreacion()
formulario.DatosPersonaje()
