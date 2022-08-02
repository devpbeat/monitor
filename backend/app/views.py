from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
import json
from .serializers import *
from .utils import *
import logging
import django.utils.timezone as timezone


# Create your views here.


class sources(APIView):

    def get(self, request, *args, **kwargs):
        """
        Get sources data from the database.
        First, it verifies if hash contains the source slug.
        If it does, it returns the source data.
        If it doesn't, error 404 not found.
        """
        slug = kwargs['slug']
        secret = kwargs['secret']
        source = Source.objects.filter(slug=slug, secret=secret).first()
        if source:
            last_update = source.last_update
            if last_update:
                data = SourceDataSerializer(instance=source).data
                response = dict()
                response['{}'.format(source.slug)] = data
                return Response(response, status=200)
            else:
                return Response({'error': 'No data related to the source has found'}, status=404)
        else:
            return Response({'error': 'Source not found'}, status=404)


class UpdaterView(APIView):
    """
    View to update the metrics.
    """

    def save_data(self, source, update, update_data, updated):
        """
        Save the data into the database.
        """
        try:
            data = json.dumps(update_data, indent=4, sort_keys=True, default=str)
            source_update = Source_Data.objects.create(
                source=source,
                update=update,
                data=data)
            source.success_update()
            source.last_update = update
            source.save()
        except Exception as e:
            source.failed_update(e)

    def post(self, request, *args, **kwargs):
        """
        Get the metrics. And save data into updates table, also
        save update status in source table.
        """
        try:
            update_data = dict()
            last_update = Updates.objects.last()
            if last_update.status == Updates.STATUS.get('running'):
                resp = stdresponse(code=200, status=last_update.status,
                                   message=last_update.description if last_update.description else "", data=None)
                json_response = json.dumps(resp, indent=4, sort_keys=True, default=str)
                return Response(json_response, status=200)
            elif last_update is None or last_update.status == Updates.STATUS.get(
                    "success") or last_update.status == Updates.STATUS.get("failed"):
                time = timezone.now().isoformat()
                update = Updates.objects.create(
                    update_time=time,
                    last_try_time=time,
                    status=Updates.STATUS.get('running'),
                )
                update.save()
                total = Source.objects.all().count()
                updated = 0
                for source in Source.objects.all():
                    if source.next_update > timezone.now():
                        continue
                    if source.credentials.slug.startswith('aws') and source.slug != 'vpn-tigo':
                        try:
                            # Get the data from the source using the source remote id and credentials.
                            update_data = get_all_metrics_statistics(source.remote_id, source.credentials)
                            self.save_data(source, update, update_data, updated)
                            updated += 1
                        except Exception as e:
                            source.failed_update(e)
                    elif source.slug == 'vpn-tigo':
                        try:
                            # Get VPN status using custom function
                            update_data = get_tigo_vpn_tunnel_status(source.credentials)
                            self.save_data(source, update, update_data, updated)
                            updated += 1
                        except Exception as e:
                            source.failed_update(e)
                    else:
                        source.failed_update("Source is not implemented.")
                if updated == 0:
                    update.delete()
                    raise Exception("No sources updated.")
                update.status = Updates.STATUS.get('success')
                update.save()
                data = UpdaterSerializer(instance=update).data
                resp = stdresponse(code=200, status=update.status, message=update.description, data=data)
                json_response = json.dumps(resp, indent=4, sort_keys=True, default=str)
                return Response(resp, status=200)
        except Exception as e:
            resp = stdresponse(code=200, status='failed', message=str(e), data=[])
            return Response(resp, status=200)


class MetricsCreatorView(APIView):
    """
    View to create metrics.
    """

    def post(self, request, *args, **kwargs):
        """
        Create metrics.
        """
        try:
            # Get all artifacts
            all_artifacts = Artifact.objects.all()
            metric_types = Metric_Types.objects.all()
            # Iterates in each artifact and create metrics
            for artifact in all_artifacts:
                # Create new metrics using the artifact and the metric type
                a_name = artifact.slug.split('-')
                if a_name[0] == 'momo':
                    artifact_name = str(a_name[0] + '-' + a_name[1])
                    source_slug = str(a_name[0] + ' ' + a_name[1])
                elif a_name[0] == 'adamspay' and len(a_name) == 3:
                    artifact_name = str(a_name[0] + '-' + a_name[1] + '-' + a_name[2])
                    source_slug = str(a_name[0] + ' ' + a_name[1] + ' ' + a_name[2])
                elif a_name[0] == 'adamspay':
                    artifact_name = str(a_name[0] + '-' + a_name[1])
                    source_slug = str(a_name[0] + ' ' + a_name[1])
                else:
                    artifact_name = str(a_name[0])
                    source_slug = str(a_name[0])
                # Iterates in each metric types that exists in the database
                for metric_type in metric_types:
                    m_name = metric_type.slug.split('_')
                    if m_name[0] == 'network':
                        metric_name = str(m_name[0] + '-' + m_name[1])
                        unit_name = 'MB/s'
                    elif m_name[0] == 'disk':
                        metric_name = str(m_name[0] + '-' + m_name[1])
                        unit_name = 'MB/s'
                    else:
                        metric_name = str(m_name[0])
                        unit_name = '%'
                    name = '{}-{}-status'.format(artifact_name, metric_name)
                    source = Source.objects.filter(name__startswith=source_slug).first()
                    last_update = source.last_update
                    if not source.metrics.filter(metric_type=metric_type).exists():
                        Metric.objects.create(
                            slug=name,
                            artifact=artifact,
                            metric_type=metric_type,
                            artifact_instance=None,
                            resource_id=None,
                            binded_source=source,
                            last_data=last_update,
                            unit=unit_name)
            response = {'meta': {
                "status": "ok",
                "description": "Metrics creadas correctamente",
                "code": "metrics_created"
            }
            }
            return Response(response, status=200)
        except Exception as e:
            response = {'meta': {
                "status": "error",
                "description": "Error al crear las metricas",
                "code": "metrics_error",
                "error": str(e)
            }
            }
            return Response(response, status=500)


