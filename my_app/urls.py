from django.urls import path, include
from my_app import views, user_login
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    
    path('', views.home, name='Home'),
    path('base', views.Base, name='Base'),
    path('courses', views.available_courses, name='courses'),
    path('search/', views.search_course, name='search-course'),
    path('product/filter-data', views.filter_data, name='filter-data'),
    path('course/<slug:slug>', views.course_detail, name='course_details'),
    path('contact', views.ContactUs, name='ContactUs'),
    path('aboutus', views.AboutUs, name='AboutUs'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', user_login.Register, name='register'),
    path('login', user_login.Login, name='login'),
    path('accounts/profile', user_login.Profile, name='profile'),
    path('accounts/profile/update', user_login.Profile_Update, name='updateprofile'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('checkout/<slug:slug>', views.checkout, name='checkout'),
    path('my_course', views.my_course, name='my_course'),
    path('order/<int:course_id>', views.order, name='order'),
    path('order/sucess/', views.sucess, name='sucess'),
    path('contactform/<int:course_id>', views.contactform, name='contactform'),
    path('watch_course/<str:slug>', views.Watch_Course, name='watch_course')

]
