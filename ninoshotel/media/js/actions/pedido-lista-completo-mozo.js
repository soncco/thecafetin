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

  $('.datepicker').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'dd-mm-yy'
  });
})(jQuery);