Vue.use(VueHighcharts);

var options = {
  title: {
    text: 'CPU & Memory',   //app.name + 'CPU & Memory Useage'
    x: -20 //center
  },
  subtitle: {
    text: '',  //app.name
    x: -20
  },
  xAxis: {
    categories: [     //appstatistics.time
    ]
  },
  yAxis: {
    title: {
      text: 'CPU & Mem Usage (%)'
    },
    plotLines: [{
      value: 0,
      width: 1,
      color: '#808080'
    }]
  },
  tooltip: {
    valueSuffix: '%'
  },
  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
  },
  series: [{
    name: 'CPU',   //
    data: []    //appstatistics.statistics.cpu
  },{
    name: 'Mem',   //
    data: []    //appstatistics.statistics.mem
  }]
};

var monitor=new Vue ({
    el: '#nav',
    data: {
        groups: [],
        apps: [],
        app_histories: [],
        app_statistics: [],
        url_app_list: '/api/apps/',
        url_app_history: '/api/app_history/',
        url_count_groups: '/api/count/groups/',
        url_statistics: '/api/statistics/',
        options: options,
        display_map: false
    },
    created: function () {
        this.countGroups();
        this.getApps(1);
    },
    methods: {
        countGroups: function () {
            this.$http.get(this.url_count_groups).then(function (response) {this.groups = response.data;}, function (response) {console.log(response)});
        },
        getApps: function (group_id) {
            this.$http.get(this.url_app_list + "?group_id=" + group_id).then(function (response) {
                this.apps = response.data;
            }, function (response) {
                console.log(response)
            });
        },
        getAppHistory: function (app_id) {
            this.$http.get(this.url_app_history + "?app_id=" + app_id).then(function (response) {
                this.app_histories = response.data;
            }, function (response) {
                console.log(response)
            });
            this.getStatistics(app_id);
            this.updateCredits();
        },
        getStatistics: function (app_id) {
            this.$http.get(this.url_statistics + app_id + "/").then(function (response) {
                // this.app_statistics = response.data;
                this.options.series[0].data=[];
                this.options.series[1].data=[];
                for(var index in response.data){
                    // console.log(JSON.parse(response.data[index].statistics).cpu);
                    this.options.series[0].data.push(JSON.parse(response.data[index].statistics)['cpu']);
                    this.options.series[1].data.push(JSON.parse(response.data[index].statistics)['mem']);
                }
                console.log(this.options.series[0].data);
                this.display_map = true
            }, function (response) {
                console.log(response)
            });
        },
        updateCredits: function() {
            var chart = this.$refs.highcharts.chart;
            chart.credits.update({
                style: {
                  color: '#' + (Math.random() * 0xffffff | 0).toString(16)
                }
            });
        }
    }
});








