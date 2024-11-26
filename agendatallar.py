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
    
    
    
    





class Evento(BaseModel):
    def crear(self, contacto_id, categoria_id, fecha, descripcion):
        self.execute(
            "INSERT INTO eventos (contacto_id, categoria_id, fecha, descripcion) VALUES (%s, %s, %s, %s)",
            (contacto_id, categoria_id, fecha, descripcion),
        )
        print("Evento creado con éxito.")

    def leer(self):
        eventos = self.execute(
            """
            SELECT e.id, e.fecha, e.descripcion, c.nombre AS contacto, cat.nombre AS categoria
            FROM eventos e
            LEFT JOIN contactos c ON e.contacto_id = c.id
            LEFT JOIN categorias cat ON e.categoria_id = cat.id
            ORDER BY e.id DESC
            """,
            fetch=True,
        )
        if eventos:
            print("\n--- Eventos (de más reciente a más antiguo) ---")
            for evento in eventos:
                print(f"ID: {evento[0]}, Fecha: {evento[1]}, Descripción: {evento[2]}, Contacto: {evento[3]}, Categoría: {evento[4]}")
        else:
            print("No hay eventos registrados.")

    def actualizar(self, evento_id, contacto_id, categoria_id, fecha, descripcion):
        self.execute(
            """
            UPDATE eventos
            SET contacto_id = %s, categoria_id = %s, fecha = %s, descripcion = %s
            WHERE id = %s
            """,
            (contacto_id, categoria_id, fecha, descripcion, evento_id),
        )
        print(f"Evento con ID {evento_id} actualizado con éxito.")

    def eliminar(self, evento_id):
        self.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
        print(f"Evento con ID {evento_id} eliminado con éxito.")


class Nota(BaseModel):
    def crear(self, titulo, contenido):
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute(
            "INSERT INTO notas (titulo, contenido, fecha_creacion) VALUES (%s, %s, %s)",
            (titulo, contenido, fecha_creacion),
        )
        print(f"Nota '{titulo}' creada con éxito.")

    def leer(self):
        notas = self.execute("SELECT * FROM notas ORDER BY id DESC", fetch=True)
        if notas:
            print("\n--- Notas (de más reciente a más antiguo) ---")
            for nota in notas:
                print(f"ID: {nota[0]}, Título: {nota[1]}, Contenido: {nota[2]}, Fecha: {nota[3]}")
        else:
            print("No hay notas registradas.")

    def actualizar(self, nota_id, titulo, contenido):
        self.execute(
            """
            UPDATE notas
            SET titulo = %s, contenido = %s
            WHERE id = %s
            """,
            (titulo, contenido, nota_id),
        )
        print(f"Nota con ID {nota_id} actualizada con éxito.")

    def eliminar(self, nota_id):
        self.execute("DELETE FROM notas WHERE id = %s", (nota_id,))
        print(f"Nota con ID {nota_id} eliminada con éxito.")
 
    
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

if __name__ == "_main_":
    Menu().mostrar_menu()
