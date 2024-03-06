
from django.contrib import admin
from django.urls import path
from main import views
from main.views import handle_exception
from django.conf import settings
from django.conf.urls.static import static


handler404 = handle_exception
handler403 = handle_exception

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page,name='home'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('logout/',views.logout_page,name='logout'),
    path('verify/<str:email>/', views.verify_otp, name='verify'),
    path('verify_login/<str:email>/', views.verify_otp_login, name='verify_login'),  
    path('teacher/dashboard',views.teacher_dashboard,name='teacher dashboard'),
    path('teacher/add',views.add_course,name='add course'),
    path('teacher/edit/<str:id>',views.edit_course,name='edit course'),
    path('teacher/delete/<str:id>',views.delete_course,name='delete course'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
