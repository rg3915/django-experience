from django import forms

from .models import Employee, Order


class OrderForm(forms.ModelForm):
    required_css_class = 'required'

    employee = forms.ModelChoiceField(
        label='Funcionário',
        queryset=None,
    )

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retorna o funcionário logado.
        employee = user.user_employees.first()

        # Retorna o departamento do funcionário logado.
        department = employee.department

        # Retorna somente os funcionários do meu departamento.
        employees = Employee.objects.filter(department=department)

        # Altera o filtro de ModelChoiceField.
        self.fields['employee'].queryset = employees

        # Adiciona classe form-control nos campos.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
