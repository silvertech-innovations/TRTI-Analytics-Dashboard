from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Home & Dashboard
    path('', views.homepage, name='homepage'),
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('extract/', views.extract_view, name='extract'),
    

    # 🔹 Authentication Routes
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 🔹 Static Pages
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),

    # 🔹 Utility & Session Handling
    path('session-timeout/', views.session_timeout_view, name='session-timeout'),
    path('auth-status/', views.check_auth_status, name='auth-status'),
    path('get-updated-data/', views.get_updated_data, name='get_updated_data'),
]