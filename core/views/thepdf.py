from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_xhtml2pdf.utils import generate_pdf

from ..models import Pedido, Consumo, Comanda, Boleta, Factura
from ..utils import total_pedido

from ..numword.numword_es import cardinal

@login_required
def pedido_imprimir_comanda(request, id):
    
    pedido = Pedido.objects.get(id = id)

    comanda = Comanda.objects.get(pedido = pedido)
    
    resp = HttpResponse(content_type = 'application/pdf')
    context = {'comanda': comanda}
    result = generate_pdf('pdf/comanda.html', file_object = resp, context = context)
    return result

@login_required
def pedido_imprimir_consumo(request, id):
    pedido = Pedido.objects.get(id = id)

    consumo = Consumo.objects.get(pedido = pedido)
    
    resp = HttpResponse(content_type = 'application/pdf')
    context = {'consumo': consumo}
    result = generate_pdf('pdf/consumo.html', file_object = resp, context = context)
    return result

@login_required
def pedido_imprimir_boleta(request, id):
    pedido = Pedido.objects.get(id = id)

    boleta = Boleta.objects.get(pedido = pedido)

    boleta.totalnum = cardinal(boleta.total)
    
    resp = HttpResponse(content_type = 'application/pdf')
    context = {'boleta': boleta}
    result = generate_pdf('pdf/boleta.html', file_object = resp, context = context)
    return result

@login_required
def pedido_imprimir_factura(request, id):
    pedido = Pedido.objects.get(id = id)

    factura = Factura.objects.get(pedido = pedido)

    factura.totalnum = cardinal(factura.total)

    resp = HttpResponse(content_type = 'application/pdf')
    context = {'factura': factura}
    result = generate_pdf('pdf/factura.html', file_object = resp, context = context)
    return result
