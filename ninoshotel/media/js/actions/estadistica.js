var cafetin = cafetin || {};

(function($) {

  forMonth = (JSON.parse(JSON.stringify(cafetin.pie)));
  forYear = (JSON.parse(JSON.stringify(cafetin.pie)));

  forMonth.title.text = 'Por mes';
  forMonth.series[0].name = 'Por mes';

  $('.plato-mes').highcharts(forMonth);
  $('.plato-anio').highcharts(forYear);
})(jQuery);

