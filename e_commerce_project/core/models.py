from django.db import models

# uuid
from shortuuid.django_fields import ShortUUIDField
from userauth.models import customUser
# tag
from taggit.managers import TaggableManager


class Category(models.Model):
    CID = ShortUUIDField(
        unique=True, prefix='CAT:', length=10, max_length=15)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Category_images')
    desc = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Vendor(models.Model):
    VID = ShortUUIDField(unique=True, length=10, prefix="VEN:", max_length=15)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Vendor_images')
    desc = models.CharField(max_length=600, blank=True,
                            null=True, default='description for vendor')
    user = models.ForeignKey(
        customUser, related_name='vendor_user', on_delete=models.SET_NULL, null=True)
    address = models.CharField(
        max_length=500, default="ABC 2nd St Kdl Kollm Kerla Ind")
    contact = models.CharField(max_length=20, default='+91 9999955555')
    message_response_time = models.CharField(max_length=10, default='2 Days')
    shipping_time = models.CharField(max_length=10, default='4 Days')
    authentic_rating = models.CharField(max_length=10, default='100%')
    return_days = models.CharField(max_length=10, default='7 Days')
    warrenty_period = models.CharField(max_length=10, default='30 Days')

    def __str__(self):
        return self.title


Product_Choices = (
    ('active', 'Active'),
    ('disabled', 'Disabled'),
    ('in-review', 'In Review'),
    ('rejected', 'Rejected'),
)

order_Status_Choices = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)


Product_Rating = (
    ('1', '★☆☆☆☆'),
    ('2', '★★☆☆☆'),
    ('3', '★★★☆☆'),
    ('4', '★★★★☆'),
    ('5', '★★★★★'),
)


class Product(models.Model):
    PID = ShortUUIDField(
        unique=True, length=10, prefix="PID:", max_length=15)
    title = models.CharField(max_length=100, default='Sample')
    desc = models.CharField(
        max_length=500, default='lorem lroeam ipsm lorem doooi')
    specifications = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='product_category')
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_vendor')
    image = models.ImageField(upload_to='Product_images')
    # stock = models.IntegerField(default=100)
    in_stock = models.BooleanField(default=True)
    featured_on_home_page = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=12, decimal_places=2, default='4.99')
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    product_status = models.CharField(
        max_length=20, choices=Product_Choices, default='active')
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    tags = TaggableManager(blank=True)

    # use this method for price

    def price_after_discount(self):
        return self.price - self.discount_amount

    def discount_percentage(self):
        if self.price > 0:
            return (self.discount_amount / self.price) * 100
        else:
            return 0

    def __str__(self):
        return self.title


class Product_Images(models.Model):
    product = models.ForeignKey(
        Product, related_name='images_for_product', on_delete=models.CASCADE, null=True, blank=True)
    images = models.ImageField(upload_to="Multiple_Images/")

    class Meta:
        verbose_name_plural = 'Product_Images'

    def __str__(self):
        return self.product.title


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################


# class Order():
#     user = models.ForeignKey(
#         customUser, on_delete=models.CASCADE, related_name='order_of_user')
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name='order_products')
#     quantity = models.IntegerField(default=0)
#     order_price = models.DecimalField(max_digits=12, decimal_places=2)
#     paid_status = models.BooleanField(default=False)
#     order_date = models.DateTimeField(auto_now_add=True)
#     order_status = models.CharField(
#         max_length=20, choices=order_Status_Choices, default='processing')


class Order(models.Model):
    user = models.ForeignKey(
        customUser, on_delete=models.CASCADE, related_name='order_of_user')

    Invoice = models.AutoField(primary_key=True)

    order_quantity = models.IntegerField()
    order_price = models.DecimalField(max_digits=12, decimal_places=2)

    order_status = models.CharField(
        max_length=20, choices=order_Status_Choices, default='processing')
    paid_status = models.BooleanField(default=False)

    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Invoice}"


class CartOrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(
        max_digits=9999999, decimal_places=2, default="1.99")
    total = models.DecimalField(
        max_digits=9999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.item.title}"


class Product_Review(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    rating = models.IntegerField(choices=Product_Rating, default=None)
    review = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(
        customUser, on_delete=models.CASCADE)
    address = models.TextField()
    default_address = models.BooleanField(default=True)
    contact = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.address


contact_us_Status_choices = (
    ('Initiated', 'Initiated'),
    ('Solved', 'Solved'),
)


class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(
        max_length=20, choices=contact_us_Status_choices, default="Initiated")
