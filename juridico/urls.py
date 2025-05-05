from django.urls import path
from .views import auth, home, registers, meet, analitico

urlpatterns = [
    path('', auth.login_usuario, name='login'),
    path('logout/', auth.logout_usuario, name='logout'),
    path('home/', home.home, name='home'),
    path('deletar_advogado/<int:id>/', home.deletar_advogado, name='deletar_advogado'), 
    path('editar_processo', home.editar_processo, name='editar_processo'), 
    path('excluir_processo/<int:id>/', home.excluir_processo, name='excluir_processo'),
    path('exportar_processos/', home.exportar_processos_excel, name='exportar_processos_excel'),
    path('exportar-pdf/<str:numero_processo>/', home.exportar_processos_pdf, name='exportar_processos_pdf'),
    path('download-planilha-modelo/', home.download_planilha_modelo, name='download_planilha_modelo'), 
    path('registros/', registers.registros, name='registros'),
    path('reunioes/', meet.reunioes, name='reunioes'),
    path('api/reunioes/', meet.api_reunioes, name='api_reunioes'),
    path("get-processos/", meet.get_processos_por_autor, name="get_processos_por_autor"), 
    path('analitico/', analitico.analitico, name='analitico'),
]