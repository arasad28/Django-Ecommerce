from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.base import Model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request
from django.utils import timezone
from django.views.generic import ListView,DetailView,View
from pkg_resources import require
from .models import Address, Item, OrderItem,Slider, Order,Review
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from .forms import CheckoutForm,SignupCreation,RatingForms

# import the logging library
import logging
import pdb

# Get an instance of a logger
logger = logging.getLogger('django')

class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider'] = Slider.objects.all()
        return context

class ItemDetails(DetailView):
        model = Item
        template_name = 'product.html'
        form = RatingForms()
        def get_context_data(self,**kwargs):
                context = super().get_context_data(**kwargs)
                context['form'] = self.form 
                context['review'] = Review.objects.order_by('-created_at')
                return context
        def post(self,request,*args, **kwargs):
                form = RatingForms(request.POST or None)
                logger.info('check')
                if form.is_valid():
                        logger.info('comming')
                        user = self.request.user
                        prodid = int(request.POST.get('prod_id')) # here
                        product = Item.objects.get(id=prodid)
                        rate = form.cleaned_data.get("rate")
                        comment = form.cleaned_data.get("comment")
                        review = Review(user = user,product = product, rate = rate ,comment = comment)
                        review.save()
                        return redirect('core:home')
                else:
                        user = self.request.user
                        prodid = int(request.POST.get('prod_id')) 
                        product = Item.objects.get(id=prodid)
                        rate = form.cleaned_data.get("rate")
                        comment = form.cleaned_data.get("comment")
                        review = Review(user = user,product = product, rate = rate ,comment = comment)
                        review.save()
                        logger.info("something went wrong")
                        return redirect('core:home')

def mobile_cat(request):
        mob=Item.objects.filter(category='Mobile')
        return render(request,'category/mobile.html',context={'mob':mob})       
def laptop_cat(request):
        lap=Item.objects.filter(category='Laptop')
        return render(request,'category/laptop.html',context={'lap':lap})       
def electronics_cat(request):
        elc=Item.objects.filter(category='Electronics')
        return render(request,'category/electronics.html',context={'elc':elc})       

class OrderSummaryView(LoginRequiredMixin,View):
        def get(self, *args, **kwargs):
                try:
                        order = Order.objects.get(user=self.request.user,ordered=False)
                        context = {
                                'object':order
                        }
                        return render(self.request,'cart.html',context)
                except ObjectDoesNotExist:
                        return redirect('/')
def search(request):
        qs = Item.objects.all()
        q = request.GET.get('q')
        if q:
                qs = qs.filter(
                        Q(title__icontains = q ) |
                        Q(description__icontains = q)|
                        Q(full_description__icontains = q)
                ).distinct()
                context = {
                'qs':qs
                }
                return render(request,'search.html',context)
                
def is_valid_form(values):
        valid=True
        for field in values:
                if field == '':
                        valid = False
        return valid
class AddressView(View):
        def get(self,*args,**kwargs):
                form = CheckoutForm
                form2 = SignupCreation
                context = {
                        'form':form,
                }
                return render(self.request,'address.html',context)
        def post(self,*args,**kwargs):
                form = CheckoutForm(self.request.POST or None)
                try:
                        order_qs = Order.objects.filter(ordered=False)
                        order = order_qs[0]
                        if form.is_valid():
                                address1 = form.cleaned_data.get('address1')
                                address2 = form.cleaned_data.get('address2')
                                country = form.cleaned_data.get('country')
                                state = form.cleaned_data.get('state')
                                zip = form.cleaned_data.get('zip')
                                if is_valid_form([address1,address2,state,country]):
                                        address = Address(
                                                        user = self.request.user,
                                                        street_address = address1,
                                                        appartment_address = address2,
                                                        state = state,
                                                        country = country,
                                                        zip = zip,
                                                        address_type = 'A',
                                                        default = True,

                                                        )
                                        address.save()
                                        order.address = address
                                        order.save()
                                return redirect('core:test')
                        return redirect('core:test')
                        
                                        
                except ObjectDoesNotExist:
                        return redirect('core:test')               
