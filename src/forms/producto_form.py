from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0.1)])
    stock = IntegerField('Cantidad en Stock', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar Producto')