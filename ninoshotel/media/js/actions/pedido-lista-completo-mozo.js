var cafetin = cafetin || {};

(function($) {

  $('.timeago').timeago();

  $('.datepicker').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'dd-mm-yy'
  });
})(jQuery);