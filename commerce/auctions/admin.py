from django.contrib import admin
from .models import User, Comments, Listing, Bid, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)
