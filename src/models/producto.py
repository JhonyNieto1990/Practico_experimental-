class Producto:
    def __init__(self, id_producto, nombre, precio, stock, id_categoria=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria