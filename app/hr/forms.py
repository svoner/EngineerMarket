from wtforms.validators import DataRequired, ValidationError, Email
from flask_wtf import FlaskForm
from app.models import Project, Product, User, Code, Role
from wtforms import (SubmitField, StringField, RadioField,
                     BooleanField, FileField)


class UserEditForm(FlaskForm):
    upload = FileField('头像')
    # upload = FileField('头像照片', validators=[
    #     FileAllowed(UploadSet('images', IMAGES), '只能上传照片')])
    name = StringField('姓名', validators=[DataRequired()])
    gender = RadioField('性别', coerce=str)
    username = StringField('登录帐号')
    phone = StringField('电话')
    email = StringField('邮箱', validators=[Email('错误邮箱格式')])
    role = RadioField('角色', coerce=int)
    is_manager = BooleanField('主管')
    submit=SubmitField('提交')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.gender.choices=[('男', '男'), ('女', '女')]
        self.role.choices=[(i.id, i.name) for i in Role.query.all()]
        self.original_username=original_username
        self.original_email=original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user=User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('已经存在的账号')

    def validate_email(self, email):
        if email.data != self.original_email:
            user=User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('已经存在的 Email')
