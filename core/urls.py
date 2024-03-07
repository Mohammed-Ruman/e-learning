
from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import handle_exception
from django.conf import settings
from django.conf.urls.static import static


handler404 = handle_exception
handler403 = handle_exception

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page,name='home'),
    path('course/',views.course_page,name='course'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('logout/',views.logout_page,name='logout'),
    path('verify/<str:email>/', views.verify_otp, name='verify'),
    path('verify_login/<str:email>/', views.verify_otp_login, name='verify_login'),  
    path('teacher/dashboard',views.teacher_dashboard,name='teacher dashboard'),
    path('teacher/add',views.add_course,name='add course'),
    path('teacher/edit/<str:id>',views.edit_course,name='edit course'),
    path('teacher/delete/<str:id>',views.delete_course,name='delete course'),
    path('course/<str:name>',views.course_detail_page,name='course detail'),
    path('student/dashboard',views.student_dashboard,name='student dashboard'),
    path('student/payment/<str:name>',views.payment_page,name='payment'),
    path('payment/success/<int:id>',views.payment_success,name='payment status'),
    path('payment/failure/<int:id>',views.payment_failure,name='payment failure'),
    path('',include('paypal.standard.ipn.urls')),
    path('student/content/<str:name>',views.content_page,name='content'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
