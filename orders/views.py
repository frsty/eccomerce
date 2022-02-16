from multiprocessing import context
from django.shortcuts import  render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime
# Create your views here.

def payments(request):
    return render(request, 'orders/payments.html')



def place_order(request, total = 0 , quantity = 0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0 :
        return redirect('store')


    grand_total = 0
    iva = 0

    #precio de la boleta
    for cart_item in cart_items:
        total += round((cart_item.product.price * cart_item.quantity))
        quantity += cart_item.quantity

    iva = round(total*0.19)
    grand_total = total + iva

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.addres_line_1 = form.cleaned_data['addres_line_1']
            data.addres_line_2 = form.cleaned_data['addres_line_2']
            data.state = form.cleaned_data['comuna']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.iva = iva
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr=int(datetime.date.today().strftime('%Y'))
            mt=int(datetime.date.today().strftime('%m'))
            dt=int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            # 20280110
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total' : total,
                'iva': iva,
                'grand_total': grand_total,
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')
