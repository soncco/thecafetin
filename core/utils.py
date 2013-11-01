# -*- coding: utf-8 -*-

from models import Comanda, ComandaDetalle, Consumo, ConsumoDetalle, Boleta, BoletaDetalle, Factura, FacturaDetalle
from datetime import datetime

from django.utils.encoding import smart_str, smart_unicode

def pedido_json(pedido):
  cliente = pedido.para
  fecha = pedido.cuando
  tiene_comanda = 'false'
  tiene_consumo = 'false'
  visitor = ''
  try:
    visitor = pedido.visitante.nombres
  except:
    visitor = ''

  # Detalles
  detalles = []
  for detalle in pedido.pedidodetalle_set.all():
    cantidad = detalle.cantidad
    precio = float(detalle.plato.precioplato_set.get(anio = 2013).precio)
    sub = cantidad * precio
    if detalle.plato.tipo.recibo == 'D':
      tiene_consumo = 'true'
    if detalle.plato.tipo.recibo == 'C':
      tiene_comanda = 'true'

    detalles.append({
      'cantidad': cantidad,
      'plato': detalle.plato.nombre,
      'precio': precio,
      'sub': sub
    })

  # Documentos

  docs = {}

  try:
    docs['comanda'] = pedido.comanda.numero
  except:
    docs['comanda'] = 0

  try:
    docs['consumo'] = pedido.consumo.numero
  except:
    docs['consumo'] = 0

  try:
    docs['boleta'] = pedido.boleta.numero
  except:
    docs['boleta'] = 0

  try:
    docs['factura'] = pedido.factura.numero
  except:
    docs['factura'] = 0

  thepedido = {
    'id': pedido.id,
    'para': cliente.nombres + ' ' + cliente.apellidos,
    'estado': pedido.estado,
    'comentarios': pedido.notas,
    'detalles': detalles,
    'hecho_por': pedido.hecho_por.first_name,
    'fecha': str(pedido.cuando),
    'punto': pedido.punto.id,
    'tiene_comanda': tiene_comanda,
    'tiene_consumo': tiene_consumo,
    'visitante': smart_str(visitor),
    'documentos': docs
  }

  return thepedido

def documento_json(documento, tipo):

  numero = documento.numero
  cliente = str(documento.pedido.para)
  fecha = documento.fecha
  total = documento.total

  if tipo == 'comanda':
    collection = documento.comandadetalle_set.all()
  if tipo == 'consumo':
    collection = documento.consumodetalle_set.all()
  if tipo == 'boleta':
    collection = documento.boletadetalle_set.all()
  if tipo == 'factura':
    collection = documento.facturadetalle_set.all()

  # Detalles
  detalles = []
  for detalle in collection:
    cantidad = detalle.cantidad
    plato = detalle.plato
    unitario = detalle.unitario
    subtotal = detalle.subtotal

    detalles.append({
      'cantidad': cantidad,
      'plato': detalle.plato.nombre,
      'unitario': float(unitario),
      'subtotal': float(subtotal)
    })

  data = {
    'numero': numero,
    'fecha': str(fecha),
    'cliente': cliente,
    'total': float(total),
    'pedido': documento.pedido.id,
    'detalles': detalles
  }

  return data


def total_pedido(pedido):
  total = 0
  for detalle in pedido.pedidodetalle_set.all():
    precio = detalle.plato.precioplato_set.get(anio = 2013).precio
    cantidad = detalle.cantidad
    total +=  precio * cantidad

  return total

def total_pedido_tipo(pedido, tipo):
  total = 0
  for detalle in pedido.pedidodetalle_set.all():
    if detalle.plato.tipo.recibo == tipo:
      precio = detalle.plato.precioplato_set.get(anio = 2013).precio
      cantidad = detalle.cantidad
      total +=  precio * cantidad

  return total

def crear_comanda(request, pedido):
  local = request.session['local']
  total = total_pedido_tipo(pedido, 'C')

  if Comanda.objects.filter(pedido = pedido).count > 0:
    pass

  comanda = Comanda(local = local, pedido = pedido, total = total)
  comanda.save()

  for detalle in pedido.pedidodetalle_set.all():
    if detalle.plato.tipo.recibo == 'C':
      plato = detalle.plato
      cantidad = detalle.cantidad
      unitario = detalle.plato.precioplato_set.get(anio = 2013).precio
      subtotal = cantidad * unitario
      cd = ComandaDetalle(pertenece_a_comanda = comanda, plato = plato, cantidad = cantidad, unitario = unitario, subtotal = subtotal)
      cd.save()

