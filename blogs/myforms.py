from django import forms
from django.forms import widgets
from blogs import models
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

class UserForms(forms.Form):
    username = forms.CharField(min_length=4,
                               label='用户名',
                               error_messages={'required': '该字段不能为空',
                                               'max_length': '太长',
                                               'min_length': '太短',},
                               widget=widgets.TextInput(attrs={'class': 'form-control'}), )

    password = forms.CharField(min_length=4,
                               label='密码',
                               error_messages={'required': '该字段不能为空',
                                               'max_length': '太长',
                                               'min_length': '太短',},
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}), )

    re_password = forms.CharField(min_length=4, label='确认密码',
                                  error_messages={'required': '该字段不能为空',
                                                  'max_length': '太长',
                                                  'min_length': '太短',},
                                  widget=widgets.PasswordInput(attrs={'class': 'form-control'}), )

    email = forms.EmailField(label='邮箱',
                             error_messages={'required': '该字段不能为空',
                                             'invalid': '格式有误',
                                             'max_length': '太长',
                                             'min_length': '太短',},
                             widget=widgets.EmailInput(attrs={'class': 'form-control'}), )

    telephone = forms.CharField(label='手机号(选填)',
                                required=False,
                                error_messages={'invalid': '格式有误',
                                                'max_length': '太长',
                                                'min_length': '太短',},
                                min_length=11,
                                widget=widgets.TextInput(attrs={'class': 'form-control'}),
                                )

    # 验证昵称局部钩子
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isdigit():
            raise ValidationError('用户名不能是纯数字!')
        else:
            param = models.UserInfo.objects.filter(username=username).first()
            if not param:
                return username
            else:
                raise ValidationError('该昵称已注册!')

    # # 验证密码
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     pattern = re.compile(r'(\d+\w+)|(\w+\d+)')
    #     result = re.findall(pattern,password)
    #     if result:
    #         print(result)

    # 验证手机号
    def clean_telphone(self):
        telphone = self.cleaned_data.get('telphone')
        if not telphone.isdigit():
            raise ValidationError('手机号码必须为数字')
        else:
            return telphone

    # 验证两次密码是否相同全局钩子

    def clean(self):
        # 当有密码输入框都有值时
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致!')

