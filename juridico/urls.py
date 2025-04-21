from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),
    path('home/', views.home, name='home'),
    path('registros/', views.registros, name='registros'),
    path('logout/', views.logout_usuario, name='logout'),
    path('deletar_advogado/<int:id>/', views.deletar_advogado, name='deletar_advogado'), 
    path('exportar_processos/', views.exportar_processos_excel, name='exportar_processos_excel'),
    path('download-planilha-modelo/', views.download_planilha_modelo, name='download_planilha_modelo'), 
]