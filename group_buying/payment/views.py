from django.shortcuts import render
import razorpay
from .models import Orders,OrderUpdate
# Create your views here.
def payment_home(request):
    return render(request,'payment/home.html')

# import razorpay
razorpay_client = razorpay.Client(auth=("rzp_live_pFO4eSGqt4R88G", "m7ZNXIhDfw0RKgl3svLrX39n"))

def checkout(request):
    return render(request, 'payment/checkout.html')

# Payment Method through Razorpay
def app_create(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order_amount = 1
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address': address}
        razorpay_order = razorpay_client.order.create(dict(amount=order_amount*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        print(razorpay_order['id'])
        order = Orders(items_json=items_json, name=name, email=email,address=address,city=city,state=state,zip_code=zip_code, phone=phone, amount=order_amount, razorpayid=razorpay_order['id'])   # saving in dataset just like by using python as in shell
        order.save()
        return render(request, 'payment/payment.html', {'order_id': razorpay_order['id'], 'cname': name, 'cemail': email,'cphone':phone})
        # ,{'order_id': order.order_id, 'amt': order_amount}

def app_charge(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            order_db = Orders.objects.get(razorpayid=order_id)
            order_db.razorpaypaymentid = payment_id
            order_db.razorpaysignature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount*100
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="The order has been placed")
                    update.save()
                    thank = True
                    # id = request.POST.get('shopping_order_id','')
                    p = OrderUpdate.objects.order_by('order_id').last()
                    id = p.order_id
                    params = {'thank': thank, 'id': id}
                    # response = json.dumps(razorpay_client.payment.fetch(payment_id))
                    return render(request, 'payment/checkout.html', params)
                except:
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
                    update.save()
                    thank =  False
                    return render(request, 'payment/checkout.html', {'thank': thank})
            else:
                update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
                update.save()
                thank =  False
                return render(request, 'payment/checkout.html', {'thank': thank})
        except:
            update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
            update.save()
            thank =  False
            return render(request, 'payment/checkout.html', {'thank': thank})
