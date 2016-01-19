from django.contrib import admin
from restaurante.models import Bar,Tapa
#from restaurante.models import UserProfile2
#from django.contrib.auth.models import User
# Register your models here.

class TapaAdmin(admin.ModelAdmin):
	list_display=('bar','nombre','votos')

class BarAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('nombre',)}
	list_display=('nombre','direccion','numerovisitas')

admin.site.register(Bar,BarAdmin)
admin.site.register(Tapa,TapaAdmin)
#admin.site.register(UserProfile)
#admin.site.register(User)

