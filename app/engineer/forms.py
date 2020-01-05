from wtforms.validators import DataRequired, ValidationError, Length
from flask_wtf import FlaskForm
from app.models import Product
from wtforms import (SubmitField, StringField, MultipleFileField,
                     TextAreaField, DateTimeField, SelectField)


class LogForm(FlaskForm):
    title = StringField('简述', validators=[DataRequired(), Length(min=1, max=20)])
    begin = DateTimeField('进场时间', format='%Y-%m-%d %H:%M', id='begin')
    after = DateTimeField('离场时间', format='%Y-%m-%d %H:%M', id='after')
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')


class SkillEditForm(FlaskForm):
    product = SelectField('技能名称', coerce=int)
    level = SelectField('技能等级', coerce=int)
    submit = SubmitField('更新')

    def __init__(self, *args, **kwargs):
        super(SkillEditForm, self).__init__(*args, **kwargs)
        self.product.choices = [(p.id, p.name) for p in Product.query.all()]
        self.level.choices = [(l, l) for l in range(1, 6)]

