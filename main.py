from getpass import getpass
from bson.binary import Binary
from bson.objectid import ObjectId
from clases import TypeAccount


url = "mongodb+srv://<username>:<password>@cluster0.rlqm0qg.mongodb.net/"
url1 = "mongodb+srv://JugadoresPorFavorFunciona:4fmRjvvCxji3QllQ@cluster0.rlqm0qg.mongodb.net/"

def menu_cliente(cliente):
    while True:
        print("\n╔═══════════════════════════════╗")
        print("║     ✨ Menú del Jugador ✨    ║")
        print("╠═══════════════════════════════╣")
        print("║ 1. 📜 Ver Fichas de Personajes║")
        print("║ 2. ⚙️  Modificar Equipamiento  ║")
        print("║ 3. 👤 Crear Personaje         ║")
        print("║ 4. 🚪 Salir                   ║")
        print("╚═══════════════════════════════╝")
        opcion = input("👉 Elija una opción: ")

        if opcion == '1':
            cliente.user.FichasPersonajes()
        elif opcion == '2':
            cliente.user.ModificarEquipamiento()
        elif opcion == '3':
            cliente.user.CrearPersonaje()
        elif opcion == '4':
            break
        else:
            print("Opción inválida.")

def menu_GameMaster(GameMaster):
    while True:
        print("\n╔═══════════════════════════════╗")
        print("║    Menú del Game Master       ║")
        print("╠═══════════════════════════════╣")
        print("║ 1.  ✚ Agregar Estado          ║")
        print("║ 2.  ⚡ Agregar Poder          ║")
        print("║ 3.  ✨ Agregar Habilidad      ║")
        print("║ 4.  🛡️ Agregar Equipamiento    ║")
        print("║ 5.  🧬 Agregar Raza           ║")
        print("║ 6.  🔄 Modificar              ║")
        print("║ 7.  ❌ Eliminar               ║")
        print("║ 8.  👁️ Ver Partida             ║")
        print("║ 9.  👤 Modificar Personaje    ║")
        print("║ 10. 🚪 Salir                  ║")
        print("╚═══════════════════════════════╝")
        opcion = input("👉 Elija una opción: ")

        if opcion == '1':
            GameMaster.user.AgregarEstado()
        elif opcion == '2':
            GameMaster.user.AgregarPoder()
        elif opcion == '3':
            GameMaster.user.AgregarHabilidades()
        elif opcion == '4':
            GameMaster.user.AgregarEquipamiento()
        elif opcion == '5':
            GameMaster.user.AgregarRaza()
        elif opcion == '6':
                Desicion = input("¿Qué desea modificar?\n1. Estado \n2. Poder \n3. Habilidad \n4. Raza \n.5 Equipamiento \nCual desea escoger?: ")
                if Desicion =='5':
                    GameMaster.user.Modificar("Equipamiento")
                elif Desicion == '4':
                    GameMaster.user.Modificar("Raza")
                elif Desicion == '3':
                    GameMaster.user.Modificar("Habilidad")
                elif Desicion == '2':
                    GameMaster.user.Modificar("Poder")
                elif Desicion == '1':
                    GameMaster.user.Modificar("Estado")
                else:
                    print("Ingrese un numero valido")

        elif opcion == '7':
                Desicion = input("¿Qué desea Eliminar?\n1. Estado \n2. Poder \n3. Habilidad \n4. Raza \n.5 Equipamiento \nCual desea escoger?: ")
                if Desicion =='5':
                    GameMaster.user.Eliminar("Equipamiento")
                elif Desicion == '4':
                    GameMaster.user.Eliminar("Raza")
                elif Desicion == '3':
                    GameMaster.user.Eliminar("Habilidad")
                elif Desicion == '2':
                    GameMaster.user.Eliminar("Poder")
                elif Desicion == '1':
                    GameMaster.user.Eliminar("Estado")
                else:
                    print("Ingrese un numero valido")
        elif opcion == '8':
            GameMaster.user.VerPartida()
        elif opcion == '9':
            GameMaster.user.modificar_personaje()
        elif opcion == '10':
            break
        else:
            print("Opción inválida.")

Usuario = TypeAccount()

if Usuario.obtener_cuenta() == "Jugador":
    Usuario.user.login()
    menu_cliente(Usuario)
else:
    menu_GameMaster(Usuario)
