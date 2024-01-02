from django.contrib import admin
from django.urls import path
from django_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.statements,name = "statements"),
    path('report-form',views.home , name="home"),
    path('statement/<str:pk>/',views.statement,name = "statement"),
    path('statement_delete/<str:pk>/',views.statement_delete,name = "statement_delete"),
    path('login/',views.login_v,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout_v,name='logout'),
]
