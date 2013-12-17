var cafetin = cafetin || {};

(function($) {

  var $inicio = $('#inicio'),
   $fin = $('#fin'),
   $mozo = $('#mozo');

  $('.datepicker').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'yy-mm-dd'
  });

  renderData = function(data) {
    var chart = nv.models.multiBarHorizontalChart()
      .x(function(d) { return d.plato })
      .y(function(d) { return d.total })
      .margin({top: 30, right: 20, bottom: 50, left: 175})
      .showValues(true)
      .tooltips(false)
      .showControls(false);

    chart.yAxis
      .tickFormat(d3.format(',.2f'));

    d3.select('#chart')
        .datum(data)
      .transition().duration(500)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  };

  $('#the-form').submit(function(e) {
    e.preventDefault();

    $.when(
      $.ajax({
        url: '/reporte/mozo/masvendido/',
        data: {
          'inicio': $inicio.val(),
          'fin': $fin.val(),
          'mozo': $mozo.val(),
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        type: 'POST',
        dataType: 'json'
      })
    ).done(function(data) {
      realData = [{'key': 'Platos más vendidos por mozo', 'values': data}];
      //console.log(JSON.stringify(realData));
      nv.addGraph(renderData(realData));
    });
  });

})(jQuery);

