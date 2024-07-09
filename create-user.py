import string

class FormularioCreacion:
    def __init__(self):
        self.nombre = None
        self.raza = None
        self.habilidad = None
        self.equipamiento = None
        self.poderes = None
        self.atributos = None

        ban = True
        while ban == True:
            self.nombre = input("Ingrese el Nombre de su personaje: ")
            
            if any(caracter in string.punctuation for caracter in self.nombre):
                print("Recuerde que no debe ingresar caracteres especiales.")
            else:
                print(f"El nombre '{self.nombre}' está correcto.")
                ban = False

        ban = True
        while ban == True:
            razadisponible = ['humano','elfo','semi elfo','enanos','draconidos','gnomo','medianos','semi orco','tiflin']

            print("Razas Disponibles:")
            for raza in razadisponible:
                print(raza)
            
            self.raza = input("Ingrese el nombre de la raza que quiere:").lower()

            if self.raza == "":
                print("Debe ingresar una raza")
            elif self.raza not in razadisponible:
                print("Ingrese una raza valida")
            else:
                print(f"Ha seleccionado la raza {self.raza}")
                ban = False
        
    def DatosPersonaje(self):
        print("============================")
        Datos = [self.nombre, self.raza]
        print("Datos del Personaje:")
        print(f"Nombre: {Datos[0]}")
        print(f"Raza: {Datos[1]}")

formulario = FormularioCreacion()
formulario.DatosPersonaje() 

