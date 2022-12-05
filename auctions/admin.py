from django.contrib import admin
from .models import User, AuctionItem, Bid, Comment, Category
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=("id","username","email","first_name","last_name")

class AuctionItemAdmin(admin.ModelAdmin):
    list_display=("id","name","user")

class BidAdmin(admin.ModelAdmin):
    list_display=("user","amount","date_placed")

class CommentAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id","name")


admin.site.register(User,UserAdmin)
admin.site.register(AuctionItem,AuctionItemAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)