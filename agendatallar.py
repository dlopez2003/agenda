import mysql.connector
from datetime import datetime


class DatabaseManager:
    """Clase para gestionar la conexión con MySQL."""
    def __init__(self, host="localhost", user="root", password="", database="agenda"):
        self.config = {"host": host, "user": user, "password": password, "database": database}
        self.connect()

    def connect(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None, fetch=False):
        self.cursor.execute(query, params or ())
        if fetch:
            return self.cursor.fetchall()
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


class BaseModel:
    """Clase base para CRUD de modelos."""
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def execute(self, query, params=None, fetch=False):
        return self.db_manager.execute_query(query, params, fetch)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    class Menu:
    def _init_(self):
        self.db_manager = DatabaseManager()
        self.models = {
            "1": ("Contactos", Contacto(self.db_manager)),
            "2": ("Categorías", Categoria(self.db_manager)),
            "3": ("Eventos", Evento(self.db_manager)),
            "4": ("Notas", Nota(self.db_manager)),
        }

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Principal ---")
            for key, (name, _) in self.models.items():
                print(f"{key}. {name}")
            print("5. Salir")

            opcion = input("Selecciona una opción: ")
            if opcion in self.models:
                self.mostrar_submenu(opcion)
            elif opcion == "5":
                self.db_manager.close()
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def mostrar_submenu(self, opcion):
        name, model = self.models[opcion]
        while True:
            print(f"\n--- Menú de {name} ---")
            print("1. Crear")
            print("2. Leer")
            print("3. Actualizar")
            print("4. Eliminar")
            print("6. Volver")

            subopcion = input("Selecciona una opción: ")
            if subopcion == "1":
                pass  # Implementar lógica
            elif subopcion == "2":
                model.leer()
            elif subopcion == "6":
                break

if _name_ == "_main_":
    Menu().mostrar_menu()
