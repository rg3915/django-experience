from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import OrderForm
from .models import Order


def order_list(request):
    template_name = 'order/order_list.html'
    object_list = Order.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)


@login_required
def order_create(request):
    template_name = 'order/order_form.html'
    # Passa o usuário logado no formulário.
    form = OrderForm(request.user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('order:order_list')

    context = {'form': form}
    return render(request, template_name, context)
