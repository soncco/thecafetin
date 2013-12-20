var cafetin = cafetin || {};

(function($) {

  $('.timeago').timeago();

  // La tabla.
  var $tables = $('.pedido-lista');

  atenderPedido = function() {
    atender = window.confirm('¿Está seguro de marcar este pedido como atendido?');
    if(atender) {
      $.post('/pedido/atender/', {
        'id': $(this).data('id'),
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      }, function(data) {
        if(data.status == 'ok') {
          io.emit('pedido:atender', data);
        } else {
          alert('Hubo un error al atender el pedido, intenta nuevamente.');
        }
      }); 
    }
  };

  // Imprime un pedido.
  printPedido = function() {
    id = $(this).data('id');
    comanda = $(this).data('comanda');
    consumo = $(this).data('consumo');
    foraneo = $(this).data('foraneo');

    $('.comanda').data('id', id);
    $('.consumo').data('id', id);

    $('.comanda').show();
    $('.consumo').show();
    /*if(comanda == 'false') $('.comanda').hide();
    if(consumo == 'false') $('.consumo').hide();*/

    if(!comanda) $('.comanda').hide();
    if(!consumo) $('.consumo').hide();

    if(foraneo) {
      $('.comanda').show();
      $('.consumo').hide();
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
      if(what == 'consumo') {
        if(!thedoc) {
          number = prompt('Ingresa el número del detalle de consumo.');
          if(number < 0) { // Fix.
            alert('Debes ingresar un número');
            return;
          }
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
          io.emit('pedido:imprimir', data);
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
    $tbody = $tables.filter('#pedido-lista-' +  pedido.punto);
    // Los elementos de las filas.
    $tr = $('<tr></tr>');
    $td = $('<td></td>');
    $status = $('<span class="btn btn-sm"></span>');
    $print = $('<button class="btn btn-sm btn-info print" data-id=""></button>&nbsp;')
      .html($('<i class="icon icon-print"></i>'));
    $edit = $('<button class="btn btn-warning attend" data-id=""></button>&nbsp;').html($('<i class="icon icon-check"></i>'));

    if(pedido.visitante != '')
      $td.clone().text('Foraneo: ' + pedido.visitante).appendTo($tr);
    else
      $td.clone().text(pedido.para).appendTo($tr);
    $td.clone().html(parseDetalles(pedido.detalles)).appendTo($tr);
    $td.clone().text(pedido.comentarios).appendTo($tr);
    $td.clone().text(pedido.hecho_por).appendTo($tr);
    $td.clone().text(jQuery.timeago(pedido.fecha)).addClass('timeago').appendTo($tr);
    $td.clone().html($status.text(cafetin.estados[pedido.estado].texto).addClass(cafetin.estados[pedido.estado].clase)).appendTo($tr);

    // Verifica los estados del pedido.
    switch(pedido.estado) {
      case 'R':
        $print.hide();
      break;
      case 'A':
        $edit.hide();
      break;
      case 'I':
        $edit.hide();
      break;
      case 'P':
        $edit.hide();
      break;
    }

    $td.clone()
        .append($edit.data('id', pedido.id))
        .append($print.data('id', pedido.id)
          .data('comanda', (pedido.tiene_comanda == 'true') ? true : false)
          .data('consumo', (pedido.tiene_consumo == 'true') ? true : false)
          .data('foraneo', (pedido.visitante != ''))
          )
      .addClass('actions')
      .appendTo($tr);

    // Agrega eventos a los botones.
    $tr.delegate('.attend', 'click', atenderPedido);
    $tr.delegate('.print', 'click', printPedido);

    // Crea la fila.
    $tr
      .attr('id', 'row-' + pedido.id)
      .prependTo($tbody)
      .addClass('animated tada');

  };

  // Parsea pedidos de JSON a una tabla HTML.
  parsePedidos = function(pedidos) {
    for(i = 0; i < pedidos.length; i++) {
      row = pedidos[i];
      parsePedido(row);
    }
  };

  sound = function() {
    var chatsound = document.createElement('audio');
    chatsound.setAttribute('src', '/media/sounds/sisfus.mp3');
    chatsound.play();
  };

  // ios.
  // Crea un pedido.
  io.on('pedido:creado', function(data) {
    for(i = 0; i < data.pedidos.length; i++) {
      pedido = data.pedidos[i];
      parsePedido(pedido);
    }
    sound();
  });

  // Quita un pedido.
  io.on('pedido:quitado', function(data) {
    $tbody = $tables.filter('#pedido-lista-' +  data.punto);
    $tbody.find('#row-' + data.id).removeClass().addClass('animated slideOutLeft').delay(1000).fadeOut();;
  });

  // Marca un pedido como atendido.
  io.on('pedido:atendido', function(data) {
    $tbody = $tables.filter('#pedido-lista-' +  data.punto);
    $tbody.find('#row-' + data.id + ' .attend')
      .remove();
    
    $tbody.find('#row-' + data.id + ' span')
      .addClass('animated slideOut')
      .removeClass('btn-danger animated slideOut')
      .addClass('btn-warning animated bounceIn')
      .text('Atendido');

    $tbody.find('#row-' + data.id + ' .print')
      .show()
      .addClass('animated tada');

  });

  // Marca un pedido como impreso.
  io.on('pedido:impreso', function(data) {
    $tbody = $tables.filter('#pedido-lista-' +  data.punto);
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
  io.on('pedido:imprime', function(data) {
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

  // Recarga la página cada 5 minutos.
  setTimeout(function() {
    location.reload();
  }, 300000);

  $('.attend').click(atenderPedido);
  $('.print').click(printPedido);
  $('.comanda').click(printDoc);
  $('.consumo').click(printDoc);

})(jQuery);