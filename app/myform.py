from django import forms
from app.conf.settings import *
from app.models import *
from django.core.exceptions import ValidationError


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, widget=wid_01,
                           label='用户名',error_messages=error_messages)
    pwd = forms.CharField(max_length=32, widget=wid_02,
                          label='密码', error_messages=pwd_error_message)
    re_pwd = forms.CharField(max_length=32, widget=wid_02,
                             label='确认密码', error_messages=pwd_error_message)
    email = forms.EmailField(max_length=32, label='邮箱',
                             widget=widgets.EmailInput(attrs={"class": "form-control"}),
                             error_messages=emil_error_message)
    telephone = forms.CharField(max_length=32, widget=wid_01,
                                label="电话", error_messages=phone_error_message)

    # 局部钩子
    def clean_user(self):
        user = self.cleaned_data.get("user")
        re_user = UserInfo.objects.filter(username=user).first()
        if not re_user:
            return user
        else:
            raise ValidationError("该用户已注册")

    # 全局钩子
    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd != re_pwd:
            raise ValidationError("两次密码不一致")
        elif pwd:
            if pwd.isdigit():
                raise ValidationError("密码必须是字母和数字的混合")
        else:
            return self.cleaned_data

    def clean_telephone(self):

        telephone = self.cleaned_data.get("telephone")
        re_telephone = UserInfo.objects.filter(telephone="telephone").first()
        if re_telephone:
            raise ValidationError("该电话已被注册")
        elif telephone:
            if not telephone.isdigit():
                raise ValidationError("电话必须为数字")
            elif len(telephone) != 11:
                raise ValidationError("电话的长度为11位")
            else:
                return telephone
