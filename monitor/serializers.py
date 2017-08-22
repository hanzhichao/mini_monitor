from rest_framework import serializers
from monitor.models import App,AppStatistics,AppHistory,Group,Host


class AppSerializer(serializers.ModelSerializer):
    last_update = serializers.ReadOnlyField(source='convert_to_epoc')
    class Meta:
        model = App
        fields = ('id','name','host_ip','configuration','status',
            'message','enable','last_update')

class ManageAppSerializer(serializers.ModelSerializer):
    last_update = serializers.ReadOnlyField(source='convert_to_epoc')
    class Meta:
        model = App
        fields = ('id','name','host_ip','group_id','configuration','status',
            'message','enable','last_update')

class AppStatisticsSerializer(serializers.ModelSerializer):
    time = serializers.ReadOnlyField(source='convert_to_epoc')
    class Meta:
        model = AppStatistics
        fields = ('id','app_id','statistics','time')

class AppHistorySerializer(serializers.ModelSerializer):
    time = serializers.ReadOnlyField(source='convert_to_epoc')
    class Meta:
        model = AppHistory
        fields = ('app_id','status','message','time')

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('unique_name', 'display_name', 'id')


class HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = ('name', 'ip', 'description')



