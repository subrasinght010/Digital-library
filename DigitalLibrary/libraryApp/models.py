from django.db import models
from django.shortcuts import render,reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import DateTimeField
from django.db.models.signals import post_save
from autoslug import AutoSlugField
from django_countries.fields import CountryField
# Create your models here.
CATEGORY_CHOICES  = (
('Action','Action'),
('Si-Fiction','Fiction'),
('Thriller','Thriller'),
('Drama','Drama'),
('Crime','Crime'),
('Romance','Romance'),
('None','None')
)
TYPE_OF_BOOK = (
('Accademics','Accademics'),
('Novels','Novels'),
('Exams','Exams'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    """docstring for Item."""
    title = models.CharField(max_length=100)
    auther = models.CharField(max_length=100)
    ordered_date = models.DateTimeField(auto_now_add=True,)
    price = models.FloatField(max_length=10)
    course = models.CharField(max_length=50,blank=True, null=True)
    branch = models.CharField(max_length=50,blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True,)
    geners = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    category =  models.CharField(choices=TYPE_OF_BOOK, max_length=15)
    image = models.ImageField(upload_to='productimg')
    slug = AutoSlugField(populate_from='title', unique_with=['auther', 'publish_date'],unique=True,blank=True, null=True,default=None,)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("libraryApp:productdetail", kwargs={
            "slug": self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("libraryApp:add-to-cart", kwargs={
            "slug": self.slug
        })

    def get_add_to_cart_issue_url(self):
        return reverse("libraryApp:add-to-cart-issue", kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("libraryApp:remove-from-cart", kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_isuue_url(self):
        return reverse("libraryApp:remove-from-cart-issue", kwargs={
            "slug": self.slug
        })


class IssueOrderitem(models.Model):
    """docstring for Orederitem."""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_issue_price(self):
        return self.quantity * 60

    def get_final_issue_price(self):
        return self.get_total_item_issue_price()


class BuyOrderitem(models.Model):
    """docstring for Orederitem."""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()



class Order(models.Model):
    """docstring for Order."""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(BuyOrderitem,)
    itemss = models.ManyToManyField(IssueOrderitem,)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total_for_buy=0
        total_for_issue=0
        x=0
        shipping_charge=0
        for order_item in self.items.all():
            total_for_buy += order_item.get_final_price()
        for order_items in self.itemss.all():
            total_for_issue += order_items.get_final_issue_price()
        total = (total_for_buy+total_for_issue)
        if total >=500:
            x=total
            shipping_charge =0
        elif total==0:
            x=total
            shipping_charge= 0
        else:
            x=(total+70)
            shipping_charge= 70
        return ({'total_for_buy':total_for_buy,'total_for_issue':total_for_issue,'x':x,'shipping_charge':shipping_charge})






class Address(models.Model):
    """docstring for Address."""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    StateName = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    """docstring for Payment."""
    user = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Refund(models.Model):
    """docstring for Refund."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
