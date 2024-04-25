from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Category, Product, Vendor, Product_Images, Product_Review, Address, Order, CartOrderItems, Contact_Us
from taggit.models import Tag
from .forms import Product_Review_Form, Address_Form
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from paypal.standard.forms import PayPalPaymentsForm


def home(request):

    feartured_products = Product.objects.filter(featured_on_home_page=True)
    latest_products = Product.objects.filter().order_by('-date_added')[:4]
    categories = Category.objects.all().order_by('?')[:4]

    deal_products = Product.objects.filter().order_by('-discount_amount')[:8]

    context = {
        "feartured_products": feartured_products,
        'latest_products': latest_products,
        'categories': categories,
        'deal_products': deal_products
    }
    return render(request, 'core/index.html', context)


def product_detail_view(request, PID):

    product = get_object_or_404(Product, PID=PID)
    product_images = Product_Images.objects.filter(product=product)
    print(product_images)

    if request.method == "POST":
        Product_Review.objects.create(
            review=request.POST['review'],
            rating=request.POST['rating'],
            user=request.user,
            product=product,
        )
        messages.success(request, 'Review Added')

        # messages.error(request, 'Review cannot be added')

    reviews_of_product = Product_Review.objects.filter(product=product)
    related_products = Product.objects.filter(
        category=product.category).exclude(PID=product.PID)

    can_review = True
    if request.user.is_authenticated:
        user_reviews = Product_Review.objects.filter(
            product=product, user=request.user)

        if len(user_reviews) > 0:
            can_review = False

    form = Product_Review_Form()

    context = {
        'product': product,
        "related_products": related_products,
        'reviews_of_product': reviews_of_product,
        'can_review': can_review,
        'form': form,
        "product_images": product_images
    }
    return render(request, 'core/product_detail_view.html', context)


def category_detail_view(request, CID):
    category = get_object_or_404(Category, CID=CID)
    products_in_category = Product.objects.filter(category=category)
    context = {
        'products_in_category': products_in_category,
        'category': category,
    }
    return render(request, 'core/category_view.html', context)


def category_list_view(request):
    all_categories = Category.objects.all()

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'core/all_categories.html', context)


def vendor_detail_view(request, VID):
    vendor = get_object_or_404(Vendor, VID=VID)
    products_of_vendor = Product.objects.filter(vendor=vendor)

    context = {
        'vendor': vendor,
        'products_of_vendor': products_of_vendor
    }
    return render(request, 'core/vendor_details.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor_list.html', context)


def vendor_shop_view(request, VID):
    vendor = get_object_or_404(Vendor, VID=VID)
    products_of_vendor = Product.objects.filter(vendor=vendor)

    context = {
        'vendor': vendor,
        'products_of_vendor': products_of_vendor
    }
    return render(request, 'core/vendor_shop.html', context)


def tag_detail_view(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    tag_products = Product.objects.filter(tags=tag)

    context = {
        'tag_products': tag_products,
        'tag': tag,
    }
    return render(request, 'core/tag_detail_view.html', context)


def search(request):
    query = request.GET.get('q')
    products = None  # Initialize as empty queryset

    if len(query) > 0:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(desc__icontains=query))

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'core/search.html', context)


# def add_to_cart(request):
#     id = request.GET['id']
#     product = get_object_or_404(Product, id=id)

#     cart_product = {}
#     cart_product[id] = {

#         'title': product.title,
#         'quantity': request.GET['quantity'],
#         'price': str(product.price_after_discount()),
#     }

#     print(cart_product)

#     if 'cart_data_object' in request.session:
#         if id in request.session['cart_data_object']:
#             cart_data = request.session['cart_data_object']
#             cart_data[id]["quantity"] = cart_product[id]["quantity"]
#             cart_data.update(cart_data)
#             request.session['cart_data_object'] = cart_data
#         else:
#             cart_data = request.session['cart_data_object']
#             cart_data.update(cart_product)
#             request.session['cart_data_object'] = cart_data
#     else:
#         request.session['cart_data_object'] = cart_product

#     print(request.session['cart_data_object'])

