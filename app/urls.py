from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('add_account', views.add_customer, name='add_customer'),
    path('account_ledger', views.account_ledger, name='account_ledger'),
    path('cash_book', views.cash_book, name='cash_book'),
    path('reports', views.reports, name='reports'),
    path("backup", views.backup_database, name="backup"),
    path("export_csv/", views.export_csv, name="export_csv"),
    
]