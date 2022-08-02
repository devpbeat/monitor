from abc import ABC

from rest_framework import serializers
from .models import *


class SourceSerializer(serializers.ModelSerializer):
    sourceName = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    lastUpdateTime = serializers.SerializerMethodField()
    lastTryTime = serializers.SerializerMethodField()
    lastErrorTime = serializers.SerializerMethodField()
    lastErrorMessage = serializers.SerializerMethodField()
    updateInterval = serializers.SerializerMethodField()
    statusTime = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            'sourceName',
            'status',
            'statusTime',
            'lastUpdateTime',
            'lastTryTime',
            'lastErrorTime',
            'lastErrorMessage',
            'updateInterval'
        ]

    def get_sourceName(self, obj):
        return obj.slug

    def get_status(self, obj):
        return obj.status

    def get_lastUpdateTime(self, obj):
        return obj.last_update_time

    def get_lastTryTime(self, obj):
        return obj.last_try_time

    def get_lastErrorTime(self, obj):
        return obj.last_error_time

    def get_lastErrorMessage(self, obj):
        return obj.last_error_message

    def get_updateInterval(self, obj):
        return obj.update_interval * 60

    def get_statusTime(self, obj):
        return obj.status_time


class UpdaterSerializer(serializers.ModelSerializer):
    update = serializers.SerializerMethodField()
    sources = serializers.SerializerMethodField()

    class Meta:
        model = Updates
        fields = [
            'update',
            'sources',
        ]

    def get_sources(self, obj):
        sources = Source.objects.filter(update_data__update_id=obj.id)
        serializer = SourceSerializer(sources, many=True)
        return serializer.data

    def get_update(self, obj):
        return {
            'tryTime': obj.update_time,
            'lastTryTime': obj.last_try_time,
        }


class SourceDataSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            'status',
            'data'
        ]

    def get_data(self, obj):
        data = json.loads(obj.last_update.data)
        return data

    def get_status(self, obj):
        response = dict()
        response['status'] = obj.status
        response['lastUpdateTime'] = obj.last_update_time
        response['lastTryTime'] = obj.last_try_time
        response['lastErrorTime'] = obj.last_error_time
        response['lastErrorMessage'] = obj.last_error_message
        response['updateInterval'] = obj.update_interval * 60
        return response


class MetricDataSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Metric_Data
        fields = [
            'label',
            'value',
            'unit',
            'time'
        ]

    def get_label(self, obj):
        return obj.metric.metric_type.slug

    def get_value(self, obj):
        return obj.value

    def get_unit(self, obj):
        return obj.unit

    def get_time(self, obj):
        return str(obj.source_data.update.update_time)