#     return JsonResponse({
#         "data": request.session['cart_data_object'],
#         "no_of_cart_items": len(request.session['cart_data_object']),
#         "boolean": True
#     })
def add_to_cart(request):
    id = request.GET['id']
    product = get_object_or_404(Product, id=id)
    quantity = int(request.GET['quantity'])

    cart_product = {
        'title': product.title,
        'quantity': quantity,
        'price': str(product.price_after_discount()),
    }

    # print(cart_product)

    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']
        if id in cart_data:
            # If product already exists in cart, increment the quantity
            # cart_data[id]["quantity"] += int(quantity)
            cart_data[id]["quantity"] = int(
                cart_data[id]["quantity"]) + quantity

        else:
            # If product doesn't exist in cart, add it
            cart_data[id] = cart_product
        request.session['cart_data_object'] = cart_data
    else:
        request.session['cart_data_object'] = {id: cart_product}

    # print(request.session['cart_data_object'])

    return JsonResponse({
        "data": request.session['cart_data_object'],
        "no_of_cart_items": len(request.session['cart_data_object']),
        "boolean": True
    })


def cart_view(request):
    list_of_products_in_cart = list()

    if 'cart_data_object' not in request.session:
        messages.warning(
            request, 'Your Cart is empty, Add items to Your Cart!')
        return redirect('core:home')

    else:
        # print(request.session['cart_data_object'])
        id_of_products = [i for i in request.session['cart_data_object']]

        list_of_products_in_cart = [
            Product.objects.get(id=i) for i in id_of_products]
        # print(list_of_products_in_cart)

        cart_dict = dict()

        for i in list_of_products_in_cart:
            cart_dict[i] = request.session['cart_data_object'][str(
                i.id)]['quantity']

        # print('cart_dict: ', cart_dict)

        cart_dict_with_price_and_qty = dict()
        for i, j in cart_dict.items():
            # print(i, j)
            cart_dict_with_price_and_qty[i] = {
                "quantity": j,
                "sub_total": i.price_after_discount() * int(j)
            }

        # print('cart____', cart_dict_with_price_and_qty)

        cart_total = 0
        for i, j in cart_dict_with_price_and_qty.items():
            # print(i, j)
            cart_total += j['sub_total']

        total_cart_items = len(list_of_products_in_cart)

    context = {
        'total_cart_items': total_cart_items,
        'cart_dict_with_price_and_qty': cart_dict_with_price_and_qty,
        'cart_total': cart_total,
    }
    return render(request, 'core/cart.html', context)


def delete_product_from_cart(request):
    id = request.GET['id']
    # print(id)

    temp_dict = request.session['cart_data_object']
    temp_dict.pop(id)
    request.session['cart_data_object'] = temp_dict

    ####################################################

    id_of_products = [i for i in request.session['cart_data_object']]

    list_of_products_in_cart = [
        Product.objects.get(id=i) for i in id_of_products]
    # print(list_of_products_in_cart)

    cart_dict = dict()

    for i in list_of_products_in_cart:
        cart_dict[i] = request.session['cart_data_object'][str(
            i.id)]['quantity']

    # print('cart_dict: ', cart_dict)

    cart_dict_with_price_and_qty = dict()
    for i, j in cart_dict.items():
        # print(i, j)
        cart_dict_with_price_and_qty[i] = {"quantity": j,
                                           "sub_total": i.price_after_discount() * int(j)}

    # print('cart____', cart_dict_with_price_and_qty)

    cart_total = 0
    for i, j in cart_dict_with_price_and_qty.items():
        # print(i, j)
        cart_total += j['sub_total']

    total_cart_items = len(list_of_products_in_cart)

    context = render_to_string('core/async/cart_async.html', {
        'total_cart_items': total_cart_items,
        'cart_dict_with_price_and_qty': cart_dict_with_price_and_qty,
        'cart_total': cart_total,
    })

    return JsonResponse({
        'context': context,
        'total_cart_items': total_cart_items
    })


