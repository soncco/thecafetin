var cafetin = cafetin || {};

(function($) {
  io.emit('chat', {'room': 'chat'});

  $message = $('#message');
  $template = $('#template');

  $el = $('.list-messages');

  $('#form-chat').submit(function(e) {
    
    e.preventDefault();

    var mensaje = {
      'mensaje': $message.val(),
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
    };

    $.post('/chat/', $.param(mensaje), function(data) {
      if(data.status == 'ok') {
        io.emit('message', {
          'cuando': moment(Date.parse(data.mensaje.cuando)).fromNow(),
          'hecho_por': data.mensaje.hecho_por,
          'mensaje': data.mensaje.mensaje
        });
      } else {
        alert('Hubo un error al crear el pedido, intenta nuevamente.');
      }
    });   

    $message.val('');
    $el.scrollTop();
  });

  refreshDates = function() {
    $('.text-muted i').each(function() {
      $(this).text(moment(parseInt($(this).data('timestamp')) * 1000).fromNow());
    });
  };

  scrollChat = function() {
    $('.list-messages').animate({scrollTop: $('.list-messages')[0].scrollHeight});
  }

  io.on('message', function(data) {
    $el.append(Mustache.render($template.html(), data));
    scrollChat();
  });

  refreshDates();
  scrollChat();
  
  setTimeout(function() {
    refreshDates();
  }, 60000);

})(jQuery);