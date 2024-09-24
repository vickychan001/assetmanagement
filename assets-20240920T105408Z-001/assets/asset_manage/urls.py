from django.urls import path
from . import views

urlpatterns = [
    path('manager_signup/', views.manager_signup, name="manger_signup"),
    path('employee_signup/', views.employee_signup, name="employee_signup"),
    path('asset_assign', views.asset_assigned_update, name="asset_assign"),
    path('employee_view/', views.employee_view, name="employee_view"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('refresh/', views.refresh_view, name="login"),
    path('add_asset/', views.add_asset, name="add_asset")
]
