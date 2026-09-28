import django_filters

from .models import Agreement


class AgreementFilter(django_filters.FilterSet):
    unidade = django_filters.NumberFilter(field_name="unidade_id")
    criado_de = django_filters.DateFilter(field_name="criado_em__date", lookup_expr="gte")
    criado_ate = django_filters.DateFilter(field_name="criado_em__date", lookup_expr="lte")

    class Meta:
        model = Agreement
        fields = []