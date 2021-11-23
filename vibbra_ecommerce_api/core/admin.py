from django.contrib import admin

from vibbra_ecommerce_api.core.models import Bid, Deal, PhotoDeal, UrgencyDeal

# Register your models here.
admin.site.register(Deal)
admin.site.register(PhotoDeal)
admin.site.register(UrgencyDeal)
admin.site.register(Bid)
