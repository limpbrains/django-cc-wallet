from django.contrib import admin

from wallet import models


class ProxyWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet')

admin.site.register(models.ProxyWallet, ProxyWalletAdmin)
