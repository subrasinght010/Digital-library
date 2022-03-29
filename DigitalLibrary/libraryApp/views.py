from django.views.generic import TemplateView,ListView, DetailView
from django.contrib.auth import login, logout
from .forms import CheckoutForm,PaymentForm
from .models import Item,BuyOrderitem,IssueOrderitem, Order, Payment, Refund, Address
from .forms import UserRegistrationForm
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import render,reverse,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
import string
import stripe




def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "libraryApp/roducts.html", context)


# Create your views here.
class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "libraryApp/home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "libraryApp/productdetail.html"



class UserRegistrationView(View):
    def get(self,request):
        form = UserRegistrationForm()
        return render(request,'libraryApp/signup.html',{'form':form})
    def post(self,request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'You Have Successfully Signup !')
            form.save()
        return render(request,'libraryApp/signup.html',{'form':form})

"""class OrderSummaryView(TemplateView):
    template_name = "libraryApp/order-summary.html"""
class OrderSummaryView(View):
    def get(self,request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(request,"libraryApp/order-summary.html", context)
        except ObjectDoesNotExist:
            return redirect("/")


"""def OrderSummaryView(request):
    return render(request,"libraryApp/order-summary.html")"""

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = BuyOrderitem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("libraryApp:order-summary")
        else:
            order.items.add(order_item)
            return redirect("libraryApp:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return render(request,'libraryApp/order-summary.html')

def add_to_cart_issue(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_items, created = IssueOrderitem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.itemss.filter(item__slug=item.slug).exists():
            order_items.quantity += 1
            order_items.save()
            return redirect("libraryApp:order-summary")
        else:
            order.itemss.add(order_items)
            return redirect("libraryApp:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.itemss.add(order_items)
    return render(request,'libraryApp/order-summary.html')

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = BuyOrderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("libraryApp:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("libraryApp:productdetail",slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("libraryApp:productdetail", slug=slug)

def remove_from_cart_issue(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.itemss.filter(item__slug=item.slug).exists():
            order_items = IssueOrderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.itemss.remove(order_items)
            order_items.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("libraryApp:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("libraryApp:productdetail",slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("libraryApp:productdetail", slug=slug)


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = BuyOrderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("libraryApp:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("libraryApp:productdetail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("libraryApp:productdetail", slug=slug)

def remove_single_item_from_cart_issue(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.itemss.filter(item__slug=item.slug).exists():
            order_items = IssueOrderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_items.quantity > 1:
                order_items.quantity -= 1
                order_items.save()
            else:
                order.itemss.remove(order_item1)
            messages.info(request, "This item quantity was updated.")
            return redirect("libraryApp:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("libraryApp:productdetail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("libraryApp:productdetail", slug=slug)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})
            return render(self.request, "libraryApp/checkout.html", context)
        except ObjectDoesNotExist:
            return redirect("libraryApp:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('libraryApp:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    State_Name = form.cleaned_data.get(
                                'State_Name')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip,State_Name]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            StateName=State_Name,
                            country=shipping_country,
                            zip=shipping_zip,
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'G':
                    return redirect('libraryApp:payment', payment_option='Gpay')
                elif payment_option == 'S':
                    return redirect('libraryApp:payment', payment_option='Stripe')
                elif payment_option == 'P':
                    return redirect('libraryApp:payment', payment_option='Paytm')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('libraryApp:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.shipping_address:
            context = {
                'order': order,
            }
            #userprofile = self.request.user.userprofile
            return render(self.request, "libraryApp/payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a shipping address")
            return redirect("libraryApp:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total())

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="Rs",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
