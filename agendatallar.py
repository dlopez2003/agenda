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

    def buscar(self, criterio):
        query = """
        SELECT c.id, c.nombre, c.telefono, c.email, cat.nombre
        FROM contactos c
        LEFT JOIN categorias cat ON c.categoria_id = cat.id
        WHERE c.nombre LIKE %s OR c.telefono LIKE %s OR c.email LIKE %s
        """
        parametros = (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%")
        resultados = self.execute(query, parametros, fetch=True)
        if resultados:
            print("\n--- Resultados de la búsqueda ---")
            for contacto in resultados:
                print(f"ID: {contacto[0]}, Nombre: {contacto[1]}, Teléfono: {contacto[2]}, Email: {contacto[3]}, Categoría: {contacto[4]}")
        else:
            print("No se encontraron contactos que coincidan con el criterio.")

    def actualizar(self, contacto_id, nombre, telefono, email, categoria_id):
        self.execute(
            """
            UPDATE contactos
            SET nombre = %s, telefono = %s, email = %s, categoria_id = %s
            WHERE id = %s
            """,
            (nombre, telefono, email, categoria_id, contacto_id),
        )
        print(f"Contacto con ID {contacto_id} actualizado con éxito.")

    def eliminar(self, contacto_id):
        self.execute("DELETE FROM contactos WHERE id = %s", (contacto_id,))
        print(f"Contacto con ID {contacto_id} eliminado con éxito.")


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
    def __init__(self):
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
            if hasattr(model, "buscar"):
                print("5. Buscar")
            print("6. Volver")

            subopcion = input("Selecciona una opción: ")
            if subopcion == "1":
                self.opcion_crear(name, model)
            elif subopcion == "2":
                model.leer()
            elif subopcion == "3":
                self.opcion_actualizar(name, model)
            elif subopcion == "4":
                id_eliminar = input("ID a eliminar: ")
                model.eliminar(id_eliminar)
            elif subopcion == "5" and hasattr(model, "buscar"):
                criterio = input("Criterio de búsqueda: ")
                model.buscar(criterio)
            elif subopcion == "6":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def opcion_crear(self, name, model):
        if name == "Contactos":
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")
            categoria_id = input("ID Categoría: ")
            model.crear(nombre, telefono, email, categoria_id)
        elif name == "Categorías":
            nombre = input("Nombre: ")
            model.crear(nombre)
        elif name == "Notas":
            titulo = input("Título: ")
            contenido = input("Contenido: ")
            model.crear(titulo, contenido)
        elif name == "Eventos":
            contacto_id = input("ID Contacto: ")
            categoria_id = input("ID Categoría: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            descripcion = input("Descripción: ")
            model.crear(contacto_id, categoria_id, fecha, descripcion)

    def opcion_actualizar(self, name, model):
        if name == "Contactos":
            contacto_id = input("ID del contacto a actualizar: ")
            nombre = input("Nuevo Nombre: ")
            telefono = input("Nuevo Teléfono: ")
            email = input("Nuevo Email: ")
            categoria_id = input("Nuevo ID Categoría: ")
            model.actualizar(contacto_id, nombre, telefono, email, categoria_id)
        elif name == "Categorías":
            categoria_id = input("ID de la categoría a actualizar: ")
            nombre = input("Nuevo Nombre: ")
            model.actualizar(categoria_id, nombre)
        elif name == "Notas":
            nota_id = input("ID de la nota a actualizar: ")
            titulo = input("Nuevo Título: ")
            contenido = input("Nuevo Contenido: ")
            model.actualizar(nota_id, titulo, contenido)
        elif name == "Eventos":
            evento_id = input("ID del evento a actualizar: ")
            contacto_id = input("Nuevo ID Contacto: ")
            categoria_id = input("Nuevo ID Categoría: ")
            fecha = input("Nueva Fecha (YYYY-MM-DD): ")
            descripcion = input("Nueva Descripción: ")
            model.actualizar(evento_id, contacto_id, categoria_id, fecha, descripcion)


if __name__ == "__main__":
    Menu().mostrar_menu()