class CollectorView(APIView):

    def post(self, request, format=None):
        aws_metrics_dict = {
            'cpu_utilization': 'CPUUtilization',
            'disk_read_bytes': 'DiskReadBytes',
            'disk_write_bytes': 'DiskWriteBytes',
            'network_in': 'NetworkIn',
            'network_out': 'NetworkOut',
            'memory_utilization': 'MemoryUtilization',
        }

        sources_list = Source.objects.all()
        sources_data = dict()
        for source in sources_list:
            try:
                data = dict()
                # Get the last update of the source
                last_source_data = Source_Data.objects.filter(source=source,
                                                              update=source.last_update).get()
                if source.slug == 'vpn-tigo':
                    data['status'] = last_source_data.data['status']

                # Get the metrics of the source
                metrics_list = source.metrics.all()
                # Get the metric data
                metric_data_json = last_source_data.data
                # converts the metric data to dict format
                metric_data = json.loads(metric_data_json)
                # Iterate in each metric
                for metric in metrics_list:
                    metric_helper = aws_metrics_dict[metric.metric_type.slug]
                    metric_value = metric_data[metric_helper]

                    # Checks if the last data of the metric is the same as the last update of the source.
                    # If it is true, then the metric is not updated.
                    # Else, the metric is updated. And those fields too.

                    if metric.last_data != last_source_data:
                        metric.last_data = last_source_data
                        metric.save()
                        value = metric_value.split(' ')[0] if metric_value else None

                        # Get the metric data
                        Metric_Data.objects.create(
                            metric=metric,
                            source_data=last_source_data,
                            value=value,
                            unit=metric.unit,
                        )
                        data[metric.metric_type.slug] = 'Actualizado' if metric_value else 'No hay datos'
                    else:
                        data[metric.metric_type.slug] = 'No actualizado'
                        continue
                sources_data[source.name] = data
            except Exception as e:
                sources_data[source.name] = {'error': str(e)}

        response = stdresponse(code='200', status='success', message='Collecciones creadas de forma exitosa',
                               data=sources_data)

        return Response(response, status=200)


class MetricsDataView(APIView):
    """
    View that returns all Metrics Data without hash authentication.
    """

    def get(self, request, format=None):
        """
        Returns all Metrics Data.
        """
        data = dict()
        sources = Source.objects.all()
        for source in sources:
            last_update = source.last_update
            if last_update:
                last_update = last_update.sources_data.filter(source=source, update=last_update).get()
                # Get the metrics of the source
                metrics_list = source.metrics.all()
                # Get all metrics data related to the source and the last update
                metrics_data = Metric_Data.objects.filter(source_data=last_update)
                # Serialize the data
                serializer = MetricDataSerializer(metrics_data, many=True)
                data[source.slug] = serializer.data
            else:
                data[source.slug] = {'error': 'No hay datos'}
            # if data = success message will be 'ok'

        response = stdresponse(code='200', status='success', message='Datos obtenidos correctamente', data=data)

        return Response(response, status=200)


class MetricDataHistoricView(APIView):
    """
    View that returns a historic data of Metrics Data, it will have the possibility to apply filters.
    Filters like: start date, end date, period (daily, weekly, monthly, year)
    """

    def get(self, request, format=None):
        """
        Returns all Metrics Data.
        """
        data = dict()
        sources = Source.objects.all()
        for source in sources:
            last_update = source.last_update
            if last_update:
                last_update = last_update.sources_data.filter(source=source, update=last_update).get()
                # Get the metrics of the source
                metrics_list = source.metrics.all()
                # Get all metrics data related to the source and the last update
                metrics_data = Metric_Data.objects.filter(source_data=last_update)
                # Serialize the data
                serializer = MetricDataSerializer(metrics_data, many=True)
                data[source.slug] = serializer.data
            else:
                data[source.slug] = {'error': 'No hay datos'}
            # if data = success message will be 'ok'

        response = stdresponse(code='200', status='success', message='Datos obtenidos correctamente', data=data)

        return Response(response, status=200)


class VPNStatusCheck(APIView):

    def get(self, request, format=None):
        """
        Returns VPN Status
        """
        data = dict()
        credentials = Credentials.objects.get(id=1)
        try:

            vpn_status = get_tigo_vpn_tunnel_status(credentials)
            data['vpn_status'] = vpn_status
            response = stdresponse(code='200', status='success', message='VPN Status obtenido correctamente', data=data)
            return Response(response, status=200)
        except Exception as e:
            data['error'] = str(e)
            response = stdresponse(code='500', status='error', message='Error al obtener el VPN Status', data=data)
            return Response(response, status=500)
