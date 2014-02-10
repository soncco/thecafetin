from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext as _
from core.models import Local, Habitacion, Punto, Cliente, Tipo, Plato, PrecioPlato, Pedido, Visitante

class HabitacionAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'pertenece_a',)
  list_filter = ('pertenece_a',)

class PuntoAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'pertenece_a',)
  list_filter = ('pertenece_a',)

class ClienteAdmin(admin.ModelAdmin):
  list_display = ('__unicode__', 'habitacion', 'ingreso', 'salida', 'activo')
  list_filter = ('activo', 'ingreso', 'salida',)
  search_fields = ['nombres', 'apellidos']

  def queryset(self, request):
    qs = super(ClienteAdmin, self).queryset(request)
    qs = qs.filter(~Q(nombres = 'Foraneo'))
    return qs

class TipoAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'recibo',)

class PrecioInline(admin.TabularInline):
  model = PrecioPlato

class PlatoAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'tipo',)
  inlines  = [PrecioInline, ]
  list_filter = ('tipo',)
  filter_vertical = ('de_venta_en',)
  search_fields = ['nombre',]

class VisitanteAdmin(admin.ModelAdmin):
  list_display = ('nombres', 'local')
  list_filter = ('local',)
  search_fields = ['nombres']


admin.site.register(Local)
admin.site.register(Habitacion, HabitacionAdmin)
admin.site.register(Punto, PuntoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Visitante, VisitanteAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Plato, PlatoAdmin)
admin.site.register(Pedido)

class MyUserAdmin(UserAdmin):
  def completo(self, obj):
    return "%s %s" % (obj.first_name, obj.last_name)

  def grupos(self, obj):
    gs = ""
    for grupo in obj.groups.all():
      gs += grupo.name + " "

    return gs

  list_display = ('username', 'completo', 'grupos',)
  list_display_links = ('username',)

  fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Staff'), {'fields': ('is_staff',)}),
        (_('Groups'), {'fields': ('groups',)}),
    )

  def queryset(self, request):
    qs = super(MyUserAdmin, self).queryset(request)
    qs = qs.filter(~Q(username = 'brau'))
    return qs

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)