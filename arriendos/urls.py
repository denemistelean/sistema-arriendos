# arriendos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_arriendos, name='lista_arriendos'),
    path('nuevo/', views.crear_arriendo, name='crear_arriendo'),
    path('<int:arriendo_id>/', views.detalle_arriendo, name='detalle_arriendo'),
    path('<int:arriendo_id>/pago/', views.registrar_pago, name='registrar_pago'),
    path('<int:arriendo_id>/exportar/pdf/', views.exportar_arriendo_pdf, name='exportar_arriendo_pdf'),
    path('<int:arriendo_id>/exportar/excel/', views.exportar_arriendo_excel, name='exportar_arriendo_excel'),

]
