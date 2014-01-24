var cafetin = cafetin || {};

(function($) {

  var $table = $('#clientes');
  var $tbody = $table.find('tbody');
  var $checkout = $('.checkout');

  $checkout.click(function() {
    var $tr = $(this).parent().parent();
    nombres = $tr.find('.cliente-nombre').text()
    conf = window.confirm('¿Estás seguro de quitar el huesped ' + nombres + '?');
    if(conf) {
      $.post(
        '/checkout/',
        {
          'id': $tr.data('id'),
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        }
      )
      .done(function() {
        $tr.fadeOut().remove('slow');
      });
    }
  });
  
})(jQuery);