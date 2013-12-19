# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Sum
import json, datetime

from ..models import Cliente, Pedido, Habitacion, Comanda, Consumo, Boleta, Factura, Plato, PedidoDetalle
from ..utils import pedido_json, strtotime, documento_json

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

@login_required
def reporte_pedido_mozo(request):

  if request.method == 'POST':
    inicio = request.POST.get('inicio')
    fin = request.POST.get('fin')
    mozo = request.POST.get('mozo')

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

@login_required
def reporte_documento_comanda(request):
  if request.method == 'POST':
    numero = request.POST.get('numero')

    try:
      documento = Comanda.objects.get(numero = numero)
      context = documento_json(documento, 'comanda')
    except:
      context = {}          
    
    return HttpResponse(json.dumps(context), content_type="application/json")
  return render_to_response('reporte-documento-comanda.html', context_instance = RequestContext(request))

@login_required
def reporte_documento_consumo(request):
  if request.method == 'POST':
    numero = request.POST.get('numero')

    try:
      documento = Consumo.objects.get(numero = numero)
      context = documento_json(documento, 'consumo')
    except:
      context = {}          
    
    return HttpResponse(json.dumps(context), content_type="application/json")
  return render_to_response('reporte-documento-consumo.html', context_instance = RequestContext(request))

@login_required
def reporte_documento_boleta(request):
  if request.method == 'POST':
    numero = request.POST.get('numero')

    try:
      documento = Boleta.objects.get(numero = numero)
      context = documento_json(documento, 'boleta')
    except:
      context = {}          
    
    return HttpResponse(json.dumps(context), content_type="application/json")
  return render_to_response('reporte-documento-boleta.html', context_instance = RequestContext(request))

@login_required
def reporte_documento_factura(request):
  if request.method == 'POST':
    numero = request.POST.get('numero')

    try:
      documento = Factura.objects.get(numero = numero)
      context = documento_json(documento, 'factura')
    except:
      context = {}          
    
    return HttpResponse(json.dumps(context), content_type="application/json")
  return render_to_response('reporte-documento-factura.html', context_instance = RequestContext(request))

@login_required
def mas_vendido_mozo(request):

  if request.method == 'POST':
    inicio = request.POST.get('inicio')
    fin = request.POST.get('fin')
    mozo = request.POST.get('mozo')

    data = []

    platos = Plato.objects.all()

    if inicio != '' and fin != '':
      inicio = strtotime(request.POST.get('inicio'))
      fin = strtotime(request.POST.get('fin'))
      detalles = PedidoDetalle.objects.filter(
        pertenece_al_pedido__hecho_por = mozo,
        pertenece_al_pedido__cuando__range = (inicio, fin))
    else:
      detalles = PedidoDetalle.objects.filter(
        pertenece_al_pedido__hecho_por = mozo
        )

    for plato in platos:
      total = detalles.filter(plato = plato).aggregate(total = Sum('cantidad'))
      total = total['total']
      if total is None:
        total = 0
        
      data.append({'plato': plato.nombre, 'total': total})

    return HttpResponse(json.dumps(data), content_type="application/json")

  mozos = User.objects.filter(groups__name = 'Mozos')
  context = {'mozos': mozos}
  return render_to_response('mas-vendido-mozo.html', context, context_instance = RequestContext(request))