from django.contrib import admin
from .models import Categorey,Listing,comments,User,Bid
# Register your models here.
admin.site.register(Listing)
admin.site.register(Categorey)
admin.site.register(comments)
admin.site.register(User)
admin.site.register(Bid)
