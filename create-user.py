import string

#Este si es mi codigo creado por mi persona :D y aun en construccion pero ahora tengo que salir asi que xd

class FormularioCreacion:
    def __init__(self):

        #while para conseguir el nombre del personaje 
        ban = True
        while ban == True:
            self.nombre = input("Ingrese el Nombre de su personaje: ")
            
            #la primera condicion de este if sirve para que el nombre ingresado no tenga
            #caracteres especiales como '_' , '+', '*' etc 
            if any(caracter in string.punctuation for caracter in self.nombre): 
                print("Recuerde que no debe ingresar caracteres especiales.")
            elif self.nombre.lower() in ["homosexual","gay","gei",""]: #Para evitar que alguien sea gei
                print("NO SEAS MARICON")
            else:
                print(f"El nombre '{self.nombre}' está correcto.")
                ban = False

        #while para conseguir la raza deseada por el usuario
        ban = True
        while ban == True:
            razadisponible = ['humano','elfo','semi elfo','enanos','draconidos','gnomo','medianos','semi orco','tiflin']

            print("\nRazas Disponibles:")
            for raza in razadisponible:
                print(f"- {raza}")
            
            self.raza = input("Ingrese el nombre de la raza que quiere:").lower()

            if self.raza == "":
                print("Debe ingresar una raza")
            elif self.raza not in razadisponible:
                print("Ingrese una raza valida")
            else:
                print(f"Ha seleccionado la raza {self.raza}")
                ban = False

        #while para conseguir las habilidades deseadas por el usuario
        ban = True
        while ban == True:
            habilidaddisponible = ['correr','reir','saltar','dormir','comer']

            print("Habilidades Disponibles:")
            for habilidad in habilidaddisponible:
                print(f'- {habilidad}')

            habilidad1= input("Ingrese la primer habilidad que desea agregar:")
            
            if habilidad1 == "":
                print("Debe ingresar una habilidad")
            elif habilidad1 not in habilidaddisponible:
                print("Ingrese una habilidad valida")
            else:
                print(f"Has escojido la primer habilidad '{habilidad1}'")
            
            habilidad2= input("Ingrese la segunda habilidad:")

            if habilidad2 == "":
                print("Debe ingresar una habilidad")
            elif habilidad2 not in habilidaddisponible:
                print("Ingrese una habilidad valida")
            else:
                print(f"Has escojido la segunda habilidad '{habilidad2}'")
            
            habilidad3= input("Ingrese la tercer habilidad:")

            if habilidad3 == "":
                print("Debe ingresar una habilidad")
            elif habilidad3 not in habilidaddisponible:
                print("Ingrese una habilidad valida")
            else:
                print(f"Has escojido la primer habilidad '{habilidad3}'")
                print(f"Estas son todas tus habilidades '{habilidad1}','{habilidad2}','{habilidad3}'")
                ban = False
            
            self.habilidad = [habilidad1,habilidad2,habilidad3]
        
        #while para el equipamiento EN CONSTRUCCIÓN
        #ban = True
        #while ban == True:
        #    equipamientodisponible = ['espada','escudo','Baculo',]


    def DatosPersonaje(self):
        print("============================")
        Datos = [self.nombre, self.raza, self.habilidad]
        print("Datos del Personaje:")
        print(f"Nombre: {Datos[0]}")
        print(f"Raza: {Datos[1]}")
        print(f"Habilidades: {', '.join(self.habilidad)}")  # Mejor formato
        print(f"Equipamiento: {', '.join(self.equipamiento) }")
        print("============================")

formulario = FormularioCreacion()
formulario.DatosPersonaje() 

