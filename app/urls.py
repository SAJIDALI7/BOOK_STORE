from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from .forms import UserLoginForm, MyPasswordChangeForm, MypasswordResetForm, MySetPasswordResetForm
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='/'),
    path('productdetail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('fiction/', views.fiction, name='fiction'),
    path('fiction/<slug:data>', views.fiction, name='fictiondata'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('account/login', auth_view.LoginView.as_view(template_name='app/login.html', form_class=UserLoginForm, success_url='/'), name='login'),
    path('logout', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/Password_change.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MypasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordResetForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('cart/', views.show_cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment, name='paymentdone'),
    path('orders/', views.order, name='orders'),
    path('del_item/<int:id>', views.delete_item, name='del_item'),
    path('email/', views.send_email.as_view(), name='email')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

