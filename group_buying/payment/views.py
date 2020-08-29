from django.shortcuts import render,redirect
from .models import Orders,OrderUpdate
from profiles.models import UserProfile
import datetime

# Create your views here.
def payment_home(request):
    return render(request,'payment/home.html')

import razorpay
razorpay_client = razorpay.Client(auth=("rzp_test_HjTkiDCGJADmpE", "FFuLbceQq7d3bxsL2rawq6oR"))

def checkout(request):
    return render(request, 'payment/checkout.html')

def app_create(request):
    if request.method == "POST":
        amount = request.POST['radio1']
        name = 'santosh'
        email = 'saisantosh.c17@iiits.in'
        address = 'Bandlaguda'
        phone = '9121467576'
        order_amount = int(amount)
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address': address}
        razorpay_order = razorpay_client.order.create(dict(amount=order_amount*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        print(razorpay_order['id'])
        order = Orders(amount=order_amount, razorpayid=razorpay_order['id'])   # saving in dataset just like by using python as in shell
        order.save()
        return render(request, 'payment/payment.html', {'order_id': razorpay_order['id'], 'cname': name, 'cemail': email,'cphone':phone})

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
                days = int(order_db.amount*90/300)
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="The order has been placed")
                    update.save()
                    thank = True
                    p = OrderUpdate.objects.order_by('order_id').last()
                    id = p.order_id
                    params = {'thank': thank, 'id': id}
                    UserProfile.objects.filter(user=request.user).update(is_subscribed=True,subscription_start=datetime.datetime.now(),subscription_end=datetime.datetime.now()+datetime.timedelta(days))
                    return redirect('chat:rooms')
                except:
                    update = OrderUpdate(order_id=order_db.order_id, update_desc="Payment is unsuccessful")
                    update.save()
                    thank =  False
                    return redirect('chat:rooms')
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
