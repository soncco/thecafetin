# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import json, datetime

from ..models import Cliente, Pedido, Habitacion
from ..utils import pedido_json, strtotime

@login_required
def reporte_pedido_fecha(request):
  if request.method == 'POST':
    inicio = strtotime(request.POST.get('inicio'))
    fin = strtotime(request.POST.get('fin'))

    pedidos = []
    results = Pedido.objects.filter(cuando__range=(inicio, fin)).order_by('cuando')

    for pedido in results:
      pedidos.append(pedido_json(pedido))

    return HttpResponse(json.dumps(pedidos), content_type="application/json")

  return render_to_response('reporte-pedido-fecha.html', context_instance = RequestContext(request))

@login_required
def reporte_pedido_habitacion(request):

  if request.method == 'POST':
    inicio = request.POST.get('inicio')
    fin = request.POST.get('fin')
    habitacion = request.POST.get('habitacion')

    pedidos = []
    clientes = Cliente.objects.filter(hospedado_en = habitacion)

    if inicio != '' and fin != '':
      inicio = strtotime(request.POST.get('inicio'))
      fin = strtotime(request.POST.get('fin'))
      results = Pedido.objects.filter(cuando__range=(inicio, fin), para__in = clientes).order_by('cuando')
    else:
      results = Pedido.objects.filter(para__in = clientes)

    for pedido in results:
      pedidos.append(pedido_json(pedido))

    return HttpResponse(json.dumps(pedidos), content_type="application/json")

  habitaciones = Habitacion.objects.filter(pertenece_a = request.session['local'])
  context = {'habitaciones': habitaciones}
  return render_to_response('reporte-pedido-habitacion.html', context, context_instance = RequestContext(request))

def reporte_pedido_mozo(request):

  if request.method == 'POST':
    inicio = request.POST.get('inicio')
    fin = request.POST.get('fin')
    mozo = request.POST.get('mozo')

    print mozo

    pedidos = []

    if inicio != '' and fin != '':
      inicio = strtotime(request.POST.get('inicio'))
      fin = strtotime(request.POST.get('fin'))
      results = Pedido.objects.filter(cuando__range=(inicio, fin), hecho_por = mozo).order_by('cuando')
    else:
      results = Pedido.objects.filter(hecho_por = mozo)

    for pedido in results:
      pedidos.append(pedido_json(pedido))

    return HttpResponse(json.dumps(pedidos), content_type="application/json")

  mozos = User.objects.filter(groups__name = 'Mozos')
  context = {'mozos': mozos}
  return render_to_response('reporte-pedido-mozo.html', context, context_instance = RequestContext(request))

def reporte_documento_comanda(request):
  return render_to_response('reporte-documento-comanda.html', context_instance = RequestContext(request))

def reporte_documento_detalle(request):
  return render_to_response('reporte-documento-detalle.html', context_instance = RequestContext(request))

def reporte_documento_boleta(request):
  return render_to_response('reporte-documento-boleta.html', context_instance = RequestContext(request))

def reporte_documento_factura(request):
  return render_to_response('reporte-documento-factura.html', context_instance = RequestContext(request))
