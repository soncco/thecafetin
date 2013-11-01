var cafetin = cafetin || {};

(function($) {

  // La tabla.
  var $documento = $('#documento'),
    $numero = $('#numero');

  $('#the-form').submit(function(e) {
    e.preventDefault();
    $documento.empty();
    $documento.removeClass('animated fadeInDownBig').delay(1000).hide();

    $.when(
      $.ajax({
        url: '/reporte/documento/boleta/',
        data: {
          'numero': $numero.val(),
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        type: 'POST',
        dataType: 'json'
      })
    ).done(function(data) {
      if(data.numero) {
        $template = $('#template').html();
        output = Mustache.render($template, data);
        $('#documento').append(output);
        $documento.show().addClass('animated fadeInDownBig');
      } else {
        alert('No existe una boleta con el número ' +  $numero.val() + '.');
        $numero.val('');
        $numero.focus();
      }
    });
  });

})(jQuery);
