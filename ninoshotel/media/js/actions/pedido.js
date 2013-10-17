var cafetin = cafetin || {};

(function($) {

  var flagClear = false;

  // Autocomplete de Clientes.
  $( "#cliente" ).autocomplete({
    source: function( request, response ) {
      $.ajax({
        url: "/json/cliente/" + request.term,
        dataType: "jsonp",
        success: function( data ) {
          response( $.map( data, function( item ) {
            cliente = item.nombres + ' ' + item.apellidos; 
            return {
              'label': cliente,
              'value': cliente,
              'id': item.id
            };
          }));
        }
      });
    },
    minLength: 1,
    select: function( event, ui ) {
      $('.cliente-nombre').data('id', ui.item.id);
      $('.cliente-nombre').text('Cliente: ' + ui.item.label).addClass('animated tada');
    },
    open: function() {
      $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
    },
    close: function() {
      $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
    }
  });

  // Autocomplete de Platos.
  $( "#platos" ).autocomplete({
    source: function( request, response ) {
      $.ajax({
        url: "/json/plato/" + request.term,
        dataType: "jsonp",
        success: function( data ) {
          response( $.map( data, function( item ) {
            plato = item.nombre;
            return {
              'label': plato,
              'value': plato,
              'id': item.id
            };
          }));
        }
      });
    },
    minLength: 1,
    select: function( event, ui ) {
      $('#current-plato').data('id', ui.item.id);
      $('#current-plato').val(ui.item.label);
    },
    open: function() {
      $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
    },
    close: function() {
      $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
    }
  });

  // Creamos el pedido.
  crearPedido = function(pedido) {
    $.post('/pedido/crear/', $.param(pedido), function(data) {
      if(data.status == 'ok') {
        io.emit('pedido:nuevo', data);
        alert('El pedido se ha creado correctamente.');
        if(flagClear) {
          cafetin.theDetalles.reset();
          $('#cliente').val('');
          $('#cliente').focus();
          $('.cliente-nombre').data('id', '');
          $('.cliente-nombre').text('');

          $('#visitante').val('');
          $('#theforeign').hide();
          $('#thecliente').removeClass('animated bounceOutRight').show();
          $('#nope').attr('checked', false);
        }
        else {
          location.href = '/pedido/lista/mozo';
        }
      } else {
        alert('Hubo un error al crear el pedido, intenta nuevamente.');
      }
    });    
  }

  pedido = function() {
    cantidades = cafetin.theDetalles.pluck('cantidad');
    platos = cafetin.theDetalles.pluck('platoId');
    var pedido = {
      para: $('.cliente-nombre').data('id'),
      visitante: $('#visitante').val(),
      cantidad: cantidades,
      platos: platos,
      observaciones: $('#observaciones').val(),
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
    };
    crearPedido(pedido);
  };

  $('.do').click(function() {
    pedido();
    flagClear = false;
  });

  $('.do-clear').click(function() {
    pedido();
    flagClear = true;
  });

  $('#cliente').focus();

  $('#nope').click(function() {
    $thecliente = $('#thecliente');
    $theforeign = $('#theforeign');
    if($(this).is(':checked')) {
      // No es cliente
      $theforeign.show()
        .removeClass('animated bounceInLeft bounceOutRight')
        .addClass('animated bounceInLeft');
      $thecliente
        .removeClass('animated bounceInLeft bounceOutRight')
        .addClass('animated bounceOutRight')
        .delay(800).fadeOut();

        $('#visitante').focus();

      $('.cliente-nombre').data('id', 'Foraneo');

    } else {
      $thecliente.show()
        .removeClass('animated bounceInLeft bounceOutRight')
        .addClass('animated bounceInLeft');
      $theforeign
        .removeClass('animated bounceInLeft bounceOutRight')
        .addClass('animated bounceOutRight')
        .delay(800).fadeOut();
    }
  });

})(jQuery);