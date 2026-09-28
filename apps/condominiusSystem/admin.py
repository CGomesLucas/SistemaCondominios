from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.condominiusSystem.features.Agreements.models import Agreement, AgreementInstallment
from apps.condominiusSystem.features.Authentication.models import User
from apps.condominiusSystem.features.Charge.models import Charge
from apps.condominiusSystem.features.Condominius.models import Condominius
from apps.condominiusSystem.features.Unity.models import Unity


class CondominiusUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "email", "role")


class CondominiusUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = User
		fields = "__all__"


@admin.register(User)
class CondominiusUserAdmin(UserAdmin):
	form = CondominiusUserChangeForm
	add_form = CondominiusUserCreationForm
	fieldsets = UserAdmin.fieldsets + (("Perfil", {"fields": ("role",)}),)
	add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "role")}),)
	list_display = ("username", "email", "role", "is_staff")
	list_filter = UserAdmin.list_filter + ("role",)


admin.site.register(Condominius)
admin.site.register(Unity)
admin.site.register(Charge)
admin.site.register(Agreement)
admin.site.register(AgreementInstallment)