from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Model2D(models.Model):
    model2D_name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='models/2d/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model2D_name

class Model3D(models.Model):
    model3D_name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='models/3d/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model3D_name


class Product2D(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/product1/')
    model_2d = models.ForeignKey(Model2D, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product3D(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/product2/')
    model_3d = models.ForeignKey(Model3D, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    email = models.EmailField(null=True, blank=True)
    mobile_number1 = models.CharField(max_length=15, null=True, blank=True)
    mobile_number2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('shipped', 'Shipped')],
        default='pending',
    )

    def __str__(self):
        return f"Order {self.id} - {self.product}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    message = models.TextField()
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # Auto-approve feedback

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Anonymous'}"
    
class LikedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Generic relation to either Product2D or Product3D
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"
