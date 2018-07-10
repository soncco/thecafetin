from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q

from ..models import Local, Bitacora, Plato, Punto, Chat, Cliente, Habitacion
from ..utils import current_year
from django.contrib.auth.models import User

import json, datetime

@login_required()
def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))

@login_required()
def blog(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        cuando = request.POST.get('cuando')
        post = Bitacora(mensaje = mensaje, hecho_por = request.user, local = request.session['local'], cuando = cuando)
        post.save()
        messages.success(request, 'Mensaje creado')
        

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    rango = request.GET.get('rango')

    if (rango is None):
        posts = Bitacora.objects.filter(
            cuando__range = (today_min, today_max),
        ).order_by('-cuando')
    else:
        posts = Bitacora.objects.filter(
            cuando = rango
        )

    context = {'posts': posts, 'rango': rango}
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

        return HttpResponse(json.dumps(context), content_type="application/json")

    chat_messages = Chat.objects.all().order_by('-cuando')[0:50]
    context = {'chat_messages': reversed(chat_messages)}
    return render_to_response('chat.html', context, context_instance = RequestContext(request))

@login_required()
def clientes(request):
    clientes = Cliente.objects.filter(hospedado_en__pertenece_a = request.session['local'], activo = True)
    clientes = clientes.filter(~Q(nombres = 'Foraneo')).order_by('hospedado_en')
    context = {'clientes': clientes}
    return render_to_response('clientes.html', context, context_instance = RequestContext(request))

@login_required()
def cliente_agregar(request):
    if request.method == 'POST':
        habitacion = Habitacion.objects.get(pk = request.POST.get('hospedado_en'))

        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        hospedado_en = habitacion
        pais = request.POST.get('pais')
        documento = request.POST.get('documento')
        activo = request.POST.get('activo')
        ingreso_pais = request.POST.get('ingreso_pais')
        ingreso = request.POST.get('ingreso')
        salida = request.POST.get('salida')

        cliente = Cliente(
            nombres = nombres,
            apellidos = apellidos,
            hospedado_en = hospedado_en,
            pais = pais,
            documento = documento,
            activo = activo,
            ingreso_pais = ingreso_pais,
            ingreso = ingreso
        )

        if salida != '':
            cliente.salida = salida

        cliente.save()
        messages.success(request, 'Se ha creado el cliente %s' % (cliente))
        return HttpResponseRedirect(reverse('clientes'))

    habitaciones = Habitacion.objects.filter(pertenece_a = request.session['local'])
    context = {'habitaciones': habitaciones}
    return render_to_response('cliente-agregar.html', context, context_instance = RequestContext(request))    

@login_required()
def checkout(request):
    pk = request.POST.get('id')
    cliente = Cliente.objects.get(pk = pk)
    cliente.salida = datetime.datetime.now()
    cliente.activo = False
    cliente.save()

    return HttpResponse('')

@login_required()
def carta(request):
    local = request.session['local']
    puntos = Punto.objects.filter(pertenece_a = local)
    platos = Plato.objects.filter(de_venta_en__in = puntos)

    for plato in platos:
        try:
            plato.theprecio = plato.precioplato_set.get(anio = current_year()).precio
        except:
            plato.theprecio = plato.precioplato_set.filter(anio = current_year())[0].precio

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
        usuarios = User.objects.filter(is_active = True)
        context = {'locales': locales, 'usuarios': usuarios}
    
    return render_to_response('login.html', context, context_instance = RequestContext(request))

def the_logout(request):
    messages.success(request, 'Hasta pronto')
    logout(request)

    return HttpResponseRedirect(reverse('index'))
