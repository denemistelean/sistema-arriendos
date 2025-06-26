# arriendos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Arriendo, Pago
from .forms import ArriendoForm, PagoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from django.http import HttpResponse

@login_required
def lista_arriendos(request):
    arriendos = Arriendo.objects.all()
    return render(request, 'arriendos/lista_arriendos.html', {'arriendos': arriendos})

def crear_arriendo(request):
    form = ArriendoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_arriendos')
    return render(request, 'arriendos/form_arriendo.html', {'form': form})

def detalle_arriendo(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)
    pagos = arriendo.pagos.all()
    return render(request, 'arriendos/detalle_arriendo.html', {'arriendo': arriendo, 'pagos': pagos})

def registrar_pago(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)
    form = PagoForm(request.POST or None)
    if form.is_valid():
        pago = form.save(commit=False)
        pago.arriendo = arriendo
        pago.save()
        return redirect('detalle_arriendo', arriendo_id=arriendo.id)
    return render(request, 'arriendos/form_pago.html', {'form': form, 'arriendo': arriendo})


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('lista_arriendos')
    return render(request, 'registration/register.html', {'form': form})

def exportar_arriendo_pdf(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)
    pagos = arriendo.pagos.all()
    template = get_template('arriendos/pdf_arriendo.html')
    html = template.render({'arriendo': arriendo, 'pagos': pagos})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="arriendo_{arriendo.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def exportar_arriendo_excel(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)
    pagos = arriendo.pagos.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pagos Arriendo"

    # Cabecera
    ws.append(['Nombre Arriendo', arriendo.nombre])
    ws.append([])
    ws.append(['Fecha', 'Año', 'Mes', 'Tipo de Pago'])

    # Filas
    for p in pagos:
        ws.append([p.fecha, p.ano, p.mes, p.tipo_pago])

    # Respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=arriendo_{arriendo.id}.xlsx'
    wb.save(response)
    return response