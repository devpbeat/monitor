import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import boto3
from datetime import datetime, timedelta, timezone
from .models import Credentials
import json

metrics = [
    'CPUUtilization',
    'DiskReadBytes',
    'DiskWriteBytes',
    'NetworkIn',
    'NetworkOut',
    'MemoryUtilization'
]

my_secret = "d4s#b04!d_s3@r3%d"


def get_boto_client(service_name, model):
    """ Get boto3 client. """
    return boto3.client(service_name,
                        aws_access_key_id=model.access_key,
                        aws_secret_access_key=model.secret_key,
                        region_name=model.region)


def get_metrics_statistics(metric_name, instance_id, credentials):
    """
    Get statistics for a metric.
    """
    time = datetime.now()
    client = get_boto_client('cloudwatch', credentials)
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ],
        StartTime=(time - timedelta(minutes=30)).isoformat(),
        EndTime=(time - timedelta(minutes=15)).isoformat(),
        Period=30,
        Statistics=['Maximum']
    )
    return response


def get_all_metrics_statistics(instances_id, model):
    """ Get all metrics statistics.
    Returns an array where the first element is the instance tag name and the second is the metric value. """
    metrics_statistics = dict()
    for metric in metrics:
        data = get_metrics_statistics(metric, instances_id, model)
        if metric != 'NetworkIn' and metric != 'NetworkOut' and metric != 'DiskReadBytes' and metric != 'DiskWriteBytes':
            value = float(data['Datapoints'][0]['Maximum']) if data['Datapoints'] else None
        else:
            value = float(data['Datapoints'][0]['Maximum']) if data['Datapoints'] else None
            if value is not None:
                value = value / 1024 ** 2
        if metric == 'CPUUtilization':
            m = ' %'
        elif metric == 'DiskReadBytes' or metric == 'DiskWriteBytes' or metric == 'NetworkIn' or metric == 'NetworkOut':
            m = ' MB'
        elif metric == 'MemoryUtilization':
            m = ' %'
        if value is not None:
            metrics_statistics[metric] = "{:.2f} {}".format(round(value, 2), str(m))
        else:
            metrics_statistics[metric] = None

    return metrics_statistics


def get_all_ec2_instances_id_and_tag_name_value(credentials):
    """ Get all ec2 instances id and tag name value. """
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=credentials.access_key,
                         aws_secret_access_key=credentials.secret_key,
                         region_name=credentials.region)
    instances = ec2.instances.all()
    instances_id = dict()
    # Creates a dictionary with the instance id and the tag name value.
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                instances_id[tag['Value']] = [instance.id, tag['Value']]
    return instances_id


def encrypt_string(string):
    """ Encrypt string. """
    import hashlib
    hash_object = hashlib.md5(string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


# Function to get all ec2 available metrics.
def get_all_ec2_metrics(credentials):
    """ Get all ec2 metrics. """
    client = get_boto_client('cloudwatch', credentials)
    response = client.list_metrics(
        Namespace='AWS/EC2',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-02698998b92f6c485'
            },
        ]
    )
    return response


class GoogleAPI:

    @staticmethod
    def get_credentials(scopes):
        """
        Gets the credentials for the Google API
        """
        # credentials = Credentials.objects.get(slug__startswith='google')
        service_account_info = './service.json'
        creds = service_account.Credentials.from_service_account_file(service_account_info, scopes=scopes)
        return creds

    @staticmethod
    def get_service(credentials, api_name, api_version, *args, **kwargs):
        """
        Gets the service for the Google API
        """
        service = build(
            api_name,
            api_version,
            credentials=credentials,
            discoveryServiceUrl=kwargs.get('discoveryServiceUrl'),
        )
        return service

    @staticmethod
    def get_crashrate_metric(project_id):
        scopes = ['https://www.googleapis.com/auth/playdeveloperreporting']
        credentials = GoogleAPI.get_credentials(scopes)

        try:
            service = GoogleAPI.get_service(credentials, None, 'v1',
                                            discoveryServiceUrl='https://playdeveloperreporting.googleapis.com/$discovery/rest')
            response = service.vitals().crashrate().get(
                name='apps/{}/crashRateMetricSet'.format(project_id)).execute()
            return response

        except HttpError as err:
            return err

    @staticmethod
    def get_latest_review(project_id):
        scopes = ['https://www.googleapis.com/androidpublisher']
        credentials = GoogleAPI.get_credentials(scopes)

        try:
            service = GoogleAPI.get_service(credentials, 'androidpublisher', 'v3')
            response = service.reviews().list(packageName=project_id, maxResults=1, )
            return response
        except HttpError as err:
            return err


def stdresponse(code, status, message, data):
    return {
        "meta": {
            "code": code,
            "status": status,
            "message": message
        },
        "data": data
    }


def get_tigo_vpn_tunnel_status(credentials):
    """ Get vpn status in the last 5 minutes """
    time = datetime.now()
    cw = get_boto_client('cloudwatch', credentials)
    vpn_status = cw.get_metric_data(
        StartTime=(time - timedelta(minutes=5)).isoformat(),
        EndTime=time.isoformat(),
        LabelOptions={
            'Timezone': '-0400'
        },
        MetricDataQueries=[
            {
                'Id': 'tigoVPNStatus',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/VPN',
                        'MetricName': 'TunnelState',
                        'Dimensions': [
                            {
                                'Name': 'TunnelIpAddress',
                                'Value': '23.23.241.51'
                            },
                        ]
                    },
                    'Period': 3600,
                    'Stat': 'Maximum',
                },
            },
        ],
    )
    value = vpn_status['MetricDataResults'][0]['Values'][0]
    time = vpn_status['MetricDataResults'][0]['Timestamps'][0]
    response = dict()
    response['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    if value == 0:
        response['status'] = 'Disconnected'
    elif value == 1:
        response['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        response['status'] = 'Connected'

    return response
