from django.contrib import admin

from sim_page.models import SimCard, MobileOperator, SIMOwner

# Register your models here.


class SimCardsAdmin(admin.ModelAdmin):
    list_display = ('sim_number', 'name', 'balance', 'owner')
    ordering = ['sim_number']
    list_filter = ('owner', 'cell_operator', 'balance_renewal_in_progress')
    save_as = True


admin.site.register(SimCard, SimCardsAdmin)
admin.site.register(MobileOperator)
admin.site.register(SIMOwner)
