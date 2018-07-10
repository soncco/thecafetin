from django.urls import path, re_path
from core.views import main
from core.views import pedido

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
    path( 'pedido/imprimir/',pedido.pedido_imprimir, name = 'pedido_imprimir' ), 
]