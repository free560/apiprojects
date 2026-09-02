from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Wallet)
admin.site.register(AdminWallet)
admin.site.register(Transaction)
admin.site.register(WithdrawalRequest)