
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


# =====================================
# 1. CATEGORY
# =====================================

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =====================================
# 2. PRODUCT
# =====================================

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.discount_price is not None:
            return self.discount_price
        return self.price


# =====================================
# 3. PRODUCT IMAGES
# =====================================

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/gallery/'
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.product.name} - Image"


# =====================================
# 4. CUSTOMER PROFILE
# =====================================

class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=15)

    profile_image = models.ImageField(
        upload_to='customers/',
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# =====================================
# 5. ADDRESS
# =====================================

class Address(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"


# =====================================
# 6. CART
# =====================================

class Cart(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.customer}"


# =====================================
# 7. CART ITEMS
# =====================================

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.product.name

    @property
    def subtotal(self):
        return self.product.final_price * self.quantity


# =====================================
# 8. ORDER
# =====================================

class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True
    )

    order_number = models.CharField(
        max_length=30,
        unique=True
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number


# =====================================
# 9. ORDER ITEMS
# =====================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        if self.product:
            return self.product.name
        return "Deleted product"


# =====================================
# 10. PAYMENT
# =====================================

class Payment(models.Model):

    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
        ('Card', 'Credit/Debit Card'),
        ('NetBanking', 'Net Banking'),
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Payment - {self.order.order_number}"


# =====================================
# 11. REVIEW
# =====================================

class Review(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars"


# =====================================
# 12. WISHLIST
# =====================================

class Wishlist(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )

    products = models.ManyToManyField(
        Product,
        blank=True
    )

    def __str__(self):
        return f"Wishlist - {self.customer}"


# =====================================
# 13. COUPON
# =====================================

class Coupon(models.Model):

    code = models.CharField(
        max_length=30,
        unique=True
    )

    discount_percentage = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
