class ModEquipmentUser:
    def __init__(self):
        # Equipamiento inicial (puedes modificarlo)
        self.equipamiento_personaje = {
            "Cabeza": "Casco de hierro",
            "Mano Izquierda": "Escudo de madera",
            "Mano Derecha": "Espada corta",
            "Torso": "Coraza de cuero",
            "Piernas": "Pantalones de tela",
            "Pies": "Botas de cuero"
        }

    def interfazmenu(self):
        while True:
            print("┌────────────────────────────┐")
            print("│     Menú Equipamiento      │")
            print("└────────────────────────────┘")
            print("1. Ver Equipamiento")
            print("2. Modificar Equipamiento")
            print("3. Salir")

            try:
                opcion = int(input("¿Qué deseas hacer? (1-3): "))
                if opcion == 1:
                    self.mostrar_equipamiento()
                elif opcion == 2:
                    self.modificar_equipamiento()
                elif opcion == 3:
                    break
                else:
                    print("Opción inválida. Inténtalo de nuevo.")
            except ValueError:
                print("Ingresa un número válido.")

    def mostrar_equipamiento(self):
        print("┌────────────────────────────┐")
        print("│   Equipamiento Actual      │")
        print("└────────────────────────────┘")
        print("          |  O                ")
        print("          +--|---|            ")
        print("             |   |            ")
        print("            / \               ")
        print("          _/   \_             ")

        for ranura, item in self.equipamiento_personaje.items():
            print(f"- {ranura}: {item}")
        
        input("Presiona Enter para volver al menú...")

    def modificar_equipamiento(self):
        print("┌────────────────────────────┐")
        print("│   Modificar Equipamiento   │")
        print("└────────────────────────────┘")
        print("          |  O                ")
        print("          +--|---|            ")
        print("             |   |            ")
        print("            / \               ")
        print("          _/   \_             ")

        equipamiento_mod = list(self.equipamiento_personaje.keys())
        for i, equipameinto in enumerate(equipamiento_mod):
            print(f"{i+1}. {equipameinto}")

        while True:
            try:
                destino = int(input("¿Qué deseas modificar? (Escribe un número): ")) - 1
                if 0 <= destino < len(equipamiento_mod):
                    break
                else:
                    print("Número inválido. Inténtalo de nuevo.")
            except ValueError:
                print("Ingresa un número válido.")

        nuevo_item = input(f"Nuevo item para {equipamiento_mod[destino]}: ")
        self.mod_equipment(equipamiento_mod[destino], nuevo_item)

    def mod_equipment(self, ranura, nuevo_item):
        self.equipamiento_personaje[ranura] = nuevo_item
        print(f"¡{nuevo_item} equipado en {ranura}!")

# Iniciar el programa
Mod = ModEquipmentUser()
Mod.interfazmenu()
