from getpass import getpass
import string
import bcrypt

class CreateAccount:
    def MenuCreateAccount(self):
        print("┌────────────────────────────┐")
        print("│  >-<  Crea tu cuenta  >-<  │")
        print("└────────────────────────────┘")

    def DatosActuales(self,email_user: str,username: str):
        pass
        
    def ObtenerEmail(self):
        self.MenuCreateAccount()    
        while True:
            email_user = input("Ingrese su email:").lower()

            if not '@' in  email_user:
                print("Tu correo debe llevar '@'")
            
            elif not '.cl' in email_user[-3:] and not '.com' in email_user[-4:]:
                print("Debe tener '.cl' o '.com' al final")
            
            else:
                print("Email Correcto")
                break

    def ObtenerUsername(self):
        while True:
            username = input("Ingrese su username:")

            if not 4 <= len(username) <= 15:
                print("El username debe tener entre 4 y 15 caracteres.")
            else:
                print(f"Su username {username} esta correcto")
                break

    def ObtenerContraseña(self):
        while True:
            contraseña = getpass("Ingrese su contraseña:")
            
            if not 8 <= len(contraseña) <= 20: #Verifica la Longitud del codigo
                print("Su contraseña debe tener entre 8 y 20 caracteres.")

            elif not any(char.isdigit() for char in contraseña):  # Verifica si hay al menos un numero
                print("Su contraseña debe tener al menos un número.")

            elif not any(char in string.punctuation for char in contraseña):  # Verifica si hay al menos un carácter especial
                print("Su contraseña debe tener al menos un carácter especial.")
            
            elif not any(char.isupper() for char in contraseña):  # Verifica si hay al menos una mayúscula
                print("Su contraseña debe tener al menos una letra mayúscula.")
            
            else:
                contraseña_hash = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt())
                print("Su contraseña esta correcta")
                print(f"la contraseña es: {contraseña}")
                break
            return contraseña_hash

        

create = CreateAccount()
create.ObtenerEmail()
create.ObtenerUsername()
create.ObtenerContraseña()