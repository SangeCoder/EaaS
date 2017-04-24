# coding: utf-8

from django.db import models
from django.http import JsonResponse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class NoDeleteQuerySet(models.query.QuerySet):

    def delete(self):
        return self.update(is_discard=True, discard_time=now())


class NoDeleteManager(models.Manager):

    def get_all(self):
        return NoDeleteQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return NoDeleteQuerySet(self.model, using=self._db).filter(is_discard=False)

    def get_deleted(self):
        return NoDeleteQuerySet(self.model, using=self._db).filter(is_discard=True)


class NoDeleteModelMixin(models.Model):
    is_discard = models.BooleanField(verbose_name=_("is discard"), default=False)
    discard_time = models.DateTimeField(verbose_name=_("discard time"), null=True, blank=True)

    objects = NoDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_discard = True
        self.discard_time = now()
        return self.save()


class JSONResponseMixin(object):
    """JSON mixin"""
    @staticmethod
    def render_json_response(context):
        return JsonResponse(context)


class IDInFilterMixin(object):
    def filter_queryset(self, queryset):
        id_list = self.request.query_params.get('id__in')
        if id_list:
            import json
            try:
                ids = json.loads(id_list)
            except Exception as e:
                return queryset
            if isinstance(ids, list):
                queryset = queryset.filter(id__in=ids)
        return queryset