def update_from_cart(request):
    id = request.GET.get('id')
    quantity = request.GET['quantity']

    temp_dict = request.session['cart_data_object']
    print(temp_dict[id])
    temp_dict[id]['quantity'] = quantity
    request.session['cart_data_object'] = temp_dict

    ####################################################

    id_of_products = [i for i in request.session['cart_data_object']]

    list_of_products_in_cart = [
        Product.objects.get(id=i) for i in id_of_products]
    # print(list_of_products_in_cart)

    cart_dict = dict()

    for i in list_of_products_in_cart:
        cart_dict[i] = request.session['cart_data_object'][str(
            i.id)]['quantity']

    # # print('cart_dict: ', cart_dict)

    cart_dict_with_price_and_qty = dict()
    for i, j in cart_dict.items():
        # print(i, j)
        cart_dict_with_price_and_qty[i] = {"quantity": j,
                                           "sub_total": i.price_after_discount() * int(j)}

    # # print('cart____', cart_dict_with_price_and_qty)

    cart_total = 0
    for i, j in cart_dict_with_price_and_qty.items():
        # print(i, j)
        cart_total += j['sub_total']

    total_cart_items = len(list_of_products_in_cart)

    context = render_to_string('core/async/cart_async.html', {
        'total_cart_items': total_cart_items,
        'cart_dict_with_price_and_qty': cart_dict_with_price_and_qty,
        'cart_total': cart_total,
    })

    return JsonResponse({
        'context': context,
        'total_cart_items': total_cart_items,
        "bool": True
    })


