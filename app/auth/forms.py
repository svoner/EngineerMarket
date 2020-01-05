from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo

class LoginForm(FlaskForm):
    username = StringField('帐户', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    # 验证码字段
    submit = SubmitField('登录')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(('新密码'), validators=[DataRequired()])
    password2 = PasswordField(
        ('重复新密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')