from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Todo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_done'].widget.attrs['class'] = None
