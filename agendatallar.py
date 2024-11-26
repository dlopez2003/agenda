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
class Categoria(BaseModel):
    def crear(self, nombre):
        self.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
        print(f"Categoría '{nombre}' creada con éxito.")

    def leer(self):
        categorias = self.execute("SELECT * FROM categorias ORDER BY id DESC", fetch=True)
        if categorias:
            print("\n--- Categorías (de más reciente a más antiguo) ---")
            for categoria in categorias:
                print(f"ID: {categoria[0]}, Nombre: {categoria[1]}")
        else:
            print("No hay categorías registradas.")

    def actualizar(self, categoria_id, nombre):
        self.execute(
            "UPDATE categorias SET nombre = %s WHERE id = %s",
            (nombre, categoria_id),
        )
        print(f"Categoría con ID {categoria_id} actualizada con éxito.")

    def eliminar(self, categoria_id):
        self.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
        print(f"Categoría con ID {categoria_id} eliminada con éxito.")


class Contacto(BaseModel):
    def crear(self, nombre, telefono, email, categoria_id):
        self.execute(
            "INSERT INTO contactos (nombre, telefono, email, categoria_id) VALUES (%s, %s, %s, %s)",
            (nombre, telefono, email, categoria_id),
        )
        print(f"Contacto '{nombre}' creado con éxito.")

    def leer(self):
        contactos = self.execute(
            """
            SELECT c.id, c.nombre, c.telefono, c.email, cat.nombre
            FROM contactos c
            LEFT JOIN categorias cat ON c.categoria_id = cat.id
            ORDER BY c.id DESC
            """,
            fetch=True,
        )
        if contactos:
            print("\n--- Contactos (de más reciente a más antiguo) ---")
            for contacto in contactos:
                print(f"ID: {contacto[0]}, Nombre: {contacto[1]}, Teléfono: {contacto[2]}, Email: {contacto[3]}, Categoría: {contacto[4]}")
        else:
            print("No hay contactos registrados.")
