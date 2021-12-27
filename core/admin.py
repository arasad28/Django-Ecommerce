from django.contrib import admin

from .models import Item,Slider,OrderItem,Order,Address,Review
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields= ('full_description',)

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        'address',
        'shipping_address',
        'ordered_date',
        
    ]
    list_display_links = [
        'address',
        'shipping_address',
        'user'
    ]
    list_filter = [
        'ordered',
    ]
    search_fields = ['user__username']

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'appartment_address',
        'state',
        'zip',
        'country',
        'address_type',
        'default'
    ]
    list_filter = ['address_type','country']
    search_fields = ['user','street_address','appartment_address','state','zip']
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields=('created_at',)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['get_products']
    def get_products(self, obj):
        return "\n".join([p.title for p in obj.item.filter(user=self.user)])

admin.site.register(Review,ReviewAdmin)
admin.site.register(Item,PostAdmin)
admin.site.register(Slider)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Address,AddressAdmin)
