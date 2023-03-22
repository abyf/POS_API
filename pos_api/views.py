from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import PaymentForm
from django.urls import reverse
from django.shortcuts import redirect
from .models import Merchant, CardHolder, Payment
from .serializers import CardHolderSerializer, MerchantSerializer

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
                card_id = form.cleaned_data['card_id']
                amount = form.cleaned_data['amount']

                try:
                    cardholder = CardHolder.objects.get(card_id=card_id)
                except CardHolder.DoesNotExist:
                    messages.error(request,'Invalid card ID')
                    return redirect(reverse('payment'))

                if cardholder.balance < amount:
                    messages.error(request,'Insufficient funds')
                    return redirect(reverse('payment'))

                cardholder.balance -= amount
                cardholder.save()

                merchant.balance += amount
                merchant.save()

                Payment.objects.create(
                        card_id=cardholder,
                        reader_id=merchant,
                        amount=amount
                        )
                messages.success(request, f'Transaction successful. Your balance is {merchant.balance}.')
                
        else:
            form = PaymentForm()
        return render(request, 'payment.html', {
            'form': form, 
            'merchant': merchant,
            'cardholders': CardHolderSerializer(CardHolder.objects.all(), many=True).data})
