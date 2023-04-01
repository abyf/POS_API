from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import PaymentForm, MerchantAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import Merchant, CardHolder, Payment
from .serializers import CardHolderSerializer, MerchantSerializer

class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = MerchantAuthenticationForm

    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username,password=password)
        if user is not None and user.is_active:
            if hasattr(user,'merchant'):
                try:
                    merchant = Merchant.objects.get(user=user)
                    login(self.request, user)
                    return redirect(reverse('payment'))
                except Merchant.DoesNotExist:
                    messages.error(self.request, 'Unknown Merchant!!!')
            else:
                messages.error('Merchant Does not Exist! Please register an account at the nearest office counter')
        else:
            messages.error(self.request, 'Please a correct username and password!!!')
    #    if not Merchant.objects.filter(user=self.request.user).exist():
    #        form.add_error(None,'Unknown User, Please register a merchant account at the nearest counter')
    #    else:
    #        form.add_error(None,'Please enter a correct username and password.')

        return super().form_invalid(form)

    def form_invalid(self,form):
        response = super().form_invalid(form)
        if 'Please enter a correct username and password.' in str(response.content):
            username = form.cleaned_data.get('username')
            try:
                merchant = form.cleaned_data.get(user__username=username)
            except Merchant.DoesNotExist:
                messages.error(self.request,"Merchant Does not Exist! Please register an account at the nearest office counter")
                return self.render_to_response(self.get_context_data(form=form))
        return response

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
        initial = {'wallet_id': merchant.wallet_id}
        form = PaymentForm(initial=initial)

    success = request.GET.get('success')
    context = {'form':form,'merchant':merchant,'success':success}
    if success:
        context['success'] = True
    return render(request, 'payment.html', context)