def crear_comanda_externo(request, pedido):
  local = request.session['local']
  total = total_pedido(pedido)

  if Comanda.objects.filter(pedido = pedido).count > 0:
    pass

  comanda = Comanda(local = local, pedido = pedido, total = total)
  comanda.save()

  for detalle in pedido.pedidodetalle_set.all():
    plato = detalle.plato
    cantidad = detalle.cantidad
    unitario = detalle.plato.precioplato_set.get(anio = 2013).precio
    subtotal = cantidad * unitario
    cd = ComandaDetalle(pertenece_a_comanda = comanda, plato = plato, cantidad = cantidad, unitario = unitario, subtotal = subtotal)
    cd.save()

def crear_consumo(request, pedido, number):
  local = request.session['local']
  total = total_pedido_tipo(pedido, 'D')
  numero = number

  if Consumo.objects.filter(pedido = pedido).count > 0:
    pass

  consumo = Consumo(local = local, pedido = pedido, total = total, numero = numero)
  consumo.save()

  for detalle in pedido.pedidodetalle_set.all():
    if detalle.plato.tipo.recibo == 'D':
      plato = detalle.plato
      cantidad = detalle.cantidad
      unitario = detalle.plato.precioplato_set.get(anio = 2013).precio
      subtotal = cantidad * unitario
      cd = ConsumoDetalle(pertenece_a_consumo = consumo, plato = plato, cantidad = cantidad, unitario = unitario, subtotal = subtotal)
      cd.save()


def crear_boleta(request, pedido, number):
  local = request.session['local']
  total = total_pedido_tipo(pedido, 'C')
  numero = number

  if Boleta.objects.filter(pedido = pedido).count > 0:
    pass

  boleta = Boleta(local = local, pedido = pedido, total = total, numero = numero)
  boleta.save()

  for detalle in pedido.pedidodetalle_set.all():
    if detalle.plato.tipo.recibo == 'C':
      plato = detalle.plato
      cantidad = detalle.cantidad
      unitario = detalle.plato.precioplato_set.get(anio = 2013).precio
      subtotal = cantidad * unitario
      bd = BoletaDetalle(pertenece_a_boleta = boleta, plato = plato, cantidad = cantidad, unitario = unitario, subtotal = subtotal)
      bd.save()

def crear_boleta_externo(request, pedido, number):
  local = request.session['local']
  total = total_pedido(pedido)
  numero = number

  if Boleta.objects.filter(pedido = pedido).count > 0:
    pass

  boleta = Boleta(local = local, pedido = pedido, total = total, numero = numero)
  boleta.save()

  for detalle in pedido.pedidodetalle_set.all():
    plato = detalle.plato
    cantidad = detalle.cantidad
    unitario = detalle.plato.precioplato_set.get(anio = 2013).precio
    subtotal = cantidad * unitario
    bd = BoletaDetalle(pertenece_a_boleta = boleta, plato = plato, cantidad = cantidad, unitario = unitario, subtotal = subtotal)
    bd.save()

def crear_factura(request, pedido, number):
  local = request.session['local']
  total = total_pedido_tipo(pedido, 'D')
  numero = number

  if Factura.objects.filter(pedido = pedido).count > 0:
    pass

  factura = Factura(local = local, pedido = pedido, total = total, numero = numero)
  factura.save()

  for detalle in pedido.pedidodetalle_set.all():
    if detalle.plato.tipo.recibo == 'D':
      plato = detalle.plato
      cantidad = detalle.cantidad
      unitario = detalle.plato.precioplato_set.get(anio = 2013).precio
      subtotal = cantidad * unitario
      fd = FacturaDetalle(pertenece_a_factura = factura, plato = plato, cantidad = cantidad, unitario = unitario, subtotal = subtotal)
      fd.save()

def strtotime(mystring):
  format = '%Y-%m-%d'
  return datetime.strptime(mystring, format)