from django.contrib import admin

from .models import Listings
from .models import User
from .models import Watchlist
from .models import Bids
from .models import Comments


# Register your models here.
admin.site.register(Listings),
admin.site.register(User),
admin.site.register(Watchlist),
admin.site.register(Bids),
admin.site.register(Comments)
