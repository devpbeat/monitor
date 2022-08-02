import json
from datetime import datetime, timedelta
from django.db import models
from django.db.models import JSONField

# Create your models here.
from django.utils import timezone


class Credentials(models.Model):
    """
    Credentials model
    """
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    secret_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    access_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    connector = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.created_at:
            self.created_at = timezone.now()
            self.updated_at = timezone.now()

        self.updated_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return 'Credentials of ' + self.slug


class Updates(models.Model):
    STATUS = {
        'success': 'success',
        'failed': 'failed',
        'running': 'running',
    }
    STATUS_CHOICES = (
        ('success', 'success'),
        ('failed', 'failed'),
        ('running', 'running'),
    )
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_try_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return 'Actualizacion realizada en: ' + str(self.update_time)

    class Meta:
        verbose_name = 'Update'
        verbose_name_plural = 'Updates'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.description = self.calculate_updated_sources()
        super().save(force_insert, force_update, using, update_fields)

    def calculate_updated_sources(self):
        amount = 0
        total = Source.objects.count()
        if total > 0:
            for source in self.sources_data.all():
                if source.source.status == 'success':
                    amount += 1
            return "{}/{} sources updated".format(amount, total)
        else:
            return "No sources updated."


class Source(models.Model):
    STATUS_CHOICES = (
        ('success', 'success'),  # It returns data and collects it
        ('failed', 'failed')  # It returns value, but not collect it
    )
    credentials = models.ForeignKey(Credentials, on_delete=models.PROTECT,
                                    related_name='sources')
    last_error_message = models.CharField(max_length=255, null=True, blank=True)
    last_try_time = models.DateTimeField(null=True, blank=True)
    last_update_time = models.DateTimeField(null=True, blank=True)
    last_error_time = models.DateTimeField(null=True, blank=True)
    next_update = models.DateTimeField(default=None, blank=True, null=True)
    secret = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    update_interval = models.IntegerField(default=15)  # in minutes
    name = models.CharField(max_length=100
                            , blank=True, null=True)
    remote_id = models.CharField(max_length=100, blank=True, null=True)
    last_update = models.ForeignKey(Updates, on_delete=models.PROTECT,
                                       related_name='last_update', null=True, blank=True)
    status_time = models.DateTimeField(null=True, blank=True)
    remote_name = models.CharField(max_length=100, blank=True, null=True)
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.next_update is None:
            self.next_update = datetime.now() + timedelta(minutes=self.update_interval)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.pk) + ' : ' + self.name if self.name else str(self.pk)

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    def success_update(self):
        time = datetime.now(tz=timezone.utc)
        if self.status == 'failed': self.status_time = time
        self.status = 'success'
        self.last_update_time = time
        self.last_try_time = time
        self.next_update = self.last_update_time + timedelta(minutes=self.update_interval)
        self.save()

    def failed_update(self, message):
        time = datetime.now(tz=timezone.utc)
        if self.status == 'success': self.status_time = time
        self.status = 'failed'
        self.last_error_message = message
        self.last_error_time = self.last_try_time = time
        self.save()



class Source_Data(models.Model):
    source = models.ForeignKey(Source, on_delete=models.PROTECT,
                               related_name='update_data', unique=False)
    update = models.ForeignKey(Updates, on_delete=models.PROTECT,
                               related_name='sources_data', unique=False)
    data = models.JSONField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Source Data'
        verbose_name_plural = 'Sources Data'

    def __str__(self):
        return str(self.source.name) + ' : ' + str(self.update)



class Artifact(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Artifact'
        verbose_name_plural = 'Artifacts'

    def __str__(self):
        return self.slug


class Metric_Types(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Metric Type'
        verbose_name_plural = 'Metric Types'

    def __str__(self):
        return self.slug


class Metric(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.PROTECT,
                                 related_name='metrics', unique=False)
    metric_type = models.ForeignKey(Metric_Types, on_delete=models.PROTECT,
                                    related_name='metrics', unique=False,
                                  null=True, blank=True)
    artifact_instance = models.CharField(max_length=100, blank=True, null=True)
    resource_id = models.CharField(max_length=100, blank=True, null=True)
    binded_source = models.ForeignKey(Source, on_delete=models.PROTECT,
                               related_name='metrics', unique=False,
                                  null=True, blank=True)
    last_data = models.ForeignKey(Source_Data, on_delete=models.PROTECT,
                                  related_name='metrics', unique=False,
                                  null=True, blank=True)
    unit = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'

    def __str__(self):
        return self.slug




class Metric_Data(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT,
                               related_name='data', unique=False)
    source_data = models.ForeignKey(Source_Data, on_delete=models.PROTECT,
                                    related_name='metric_data', unique=False)
    value = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Metric Data'
        verbose_name_plural = 'Metrics Data'

    def __str__(self):
        return str(self.metric) + ' : ' + str(self.source_data)