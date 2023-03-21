from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import PaymentForm
from django.urls import reverse
from django.shortcuts import redirect
from .models import Merchant

def PaymentView(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access the payment page')
        return redirect(reverse('login'))
    else:
        try:
            merchant = Merchant.objects.get(user=request.user)
        except Merchant.DoesNotExist:
            messages.error(request,'Merchant not found')
            return redirect(reverse('login'))

        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                form.save(merchant)
                messages.success(request,f'Welcome {merchant.name}!')
                return redirect(reverse('payment'))
        else:
            form = PaymentForm()
        return render(request, 'payment.html', {'form': form, 'merchant': merchant})
