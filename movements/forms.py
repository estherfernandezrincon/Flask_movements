from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, HiddenField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, AnyOf, Email
from wtforms.widgets import TextArea, Select


from datetime import date




class alta(FlaskForm):
    fecha = DateField('fecha', validators=[DataRequired()])
    concepto = StringField('concepto', validators=[DataRequired("debes introducir concpeto")])
    cantidad=  DecimalField ('cantidad', validators=[DataRequired()])
 
    enviar= SubmitField("enviar")

    def validate_fecha(self, field):
        hoy = date.today()
        if self.fecha.data > hoy:
            raise ValidationError('La fecha debe ser inferior o igual a hoy')