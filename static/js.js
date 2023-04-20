var data = [
      { y: '2014', a: 50},
      { y: '2015', a: 65},
      { y: '2016', a: 50},
      { y: '2017', a: 75},
      { y: '2018', a: 80},
      { y: '2019', a: 90},
      { y: '2020', a: 100},
      { y: '2021', a: 115},
      { y: '2022', a: 120},
      { y: '2023', a: 145},
      { y: '2024', a: 50}
    ],
    config = {
      data: data,
      xkey: 'y',
      ykeys: ['a', 'b'],
      labels: ['Total Income', 'Total Outcome'],
      fillOpacity: 0.6,
      hideHover: 'auto',
      behaveLikeLine: true,
      resize: true,
      pointFillColors:['#ffffff'],
      pointStrokeColors: ['black'],
      lineColors:['gray','red']
  };
config.element = 'area-chart';
Morris.Area(config);
