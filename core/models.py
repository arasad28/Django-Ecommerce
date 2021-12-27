from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django_resized import ResizedImageField
from django.db.models.signals import pre_save
from Ecommerce.utlis import unique_slug_generator
from PIL import Image
from tinymce.models import HTMLField 
from stdimage import StdImageField


address_choice=(
    ('A','Address'),
    ('S','Shipping'),
)
category_choice=(
    ('Electronics','Electronics'),
    ('Mobile','Mobile'),
    ('Laptop','Laptop'),
    ('Earphone','Earphone'),
    ('Android','Android'),
    ('Tshirt','T Shirt'),
    ('Shoe','Shoe'),
    ('Gadget','Gadget')
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

def upload_path(instance, filename):
        return 'image/{0}/{1}'.format(instance.slug, filename)

class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(choices=category_choice,max_length=20,blank=True,null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    image = models.ImageField()
    image2 = StdImageField(upload_to=upload_path,blank=True,null=True, variations={'thumbnail': (700, 820)})
    description = models.CharField(max_length=500)
    full_description = models.TextField()
    slug = models.SlugField(max_length=250,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("core:product",kwargs = {
            'slug' : self.slug
        })
    def add_to_cart(self):
        return reverse("core:add",kwargs = {
            'slug' : self.slug
        })
    def get_remove_from_cart(self):
        return reverse("remove",kwargs={
            'slug':self.slug
        })

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Item)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)

    # def get_products(self):
    #     return "\n".join([p.title for p in self.item.all()])

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_amount_product(self):
        return self.quantity * self.item.price
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    address = models.ForeignKey('Address',related_name='main_address',on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address = models.ForeignKey('Address',related_name='shipping_address',on_delete=models.SET_NULL,blank=True,null=True)

    


    def __str__(self):
        return self.user.username
    def total_amount(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_total_amount_product()
        return total

class Slider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    link = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.title

class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=200)
    appartment_address=models.CharField(max_length=200)
    country = CountryField()
    state = models.CharField(max_length=100,blank=True,null=True)
    zip = models.CharField(max_length=100)
    address_type=models.CharField(max_length=1,choices=address_choice)
    default=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural='addresses'

class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Item,models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
