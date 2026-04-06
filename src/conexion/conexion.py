import MySQLdb

def conectar():
    try:
        conexion = MySQLdb.connect(
            host='localhost',
            user='root',
            password='2017Ldumb', # <--- Pon aquí la contraseña que elegiste en el instalador
            db='crunch_house_db',      # El nombre de la base que creamos en Workbench
            port=3307                  # Tu puerto especial
        )
        print("¡Conexión exitosa a la base de datos de Crunch House!")
        return conexion
    except Exception as ex:
        print("Error al conectar a MySQL:", ex)
        return None