# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from ..models import Local, Bitacora, Plato, Punto, Chat
from django.contrib.auth.models import User

import json, datetime

@login_required()
def index(request):
  return render_to_response('index.html', context_instance = RequestContext(request))

@login_required()
def blog(request):
  if request.method == 'POST':
    mensaje = request.POST.get('mensaje')
    post = Bitacora(mensaje = mensaje, hecho_por = request.user, local = request.session['local'], cuando = datetime.datetime.now())
    post.save()
    messages.success(request, 'Mensaje creado')
    
  posts = Bitacora.objects.filter(hecho_por = request.user).order_by('-cuando')
  context = {'posts': posts}
  return render_to_response('blog.html', context, context_instance = RequestContext(request))

@login_required()
def chat(request):

  if request.method == 'POST':
    mensaje = request.POST.get('mensaje')
    chat = Chat(mensaje = mensaje, hecho_por = request.user, cuando = datetime.datetime.now())
    chat.save()

    context = {'status': 'ok', 'mensaje': {
      'cuando': str(chat.cuando),
      'hecho_por': chat.hecho_por.username,
      'mensaje': chat.mensaje
    }}

    print context

    return HttpResponse(json.dumps(context), content_type="application/json")

  chat_messages = Chat.objects.all().order_by('cuando')[0:50]
  context = {'chat_messages': chat_messages}
  return render_to_response('chat.html', context, context_instance = RequestContext(request))

@login_required()
def carta(request):
  local = request.session['local']
  puntos = Punto.objects.filter(pertenece_a = local)
  platos = Plato.objects.filter(de_venta_en__in = puntos)

  for plato in platos:
    plato.theprecio = plato.precioplato_set.get(anio = 2013).precio

  context = {'platos': platos}
  return render_to_response('carta.html', context, context_instance = RequestContext(request))

def the_login(request):
  if(request.user.is_authenticated()):
    return HttpResponseRedirect(reverse('index'))
  else:
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      local = request.POST['local']

      user = authenticate(username = username, password = password)
      if user is not None:
        if user.is_active:
          login(request, user)
          request.session['local'] = Local.objects.get(pk = local)
          return HttpResponseRedirect(reverse('index'))
        else:
          messages.error(request, 'El usuario no está activo. Contacte con el administrador.')
      else:
        messages.error(request, 'Revise el usuario o la contraseña.')

    locales = Local.objects.all()
    usuarios = User.objects.all()
    context = {'locales': locales, 'usuarios': usuarios}
  
  return render_to_response('login.html', context, context_instance = RequestContext(request))

def the_logout(request):
  messages.success(request, 'Hasta pronto')
  logout(request)

  return HttpResponseRedirect(reverse('index'))