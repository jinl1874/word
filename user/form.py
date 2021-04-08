from django import forms


class UserDetailForm(forms.Form):
    nickname = forms.CharField(label='昵称', max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Nickname", 
    }))

    sign = forms.CharField(
        label='签名', max_length=256, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "sign",
        }))
    
    # age = forms.IntegerField(label='年龄', min_value=0, max_value=100,  widget=forms.PasswordInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': "age",
    #     }))

    avatar = forms.ImageField(label='头像')
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其它'),
    )
    sex = forms.ChoiceField(label='性别', choices=gender, widget=forms.RadioSelect(attrs={
        'class': 'Radio'
    }))
    birthday = forms.DateField(label='出生日期', widget=forms.DateInput(attrs={
        'class': 'form-control'
    }))
    


class PasswordChange(forms.Form):
    old_password = forms.CharField(
        label='旧密码', max_length=256, widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "old password",
        }))
    new_password_1 = forms.CharField(
        label='新密码', max_length=256, widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "new password",
        }))
    new_password_2 = forms.CharField(
        label='重复密码', max_length=256, widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "new password",
        }))

class SelectForm(forms.Form):
    ACTIVITY_STYLE = (("四级", "1"), ("六级", "2"), ("高考", "3"), ("全部", 4))
    word_type = forms.ChoiceField(label=u'活动类型', choices=ACTIVITY_STYLE, widget=forms.RadioSelect(attrs={
        'class': 'Radio'
    }))
