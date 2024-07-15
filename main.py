from getpass import getpass
from clases import AtlasCliente
from clases import AtlasGameMaster
from clases import TypeAccount

url = "mongodb+srv://<username>:<password>@cluster0.rlqm0qg.mongodb.net/"
url1 = "mongodb+srv://JugadoresPorFavorFunciona:4fmRjvvCxji3QllQ@cluster0.rlqm0qg.mongodb.net/"

def menu_cliente(cliente):
    while True:
        print("\n╔═══════════════════════════════╗")
        print("║     ✨ Menú del Jugador ✨     ║")
        print("╠═══════════════════════════════╣")
        print("║ 1. 📜 Ver Fichas de Personajes ║")
        print("║ 2. ⚙️ Modificar Equipamiento   ║")
        print("║ 3. 👤 Crear Personaje          ║")
        print("║ 4. 🚪 Salir                     ║")
        print("╚═══════════════════════════════╝")
        opcion = input("👉 Elija una opción: ")

        if opcion == '1':
            cliente.FichasPersonajes()
        elif opcion == '2':
            cliente.ModificarEquipamiento()
        elif opcion == '3':
            cliente.CrearPersonaje()
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
            GameMaster.AgregarEstado()
        elif opcion == '2':
            GameMaster.AgregarPoder()
        elif opcion == '3':
            GameMaster.AgregarHabilidades()
        elif opcion == '4':
            GameMaster.AgregarEquipamiento()
        elif opcion == '5':
            GameMaster.AgregarRaza()
        elif opcion == '6':
            while True:
                Desicion = input("¿Qué desea modificar?\n1. Estado \n2. Poder \n3. Habilidad \n4. Raza \n.5 Equipamiento \nCual desea escoger?: ")
                if Desicion =='5':
                    GameMaster.Modificar("Equipamiento")
                elif Desicion == '4':
                    GameMaster.Modificar("Raza")
                elif Desicion == '3':
                    GameMaster.Modificar("Habilidad")
                elif Desicion == '2':
                    GameMaster.Modificar("Poder")
                elif Desicion == '1':
                    GameMaster.Modificar("Estado")
                else:
                    print("Ingrese un numero valido")

        elif opcion == '7':
            while True:
                Desicion = input("¿Qué desea Eliminar?\n1. Estado \n2. Poder \n3. Habilidad \n4. Raza \n.5 Equipamiento \nCual desea escoger?: ")
                if Desicion =='5':
                    GameMaster.Eliminar("Equipamiento")
                elif Desicion == '4':
                    GameMaster.Eliminar("Raza")
                elif Desicion == '3':
                    GameMaster.Eliminar("Habilidad")
                elif Desicion == '2':
                    GameMaster.Eliminar("Poder")
                elif Desicion == '1':
                    GameMaster.Eliminar("Estado")
                else:
                    print("Ingrese un numero valido")
        elif opcion == '8':
            GameMaster.VerPartida()
        elif opcion == '9':
            GameMaster.modificar_personaje()
        elif opcion == '10':
            break
        else:
            print("Opción inválida.")
