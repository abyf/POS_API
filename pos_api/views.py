from django.shortcuts import render
from .forms import PaymentForm

def PaymentView(request):
    form = PaymentForm()
    return render(request, 'payment.html', {'form': form})