class CheckoutView(View):
        def get(self,*args,**kwargs):
                order = Order.objects.get(user=self.request.user,ordered=False)
                form = CheckoutForm
                context = {
                        'form':form,
                        'order':order
                }
                address_qs = Address.objects.filter(
                        user = self.request.user,
                        address_type = 'A',
                        default = True
                )
                if address_qs.exists():
                        context.update({
                                'address':address_qs[0]
                        })
                return render(self.request,'checkout.html',context)
        def post(self, *args, **kwargs):
                form = CheckoutForm(self.request.POST or None)
                try:
                        order = Order.objects.get(user=self.request.user,ordered=False)
                        if form.is_valid():
                                default_shipping_address =form.cleaned_data.get('default_shipping_address')
                                if default_shipping_address:
                                        address_qs = Address.objects.filter(user = self.request.user,address_type='A',default = True)
                                        order.address = address_qs[0]
                                        order.save()
                                        if address_qs.exists():
                                                address = address_qs[0]
                                                shipping_address = Address(
                                                        user = self.request.user,
                                                        street_address = address.street_address,
                                                        appartment_address = address.appartment_address,
                                                        country = address.country,
                                                        state = address.state,
                                                        zip = address.zip,
                                                        address_type = 'S',
                                                        default = True,
                                                )
                                                shipping_address.save()
                                                order.shipping_address = shipping_address
                                                
                                                order.save()
                                        else:
                                                return redirect ("core:checkout")
                                else:
                                        address1 = form.cleaned_data.get('address1')
                                        address2 = form.cleaned_data.get('address2')
                                        country = form.cleaned_data.get('country')
                                        state = form.cleaned_data.get('state')
                                        zip = form.cleaned_data.get('zip')
                                        if is_valid_form([address1,address2,state,country]):
                                                shipping_address = Address(
                                                        user = self.request.user,
                                                        street_address = address1,
                                                        appartment_address = address2,
                                                        state = state,
                                                        country = country,
                                                        zip = zip,
                                                        address_type = 'S',
                                                        default = True,

                                                )
                                                shipping_address.save()
                                                order.shipping_address = shipping_address
                                                order.save()
                                        else:
                                                return redirect ("core:checkout")
                                return redirect("core:checkout")
                                

                except ObjectDoesNotExist:
                        return redirect("core:cart")


@login_required
def add_to_cart(request,slug):
        item = get_object_or_404(Item,slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
                user = request.user,
                item = item,
                ordered = False
        )
        order_qs = Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(item__slug=item.slug).exists():
                        order_item.quantity +=1
                        order_item.save()
                        return redirect("core:cart")
                else:
                        order.items.add(order_item)
                        return redirect("core:cart")
        else:
                ordered_date = timezone.now()
                order = Order.objects.create(
                        user = request.user,ordered_date=ordered_date
                )
                order.items.add(order_item)
                return redirect("core:cart")

@login_required
def remove_from_cart(request,slug):
        item = get_object_or_404(Item,slug=slug)
        order_qs = Order.objects.filter(
                user=request.user,
                ordered=False
        )
        if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(item__slug=item.slug).exists():
                        order_item = OrderItem.objects.filter(
                                user=request.user,
                                item=item,
                                ordered=False
                        )[0]
                        order.items.remove(order_item)
                        return redirect("core:cart")
                else:
                        return redirect("core:product",slug=slug)
        else:
                return redirect("core:product",slug=slug)
        return redirect("core:product",slug=slug)

def remove_single_item_from_cart(request,slug):
        item = get_object_or_404(Item,slug=slug)
        order_qs = Order.objects.filter(
                user=request.user,
                ordered = False
        )
        if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(item__slug=item.slug).exists():
                        order_item = OrderItem.objects.filter(
                                user=request.user,
                                item=item,
                                ordered=False
                        )[0]
                        if order_item.quantity > 1:
                                order_item.quantity -= 1
                                order_item.save()
                        else:
                                order.items.remove(order_item)
                        return redirect("core:cart")
                else:
                        return redirect("core:cart")
        else:
                return redirect("core:product",slug=slug)
        return redirect("core:product",slug=slug)
class TestView(HomeView):
        model = Item
        template_name = 'test.html'
        # productId = request.POST.get('prod_id')
        # product = Item.objects.get(id=productId)
        # product = Item.objects.get()
        # logger.info(product)



        # cmnt = Review.objects.all().values_list('rate', flat=True).order_by('id')
        # co = 0
        # for cmn in cmnt:
        #         logger.info(cmn)
        #         co+=cmn
        # cm = int(cmnt.count())
        # rat = co/cm
        # # logger.info(rat)
        # def rating_count(slug):
        #         cmnt = Review.objects.filter(slug=slug).values_list('rate', flat=True).order_by('id')
        #         count = 0
        #         for cmn in cmnt:
        #                 count+=cmn
        #         co = int(cmnt.count())
        #         rat = count/co
        #         return rat
        # logger.info(rat)
        mob=Item.objects.filter(category='Mobile')
        logger.info(mob)