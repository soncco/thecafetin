var cafetin = cafetin || {};
cafetin.colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#e67e22','#e74c3c', '#7f8c8d', '#d35400', '#2980b9'];

cafetin.pie = {
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false
  },
  title: {
    text: ''
  },
  colors: cafetin.colors,
  tooltip: {
    pointFormat: '{series.name}: <b>{point.percentage:.1f}</b>'
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        color: '#000000',
        connectorColor: '#000000',
        format: '<b>{point.name}</b>: {point.percentage:.1f}'
      }
    }
  },
  series: [{
    type: 'pie',
    name: '',
    data: []
  }]
}