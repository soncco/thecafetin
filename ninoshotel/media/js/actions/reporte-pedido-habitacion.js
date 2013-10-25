var cafetin = cafetin || {};

(function($) {

  // La tabla.
  var $inicio = $('#inicio'),
   $fin = $('#fin'),
   $habitacion = $('#habitacion');

  $('#the-form').submit(function(e) {
    e.preventDefault();
    $tbody.empty();
    $table.removeClass('animated fadeInDownBig').delay(1000).hide();

    $.when(
      $.ajax({
        url: '/reporte/pedido/habitacion/',
        data: {
          'inicio': $inicio.val(),
          'fin': $fin.val(),
          'habitacion': $habitacion.val(),
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        type: 'POST',
        dataType: 'json'
      })
    ).done(function(data) {
      if(data.length > 0) {
        $total.text(data.length);
        parsePedidos(data);
        $table.show().addClass('animated fadeInDownBig');
      } else {
        alert('No existen pedidos con esos datos.');
      }
    });
  });

})(jQuery);