var monitor=new Vue ({
    el: '#nav',
    data: {
        groups: [],
        apps: [],
        app_histories: [],
        url_app_list: '/api/apps/',
        url_app_history: '/api/app_history/',
        url_count_groups: '/api/count/groups/'
    },
    created: function () {
        this.countGroups();
        this.getApps(1)
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
        }
    }
});





