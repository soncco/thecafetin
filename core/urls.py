from django.urls import path, re_path
from core.views import main
from core.views import pedido
from core.views import reporte
from core.views import thedocs
from core.views import thejson
from core.views import thepdf

urlpatterns = [
    # Main
    path( '', main.index, name = 'index' ),
    path( 'login/', main.the_login, name = 'the_login' ),
    path( 'logout/', main.the_logout, name = 'the_logout' ),

    # Pedidos
    path( 'pedido/', pedido.pedido, name = 'pedido' ),
    path( 'pedido/lista/mozo/', pedido.pedido_lista_mozo, name = 'pedido_lista_mozo' ),
    path( 'pedido/lista/cocina/', pedido.pedido_lista_cocina, name = 'pedido_lista_cocina' ),
    path( 'pedido/lista/recepcion/', pedido.pedido_lista_recepcion, name = 'pedido_lista_recepcion' ),
    path( 'pedido/crear/', pedido.pedido_crear, name = 'pedido_crear' ), 
    path( 'pedido/quitar/', pedido.pedido_quitar, name = 'pedido_quitar' ), 
    path( 'pedido/atender/', pedido.pedido_atender, name = 'pedido_atender' ), 
    path( 'pedido/imprimir/', pedido.pedido_imprimir, name = 'pedido_imprimir' ),
    re_path( r'^pedido/imprimir/consumo/(?P<id>.*)$', thepdf.pedido_imprimir_consumo, name = 'pedido_imprimir_consumo' ), 
    re_path( r'^pedido/imprimir/comanda/(?P<id>.*)$', thepdf.pedido_imprimir_comanda, name = 'pedido_imprimir_comanda' ), 
    re_path( r'^pedido/imprimir/boleta/(?P<id>.*)$', thepdf.pedido_imprimir_boleta, name = 'pedido_imprimir_boleta' ), 
    re_path( r'^pedido/imprimir/factura/(?P<id>.*)$', thepdf.pedido_imprimir_factura, name = 'pedido_imprimir_factura' ),

    # Reportes
    path( 'reporte/pedido/fecha/', reporte.reporte_pedido_fecha, name = 'reporte_pedido_fecha' ), 
    path( 'reporte/pedido/habitacion/', reporte.reporte_pedido_habitacion, name = 'reporte_pedido_habitacion' ), 
    path( 'reporte/pedido/mozo/', reporte.reporte_pedido_mozo, name = 'reporte_pedido_mozo' ), 
    path( 'reporte/documento/comanda/', reporte.reporte_documento_comanda, name = 'reporte_documento_comanda' ),
    path( 'reporte/documento/consumo/', reporte.reporte_documento_consumo, name = 'reporte_documento_consumo' ),
    path( 'reporte/documento/boleta/', reporte.reporte_documento_boleta, name = 'reporte_documento_boleta' ), 
    path( 'reporte/documento/factura/', reporte.reporte_documento_factura, name = 'reporte_documento_factura' ), 
    path( 'reporte/mozo/masvendido/', reporte.mas_vendido_mozo, name = 'mas_vendido_mozo' ), 
    path( 'reporte/plato/ranking/', reporte.ranking_platos, name = 'ranking_platos' ), 

    #Completo
    path( 'pedido/lista/completo/mozo/', pedido.pedido_lista_completo_mozo, name = 'pedido_lista_completo_mozo' ),

    # Varios.
    path( 'blog/', main.blog, name = 'blog' ),
    path( 'chat/', main.chat, name = 'chat' ),
    path( 'carta/', main.carta, name = 'carta' ),
    path( 'clientes/', main.clientes, name = 'clientes' ),
    path( 'clientes/agregar/', main.cliente_agregar, name = 'cliente_agregar' ),
    path( 'checkout/', main.checkout, name = 'checkout' ),

    # JSON.
    re_path( r'^json/cliente/(?P<q>.*)/$', thejson.json_clientes_local, name = 'json_clientes_local' ),
    re_path( r'^json/plato/(?P<q>.*)/$', thejson.json_platos_local, name = 'json_platos_local' ),
    re_path( r'^json/pedido/habitacion/(?P<id>.*)/$', thejson.pedido_lista_habitacion, name = 'pedido_lista_habitacion' ),
    re_path( r'^json/pedido/externos/$', thejson.pedido_lista_externos, name = 'pedido_lista_externos' ),
    re_path( r'^json/consumo/(?P<id>.*)/$', thedocs.tiene_consumo, name = 'tiene_consumo' ),
    re_path( r'^json/comanda/(?P<id>.*)/$', thedocs.tiene_comanda, name = 'tiene_comanda' ),
    re_path( r'^json/boleta/(?P<id>.*)/$', thedocs.tiene_boleta, name = 'tiene_boleta' ),
    re_path( r'^json/factura/(?P<id>.*)/$', thedocs.tiene_factura, name = 'tiene_factura' ),
    re_path( r'^json/pagar/(?P<id>.*)/$', pedido.json_pagar, name = 'json_pagar' ),
]