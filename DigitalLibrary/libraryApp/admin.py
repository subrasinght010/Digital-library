from django.contrib import admin
from .models import Item, BuyOrderitem,IssueOrderitem, Order, Payment, Refund, Address

# Register your models here.
admin.site.register(Item)
admin.site.register(IssueOrderitem)
admin.site.register(BuyOrderitem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Address)
