class ProductoService:
    @staticmethod
    def listar_todos(db):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()

    @staticmethod
    def crear_producto(db, nombre, precio, stock, id_categoria):
        cursor = db.connection.cursor()
        # Esta es la parte de la imagen:
        sql = "INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)"
        valores = (nombre, precio, stock, id_categoria)
        cursor.execute(sql, valores)
        db.connection.commit()

    @staticmethod
    def obtener_por_id(db, id_producto):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        return cursor.fetchone()

    @staticmethod
    def actualizar_producto(db, id_producto, nombre, precio, stock):
        cursor = db.connection.cursor()
        sql = "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s"
        valores = (nombre, precio, stock, id_producto)
        cursor.execute(sql, valores)
        db.connection.commit()

    @staticmethod
    def eliminar_producto(db, id_producto):
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        db.connection.commit()