var cafetin = cafetin || {};

cafetin.estados = {
  R: {
    'texto': 'Recibido',
    'clase': 'btn-danger'
  },
  A: {
    'texto': 'Atendido',
    'clase': 'btn-warning'
  },
  I: {
    'texto': 'Impreso',
    'clase': 'btn-info'
  },
  P: {
    'texto': 'Pagado',
    'clase': 'btn-success'
  }
};

(function($) {

  $('.timeago').timeago();

  // La tabla.
  var $table = $('#pedido-lista');
  var $tbody = $table.find('tbody');
  var $ver = $('.ver');
  var $verexterno = $('.ver-externo');

  // Imprime un pedido.
  printPedido = function() {
    id = $(this).data('id');
    boleta = $(this).data('boleta');
    factura = $(this).data('factura');
    foraneo = $(this).data('foraneo');

    $('.boleta').data('id', id);
    $('.factura').data('id', id);

    $('.boleta').show();
    $('.factura').show();
    
    if(boleta == 'false') $('.boleta').hide();
    if(factura == 'false') $('.factura').hide();
    if(foraneo) {
      $('.boleta').show();
      $('.factura').hide();
    }

    $('#theModal').modal({show: true});
  };

  printDoc = function() {
    var id = $(this).data('id');
    var what = $(this).data('what');
    var thedoc = 0;
    var number = 0;

    $.when(
      $.ajax({
        url: '/json/' + what + '/' + id + '/',
        dataType: 'json'
      })
    ).done(function(data) {
      thedoc = parseInt(data);
      if(!thedoc) {
        number = prompt('Ingresa el número de la ' + what + '.');
        if(number < 0) { // Fix.
          alert('Debes ingresar un número');
          return;
        }
      }

      $.post('/pedido/imprimir/', {
        'id': id,
        'what': what,
        'thedoc': thedoc,
        'number': number,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      }, function(data) {
        if(data.status == 'ok') {
          io.emit('pedido:pagar', data);
          $('#theModal').modal('hide');
        } else {
          alert('Hubo un error al imprimir el pedido, intenta nuevamente.');
        }
      });
    }); 
  }

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

  // Parsea un pedido JSON en una fila de tabla HTML.
  parsePedido = function(pedido) {
    // Los elementos de las filas.
    $tr = $('<tr></tr>');
    $td = $('<td></td>');
    $status = $('<span class="btn btn-sm"></span>');
    $pay = $('<button class="btn btn-sm btn-success pay" data-id=""></button>')
      .html($('<i class="icon icon-dollar"></i>'));
    
    if(pedido.visitante != '')
      $td.clone().text('Foraneo: ' + pedido.visitante).appendTo($tr);
    else
      $td.clone().text(pedido.para).appendTo($tr);
    $td.clone().html(parseDetalles(pedido.detalles)).appendTo($tr);
    $td.clone().text(pedido.comentarios).appendTo($tr);
    $td.clone().text(pedido.hecho_por).appendTo($tr);
    $td.clone().text(jQuery.timeago(pedido.fecha)).addClass('timeago').appendTo($tr);
    $td.clone().html($status.text(cafetin.estados[pedido.estado].texto).addClass(cafetin.estados[pedido.estado].clase)).appendTo($tr);
    $td.clone()
        .append($pay.data('id', pedido.id)
          .data('boleta', pedido.comanda)
          .data('factura', pedido.consumo)
          .data('foraneo', (pedido.visitante != ''))
          )
        .append($pay.data('id', pedido.id))
      .addClass('actions')
      .appendTo($tr);

    // Agrega eventos a los botones.
    $tr.delegate('.pay', 'click', printPedido);


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

  // Quita un pedido.
  io.on('pedido:quitado', function(data) {
    $tbody.find('#row-' + data.id).removeClass().addClass('animated slideOutLeft').delay(1000).fadeOut();
  });

  // Marca un pedido como impreso.
  io.on('pedido:impreso', function(data) {
    
    $el = $tbody.find('#row-' + data.id + ' span');
    if($el.text() != 'Pagado') {
      $el
        .addClass('animated slideOut')
        .removeClass('btn-warning animated slideOut')
        .addClass('btn-info animated bounceIn')
        .text('Impreso');
    }
  });

  // Muestra una ventana con el comprobante.
  io.on('pedido:cancela', function(data) {
    frameSrc = '/pedido/imprimir/' + data.what + '/' + data.id;
    $('iframe').attr("src", frameSrc);
    $('#printModal').modal({show: true});
  }); 

  // Marca un pedido como pagado.
  io.on('pedido:pagado', function(data) {
    $tbody.find('#row-' + data.id + ' span')
      .addClass('animated slideOut')
      .removeClass('btn-info animated slideOut')
      .addClass('btn-success animated bounceIn')
      .text('Pagado');
  });

  $('#the-form').submit(function(e) {
    $tbody.empty();
    $table.removeClass('animated fadeInDownBig').delay(1000).hide();

    $ver.attr('disabled', 'disabled');
    $ver.text('Un momento...');

    $.when(
      $.ajax({
        url: '/json/pedido/habitacion/' + $('#habitacion').val(),
        dataType: 'json'
      })
    ).done(function(data) {
      if(data.pedidos.length > 0) {
        parsePedidos(data.pedidos);
        $table.show().addClass('animated fadeInDownBig');
      } else {
        alert('No existen pedidos.');
      }

      $ver.removeAttr('disabled');
      $ver.text('Ver pedidos');
    });

    e.preventDefault();

  });

  $verexterno.click(function() {
    $tbody.empty();
    $table.removeClass('animated fadeInDownBig').delay(1000).hide();

    $verexterno.attr('disabled', 'disabled');
    $verexterno.text('Un momento...');

    $.when(
      $.ajax({
        url: '/json/pedido/externos',
        dataType: 'json'
      })
    ).done(function(data) {
      if(data.pedidos.length > 0) {
        parsePedidos(data.pedidos);
        $table.show().addClass('animated fadeInDownBig');
      } else {
        alert('No existen pedidos.');
      }

      $verexterno.removeAttr('disabled');
      $verexterno.text('Ver pedidos externos');
    });
  });

  $('.pay').click(printPedido);
  $('.boleta').click(printDoc);
  $('.factura').click(printDoc);
})(jQuery);