@login_required
def update_address(request):
    if request.method == "POST":
        address_form = Address_Form(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            if new_address.default_address:
                temp_address = Address.objects.filter(user=request.user)
                temp_address.update(default_address=False)
            new_address.save()
            messages.success(request, 'Address added!')
            return redirect('core:checkout_view')

    address_form = Address_Form()
    return render(request, 'core/update_address.html', {'form': address_form})


@login_required
def checkout_view(request):
    if request.method == "POST":
        address_form = Address_Form(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            if new_address.default_address:
                temp_address = Address.objects.filter(user=request.user)
                temp_address.update(default_address=False)
            new_address.save()
            messages.success(request, 'Address added!')

    address_form = Address_Form()

    all_address = Address.objects.filter(user=request.user)
    try:
        default_address = Address.objects.get(
            user=request.user, default_address=True)
    except:
        default_address = None

    list_of_products_in_cart = list()

    if 'cart_data_object' not in request.session:
        messages.warning(
            request, 'Your Cart is empty, Add items to Your Cart!')
        return redirect('core:home')

    else:
        # print(request.session['cart_data_object'])
        id_of_products = [i for i in request.session['cart_data_object']]

        list_of_products_in_cart = [
            Product.objects.get(id=i) for i in id_of_products]
        # print(list_of_products_in_cart)

        cart_dict = dict()

        for i in list_of_products_in_cart:
            cart_dict[i] = request.session['cart_data_object'][str(
                i.id)]['quantity']

        # print('cart_dict: ', cart_dict)

        cart_dict_with_price_and_qty = dict()
        for i, j in cart_dict.items():
            # print(i, j)
            cart_dict_with_price_and_qty[i] = {
                "quantity": j,
                "sub_total": i.price_after_discount() * int(j)
            }

        # print('cart____', cart_dict_with_price_and_qty)

        cart_total = 0
        for i, j in cart_dict_with_price_and_qty.items():
            # print(i, j)
            cart_total += j['sub_total']

        total_cart_items = len(list_of_products_in_cart)

        order, created_ = Order.objects.get_or_create(
            user=request.user,
            order_quantity=total_cart_items,
            order_price=cart_total
        )

        for i, j in cart_dict_with_price_and_qty.items():
            print(i, '::', j)
            order_item = CartOrderItems.objects.get_or_create(
                order=order,
                item=i,
                quantity=j['quantity'],
                price=i.price,
                total=j['sub_total'],
            )

        # deleting items that is not assosiated with the current order and those which are only of the current user
        other_order_items = CartOrderItems.objects.exclude(
            order=order).filter(order__user=request.user, order__paid_status=False)
        other_order_items.delete()

        # deleting order that is not assosiated with the current order and those which are only of the current user
        other_orders = Order.objects.exclude(
            pk=order.pk).filter(user=request.user, paid_status=False)
        other_orders.delete()

    paypal_dict = {
        "business": "bizaytheeh@gmail.com",
        "amount": cart_total,
        "item_name": str(order.Invoice),
        "invoice": "INV:"+str(order.Invoice),
        "notify_url": request.build_absolute_uri(reverse('core:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('core:order-success')),
        "cancel_return": request.build_absolute_uri(reverse('core:order-failed')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'total_cart_items': total_cart_items,
        'cart_dict_with_price_and_qty': cart_dict_with_price_and_qty,
        'cart_total': cart_total,
        'form': form,
        'address_form': address_form,
        'default_address': default_address,
    }
    return render(request, 'core/checkout.html', context)


@login_required
def order_success(request):
    order = Order.objects.filter(user=request.user).latest('order_date')
    order.paid_status = True
    order.save()

    ordered_items = CartOrderItems.objects.filter(order=order)

    context = {
        'ordered_items': ordered_items,
        'order': order
    }
    return render(request, 'core/order_success.html', context)


def order_failed(request):
    return render(request, 'core/order_failed.html')


@login_required
def buy_now(request, PID):
    product = get_object_or_404(Product, PID=PID)

    if request.method == "POST":
        address_form = Address_Form(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            if new_address.default_address:
                temp_address = Address.objects.filter(user=request.user)
                temp_address.update(default_address=False)
            new_address.save()
            messages.success(request, 'Address added!')

    try:
        default_address = Address.objects.get(
            user=request.user, default_address=True)
    except:
        default_address = None

    address_form = Address_Form()

    order, created_ = Order.objects.get_or_create(
        user=request.user,
        order_quantity=1,
        order_price=product.price_after_discount()
    )

    order_item = CartOrderItems.objects.get_or_create(
        order=order,
        item=product,
        quantity=1,
        price=product.price_after_discount(),
        total=product.price_after_discount(),
    )

    # deleting items that is not assosiated with the current order and those which are only of the current user
    other_order_items = CartOrderItems.objects.exclude(
        order=order).filter(order__user=request.user, order__paid_status=False)
    other_order_items.delete()

    # deleting order that is not assosiated with the current order and those which are only of the current user
    other_orders = Order.objects.exclude(
        pk=order.pk).filter(user=request.user, paid_status=False)
    other_orders.delete()

    paypal_dict = {
        "business": "bizaytheeh@gmail.com",
        "amount": product.price_after_discount(),
        "item_name": str(order.Invoice),
        "invoice": "INV:"+str(order.Invoice),
        "notify_url": request.build_absolute_uri(reverse('core:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('core:order-success')),
        "cancel_return": request.build_absolute_uri(reverse('core:order-failed')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        "product": product,
        "default_address": default_address,
        "address_form": address_form,
        'form': form,
        'total_cart_items': 1,
        'cart_total': product.price_after_discount(),
    }
    return render(request, 'core/buy_now.html', context)


@login_required
def dashboard(request):
    orders = Order.objects.filter(
        user=request.user, paid_status=True).order_by('-order_date')

    order_and_ordered_items = {
        i: CartOrderItems.objects.filter(order=i) for i in orders
    }

    context = {
        'orders': orders,
        "order_and_ordered_items": order_and_ordered_items
    }
    return render(request, 'core/dashboard.html', context)


def order_details(request, Invoice):
    order = get_object_or_404(Order, Invoice=Invoice)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'core/order_details.html', context)


@login_required
def dashboard_address(request):
    address = Address.objects.filter(user=request.user)
    address_form = Address_Form()
    context = {
        'address': address,
        'address_form': address_form
    }
    return render(request, 'core/dashboard_address.html', context)


def dashboard_update_address(request, id):
    address = get_object_or_404(Address, id=id)
    if request.method == "POST":
        address_form = Address_Form(request.POST, instance=address)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            if new_address.default_address:
                temp_address = Address.objects.filter(user=request.user)
                temp_address.update(default_address=False)
            new_address.save()
            messages.success(request, 'Address added!')
        else:
            messages.error(request, "Updating Failed")
    form = Address_Form(instance=address)
    context = {
        'address': address,
        'form': form
    }
    return render(request, 'core/dashboard_address_update.html', context)


@login_required
def my_reviews(request):
    user = request.user
    reviews = Product_Review.objects.filter(user=user)
    return render(request, 'core/my_reviews.html', {'reviews': reviews})


def delete_review(request, id):
    user = request.user
    review = get_object_or_404(Product_Review, id=id)
    review.delete()
    return redirect('core:my_reviews')


def about_us(request):
    return render(request, 'core/about.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        new_contact_us = Contact_Us.objects.create(
            name=name,
            email=email,
            message=message
        )
        if new_contact_us:
            messages.success(request, 'Message Sent!')
        else:
            messages.error(request, 'Message Sending Failed!')
    return render(request, 'core/contact.html')
