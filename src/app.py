from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from fpdf import FPDF 
import os

from config import config

# Importar las CAPAS de Crunch House
from models.ModelUser import ModelUser
from models.entities.User import User
from models.producto import Producto
from services.producto_service import ProductoService
from forms.producto_form import ProductoForm

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# --- RUTAS DEL CRUD DE PRODUCTOS ---

@app.route('/productos')
@login_required
def listar_productos():
    productos = ProductoService.listar_todos(db)
    return render_template('productos/inventario.html', productos=productos)

@app.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        # id_categoria 1 por defecto
        ProductoService.crear_producto(db, form.nombre.data, form.precio.data, form.stock.data, 1)
        flash("¡Producto guardado exitosamente!")
        return redirect(url_for('listar_productos'))
    return render_template('productos/crear.html', form=form, editando=False)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto_data = ProductoService.obtener_por_id(db, id)
    if not producto_data:
        flash("Producto no encontrado.")
        return redirect(url_for('listar_productos'))
    
    form = ProductoForm()
    
    if request.method == 'GET':
        # AJUSTE DE ÍNDICES: [1] nombre, [3] precio, [4] stock
        form.nombre.data = producto_data[1]
        form.precio.data = producto_data[3]
        form.stock.data = producto_data[4]
        
    if form.validate_on_submit():
        ProductoService.actualizar_producto(db, id, form.nombre.data, form.precio.data, form.stock.data)
        flash("¡Producto actualizado correctamente!")
        return redirect(url_for('listar_productos'))
        
    return render_template('productos/crear.html', form=form, editando=True)

@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    ProductoService.eliminar_producto(db, id)
    flash("Producto eliminado.")
    return redirect(url_for('listar_productos'))

# --- REPORTE PDF AJUSTADO ---

@app.route('/reporte_pdf')
@login_required
def reporte_pdf():
    try:
        productos = ProductoService.listar_todos(db)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="CRUNCH HOUSE - REPORTE DE INVENTARIO", ln=1, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(80, 10, "Nombre", 1)
        pdf.cell(40, 10, "Precio", 1)
        pdf.cell(40, 10, "Stock", 1)
        pdf.ln()
        
        pdf.set_font("Arial", size=12)
        for prod in productos:
            pdf.cell(80, 10, str(prod[1]), 1)
            # Ajuste de índices también en el PDF
            pdf.cell(40, 10, str(prod[3]), 1)
            pdf.cell(40, 10, str(prod[4]), 1)
            pdf.ln()
        
        nombre_archivo = "reporte_crunch_house.pdf"
        ruta_completa = os.path.join(os.getcwd(), nombre_archivo)
        pdf.output(ruta_completa)
        return send_file(ruta_completa, as_attachment=True)
    except Exception as e:
        return f"Error al generar reporte: {str(e)}"

# --- MANEJO DE ERRORES ---

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()