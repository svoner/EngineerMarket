from wtforms.validators import DataRequired, ValidationError, Length
from flask_wtf import FlaskForm
from app.models import Project, Product, User, Code
from wtforms import (SubmitField, StringField, MultipleFileField,
                     TextAreaField, DateField, RadioField, SelectField,
                     BooleanField, SelectMultipleField, DateTimeField, FieldList,
                     FormField, widgets)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class OrderForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    project = SelectField('项目', coerce=int)
    engineer = SelectField('工程师', coerce=int)
    working_hours = StringField('工时')
    begin_time = DateTimeField('进场时间', format='%Y-%m-%d %H:%M', id='datepick')
    # mode = RadioField('派工方式', coerce=int)
    description = TextAreaField(
        '实施说明', default='', validators=[DataRequired()])
    submit = SubmitField('提交')
    products = MultiCheckboxField('涉及产品', coerce=int)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.project.choices = [(p.id, p.name) for p in Project.query.all()]
        self.products.choices = [(p.id, p.name) for p in Product.query.all()]
        self.engineer.choices = [(0, '随机派发')]
        for p in User.query.filter(User.role_id == Code.engineer).all():
            self.engineer.choices.append((p.id, p.name))


class ProductForm(FlaskForm):
    name = StringField('产品名称', validators=[DataRequired()])
    description = StringField('产品描述', default='')
    price = StringField('基础实施价格', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, original_name, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            product = Product.query.filter_by(name=self.name.data).first()
            if product is not None:
                raise ValidationError('已经存在的产品名称')


class ProjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired()])
    customer_name = StringField('用户联系人', validators=[DataRequired()])
    customer_phone = StringField('联系电话', validators=[DataRequired()])
    customer_address = StringField('项目地址', validators=[DataRequired()])
    description = TextAreaField('项目描述', default='')
    submit = SubmitField('提交')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            project = Project.query.filter_by(name=self.name.data).first()
            if project is not None:
                raise ValidationError('已经存在的项目名称')

class OrderCommentForm(FlaskForm):
    score = RadioField('评分', choices=[(1, '差'),(2, '一般'),(3, '好')], coerce=int)
    content = TextAreaField('评价内容', validators=[(DataRequired('请输入评价内容'))])
    submit = SubmitField('提交')
