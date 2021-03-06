from django.conf.urls import patterns,url


urlpatterns = patterns('core.views',
  url(r'^$', 'index', name = 'index'),
  url(r'^login/$', 'the_login', name = 'the_login'),
  url(r'^logout/$', 'the_logout', name = 'the_logout'),

  # Pedidos.
  url(r'^pedido/$', 'pedido', name = 'pedido'),
  url(r'^pedido/lista/mozo/$', 'pedido_lista_mozo', name = 'pedido_lista_mozo'),
  url(r'^pedido/lista/cocina/$', 'pedido_lista_cocina', name = 'pedido_lista_cocina'),
  url(r'^pedido/lista/recepcion/$', 'pedido_lista_recepcion', name = 'pedido_lista_recepcion'),
  url(r'^pedido/crear/$', 'pedido_crear', name = 'pedido_crear'), 
  url(r'^pedido/quitar/$', 'pedido_quitar', name = 'pedido_quitar'), 
  url(r'^pedido/atender/$', 'pedido_atender', name = 'pedido_atender'), 
  url(r'^pedido/imprimir/$', 'pedido_imprimir', name = 'pedido_imprimir'), 
  url(r'^pedido/imprimir/consumo/(?P<id>.*)$', 'pedido_imprimir_consumo', name = 'pedido_imprimir_consumo'), 
  url(r'^pedido/imprimir/comanda/(?P<id>.*)$', 'pedido_imprimir_comanda', name = 'pedido_imprimir_comanda'), 
  url(r'^pedido/imprimir/boleta/(?P<id>.*)$', 'pedido_imprimir_boleta', name = 'pedido_imprimir_boleta'), 
  url(r'^pedido/imprimir/factura/(?P<id>.*)$', 'pedido_imprimir_factura', name = 'pedido_imprimir_factura'),

  # Reportes
  url(r'^reporte/pedido/fecha/$', 'reporte_pedido_fecha', name = 'reporte_pedido_fecha'), 
  url(r'^reporte/pedido/habitacion/$', 'reporte_pedido_habitacion', name = 'reporte_pedido_habitacion'), 
  url(r'^reporte/pedido/mozo/$', 'reporte_pedido_mozo', name = 'reporte_pedido_mozo'), 

  url(r'^reporte/documento/comanda/$', 'reporte_documento_comanda', name = 'reporte_documento_comanda'),
  url(r'^reporte/documento/consumo/$', 'reporte_documento_consumo', name = 'reporte_documento_consumo'),
  url(r'^reporte/documento/boleta/$', 'reporte_documento_boleta', name = 'reporte_documento_boleta'), 
  url(r'^reporte/documento/factura/$', 'reporte_documento_factura', name = 'reporte_documento_factura'), 

  url(r'^reporte/mozo/masvendido/$', 'mas_vendido_mozo', name = 'mas_vendido_mozo'), 
  url(r'^reporte/plato/ranking/$', 'ranking_platos', name = 'ranking_platos'), 

  #Completo
  url(r'^pedido/lista/completo/mozo/$', 'pedido_lista_completo_mozo', name = 'pedido_lista_completo_mozo'),

  # Varios.
  url(r'^blog/$', 'blog', name = 'blog'),
  url(r'^chat/$', 'chat', name = 'chat'),
  url(r'^carta/$', 'carta', name = 'carta'),
  url(r'^clientes/$', 'clientes', name = 'clientes'),
  url(r'^clientes/agregar$', 'cliente_agregar', name = 'cliente_agregar'),
  url(r'^checkout/$', 'checkout', name = 'checkout'),

  # JSON.
  url(r'^json/cliente/(?P<q>.*)/$', 'json_clientes_local', name = 'json_clientes_local'),
  url(r'^json/plato/(?P<q>.*)/$', 'json_platos_local', name = 'json_platos_local'),
  url(r'^json/pedido/habitacion/(?P<id>.*)/$', 'pedido_lista_habitacion', name = 'pedido_lista_habitacion'),
  url(r'^json/pedido/externos/$', 'pedido_lista_externos', name = 'pedido_lista_externos'),
  url(r'^json/consumo/(?P<id>.*)/$', 'tiene_consumo', name = 'tiene_consumo'),
  url(r'^json/comanda/(?P<id>.*)/$', 'tiene_comanda', name = 'tiene_comanda'),
  url(r'^json/boleta/(?P<id>.*)/$', 'tiene_boleta', name = 'tiene_boleta'),
  url(r'^json/factura/(?P<id>.*)/$', 'tiene_factura', name = 'tiene_factura'),
  url(r'^json/pagar/(?P<id>.*)/$', 'json_pagar', name = 'json_pagar'),
)