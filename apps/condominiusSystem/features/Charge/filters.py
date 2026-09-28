import django_filters

from .models import Charge, ChargeStatus


class ChargeFilter(django_filters.FilterSet):
    condominio = django_filters.NumberFilter(field_name="unidade__condominio_id")
    unidade = django_filters.NumberFilter(field_name="unidade_id")
    status = django_filters.ChoiceFilter(choices=ChargeStatus.choices)
    competencia = django_filters.DateFilter(field_name="competencia")
    vencimento_de = django_filters.DateFilter(field_name="data_vencimento", lookup_expr="gte")
    vencimento_ate = django_filters.DateFilter(field_name="data_vencimento", lookup_expr="lte")

    class Meta:
        model = Charge
        fields = []