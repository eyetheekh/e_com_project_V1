from .models import Category, Order, Product, Vendor, Product_Images, Product_Review


def context_fn(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    if "cart_data_object" in request.session:
        cart_items_count = len(request.session['cart_data_object'])
    else:
        cart_items_count = 0

    context = {
        'categories_context': categories,
        'vendors_context': vendors,
        'cart_items_count_context': cart_items_count,
    }

    return context
