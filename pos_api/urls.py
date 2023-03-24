from django.urls import path
from . import views
from .views import PaymentView
from django.contrib.auth.views import LoginView

class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self,form):
        messages.error(self.request,'Invalid username or password')
        return super().form_invalid(form)

urlpatterns = [
        path('', views.PaymentView, name='payment'),
        path('payment/',views.PaymentView, name='payment'),
        path('login/',MyLoginView.as_view(), name='login'),
]
