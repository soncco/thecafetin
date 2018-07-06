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

  showDoc = function() {
    what = $(this).data('what');
    id = $(this).data('id');

    frameSrc = '/pedido/imprimir/' + what + '/' + id;
    $('iframe').attr("src", frameSrc);
    $('#printModal').modal({show: true});
  }

  parseDocumentos = function(pedido) {
    id = pedido.id;
    documentos = pedido.documentos;

    $ul = $('<ul class="list-unstyled"></ul>');
    $li = $('<li></li>');
    $a = $('<a href="#" class="btn btn-default print-doc"></a>');
    if(pedido.visitante == '') {
      if(documentos.comanda > 0){
        $li.clone().html($a.clone()
          .data('what', 'comanda')
          .data('id', id)
          .text('Comanda nro: ' + documentos.comanda))
        .appendTo($ul);
      } 
      if(documentos.consumo > 0){
        $li.clone().html($a.clone()
          .data('what', 'consumo')
          .data('id', id)
          .text('Consumo nro: ' + documentos.consumo))
        .appendTo($ul);
      }
      if(documentos.boleta > 0) {
        $li.clone().html($a.clone()
          .data('what', 'boleta')
          .data('id', id)
          .text('Boleta nro: ' + documentos.boleta))
        .appendTo($ul);
      }
      if(documentos.factura > 0) {
        $li.clone().html($a.clone()
          .data('what', 'factura')
          .data('id', id)
          .text('Factura nro: ' + documentos.factura))
        .appendTo($ul);
      }
    } else {
      if(documentos.comanda > 0) {
        $li.clone().html($a.clone()
          .data('what', 'comanda')
          .data('id', id)
          .text('Comanda nro: ' + documentos.comanda))
        .appendTo($ul);
      }
      if(documentos.boleta > 0) {
        $li.clone().html($a.clone()
          .data('what', 'boleta')
          .data('id', id)
          .text('Boleta nro: ' + documentos.boleta))
        .appendTo($ul);
      }
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
    $td.clone().addClass('btn-group').html(parseDocumentos(pedido)).appendTo($tr);

    // Crea la fila.
    $tr
      .attr('id', 'row-' + pedido.id)
      .prependTo($tbody);

    $tr.delegate('.print-doc', 'click', showDoc);

  };

  // Parsea pedidos de JSON a una tabla HTML.
  parsePedidos = function(pedidos) {
    for(i = 0; i < pedidos.length; i++) {
      row = pedidos[i];
      parsePedido(row);
    }
  };

  printDoc = function() {
    var id = $(this).data('id');
    var what = $(this).data('what');

    frameSrc = '/pedido/imprimir/' + what + '/' + id;
    $('iframe').attr("src", frameSrc);
    $('#printModal').modal({show: true});
  };

  // Muestra una ventana con el comprobante.
  $('.comanda').click(printDoc);
  $('.consumo').click(printDoc);
  $('.boleta').click(printDoc);
  $('.factura').click(printDoc);

})(jQuery);