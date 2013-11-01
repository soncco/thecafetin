var cafetin = cafetin || {};

var $table = $('#pedido-lista'),
 $tbody = $table.find('tbody'),
 $total = $('.total');

(function($) {

  $('.datepicker').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'yy-mm-dd'
  });

  showDocs = function() {
    id = $(this).data('id');
    comanda = $(this).data('comanda');
    consumo = $(this).data('consumo');
    boleta = $(this).data('boleta');
    factura = $(this).data('factura');
    foraneo = $(this).data('foraneo');

    $('.comanda').data('id', id);
    $('.consumo').data('id', id);
    $('.boleta').data('id', id);
    $('.factura').data('id', id);

    $('.comanda').show();
    $('.consumo').show();
    $('.boleta').show();
    $('.factura').show();
    
    if(boleta == 'false') $('.boleta').hide();
    if(factura == 'false') $('.factura').hide();
    if(consumo == 'false') $('.consumo').hide();
    if(comanda == 'false') $('.comanda').hide();
    if(foraneo) {
      $('.comanda').show();
      $('.consumo').hide();
      $('.boleta').show();
      $('.factura').hide();
    }

    $('#theModal').modal({show: true});
  };

  // Parsea los detalles del pedido JSON en una lista HTML.
  parseDetalles = function(detalles) {
    $ul = $('<ul class="list-unstyled"></ul>');
    $li = $('<li></li>'); 

    for(j = 0; j < detalles.length; j++) {
      detalle = detalles[j];
      $li.clone().text(detalle.cantidad + ' x ' + detalle.plato).appendTo($ul);
    }
    return $ul;
  };

  parseDocumentos = function(pedido) {
    documentos = pedido.documentos;

    $ul = $('<ul class="list-unstyled"></ul>');
    $li = $('<li></li>'); 
    if(pedido.visitante == '') {
      if(documentos.comanda > 0) $li.clone().text('Comanda nro: ' + documentos.comanda).appendTo($ul);
      if(documentos.consumo > 0) $li.clone().text('Consumo nro: ' + documentos.consumo).appendTo($ul);
      if(documentos.boleta > 0)  $li.clone().text('Boleta nro: ' + documentos.boleta).appendTo($ul);
      if(documentos.factura > 0) $li.clone().text('Factura nro: ' + documentos.factura).appendTo($ul);
    } else {
      if(documentos.comanda > 0) $li.clone().text('Comanda nro: ' + documentos.comanda).appendTo($ul);
      if(documentos.boleta > 0)  $li.clone().text('Boleta nro: ' + documentos.boleta).appendTo($ul);      
    }
    
    return $ul;
  }

  // Parsea un pedido JSON en una fila de tabla HTML.
  parsePedido = function(pedido) {
    // Los elementos de las filas.
    $tr = $('<tr></tr>');
    $td = $('<td></td>');
    $status = $('<span class="btn btn-sm"></span>');
    $print = $('<button class="btn btn-sm btn-default print" data-id=""></button>').text('Ver documentos');
    
    if(pedido.visitante != '')
      $td.clone().text('Foraneo: ' + pedido.visitante).appendTo($tr);
    else
      $td.clone().text(pedido.para).appendTo($tr);
    $td.clone().html(parseDetalles(pedido.detalles)).appendTo($tr);
    $td.clone().text(pedido.comentarios).appendTo($tr);
    $td.clone().text(pedido.hecho_por).appendTo($tr);
    $td.clone().text(moment(pedido.fecha).calendar()).addClass('timeago').appendTo($tr);
    $td.clone().html($status.text(cafetin.estados[pedido.estado].texto).addClass(cafetin.estados[pedido.estado].clase)).appendTo($tr);
    $td.clone().html(parseDocumentos(pedido)).appendTo($tr);
    $td.clone()
        .append($print.data('id', pedido.id)
          .data('comanda', pedido.tiene_comanda)
          .data('consumo', pedido.tiene_consumo)
          .data('boleta', pedido.tiene_comanda)
          .data('factura', pedido.tiene_consumo)
          .data('foraneo', (pedido.visitante != ''))
          )
        .append($print.data('id', pedido.id))
      .addClass('actions')
      .appendTo($tr);

    // Agrega eventos a los botones.
    $tr.delegate('.print', 'click', showDocs);


    // Crea la fila.
    $tr
      .attr('id', 'row-' + pedido.id)
      .prependTo($tbody);

  };

  // Parsea pedidos de JSON a una tabla HTML.
  parsePedidos = function(pedidos) {
    for(i = 0; i < pedidos.length; i++) {
      row = pedidos[i];
      parsePedido(row);
    }
  };

})(jQuery);