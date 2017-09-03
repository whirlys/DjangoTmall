from django import forms
from .models import UserProfile
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label="用户名",error_messages={"invalid":"用户名不能为空"})
    email = forms.EmailField(required=True, label="邮箱", error_messages={"invalid":"邮箱格式错误"})
    password = forms.CharField(required=True, widget=forms.PasswordInput,min_length=6, label="密码",error_messages={"invalid":"密码至少需要6字符"})
    password2 = forms.CharField(required=True, widget=forms.PasswordInput,min_length=6, label="确认密码",error_messages={"invalid":"确认密码至少需要6字符"})
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username):
            raise forms.ValidationError("该用户名已经存在")
        return username

    # 邮箱唯一
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and UserProfile.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('该邮箱已被注册')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('两次密码不一致')

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    # captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class UserProfileForm(forms.Form):
    nick_name = forms.CharField(required=False, max_length=50)
    birthday = forms.DateField(required=False)
    gender = forms.CharField(required=False,max_length=6)
    address = forms.CharField(required=False,max_length=100)
    mobile = forms.CharField(required=False,max_length=11)
    identityCardType = forms.CharField(required=False,max_length=20)
    identityCardNo = forms.CharField(required=False,max_length=20)

    # def clean_identityCardType(self):
    #     identityCardType = self.cleaned_data.get('identityCardType')
    #     if identityCardType != '' or identityCardType != 'IDCard' or identityCardType != 'passport':
    #         raise forms.ValidationError("证件类型错误！")
    #     return identityCardType
    #
    # def clean_gender(self):
    #     gender = self.cleaned_data.get('gender')
    #     if gender != '' or gender != 'female' or gender != 'male':
    #         raise forms.ValidationError("性别错误")
    #     return gender


