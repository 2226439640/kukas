#自定义表单控件
# 在内部自定义一个表单类，继承于 forms.Form
from django import forms

class FileForm(forms.Form):
    file = forms.FileField(
        # 支持多文件上传
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='请选择文件',
    )