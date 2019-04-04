from django.forms import widgets

wid_01 = widgets.TextInput(attrs={"class": "form-control"})
wid_02 = widgets.PasswordInput(attrs={"class": "form-control"})
error_messages = {"required": "用户名不能为空"}
pwd_error_message = {"required": "密码不能为空"}
emil_error_message = {"required": "邮箱不能为空"}
phone_error_message = {"required": "电话不能为空"}