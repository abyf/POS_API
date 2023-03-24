from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import PaymentForm
from django.urls import reverse
from .models import Merchant, CardHolder, Payment
from .serializers import CardHolderSerializer, MerchantSerializer

def PaymentView(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access the payment page')
        return redirect(reverse('login'))

    try:
        merchant = Merchant.objects.get(user=request.user)
    except Merchant.DoesNotExist:
        messages.error(request,'Merchant not found',)
        return redirect(reverse('login'))

    success = False
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                form.charge_and_credit(merchant)
                messages.success(request, 'Payment processed successfully')
                return redirect(reverse('payment') + '?success=true')
            except Exception as e:
                messages.error(request,str(e))
                return redirect(reverse('payment'))

    else:
        form = PaymentForm()

    success = request.GET.get('success')
    context = {'form':form,'merchant':merchant,'success':success}
    if success:
        context['success'] = True
    return render(request, 'payment.html', context)
