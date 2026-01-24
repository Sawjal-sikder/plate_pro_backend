from django.db import models #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class PlateShape(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='plate_shapes/icons/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    points = models.JSONField(
        help_text="List of coordinate points [[x, y], [x, y], ...]"
    )
    closed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    
class PlateVariant(models.Model):
    plate_shape = models.ForeignKey(PlateShape, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    
class DrillingService(models.Model):
    name = models.CharField(max_length=255)
    price_per_hole = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    
    
class CartItem(models.Model): 

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Product
    plate_variant = models.ForeignKey(
        PlateVariant,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    # Service
    drilling_service = models.ForeignKey(
        DrillingService,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)
    holes_count = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.plate_variant:
            return f"CartItem {self.id} - {self.plate_variant.name} (x{self.quantity})"
        elif self.drilling_service:
            return f"CartItem {self.id} - {self.drilling_service.name} ({self.holes_count} holes)"
        return f"CartItem {self.id}"


class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    plate_variant = models.ForeignKey(
        PlateVariant,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    drilling_service = models.ForeignKey(
        DrillingService,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    holes_count = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.plate_variant:
            return f"OrderItem {self.id} - {self.plate_variant.name} (x{self.quantity})"
        elif self.drilling_service:
            return f"OrderItem {self.id} - {self.drilling_service.name} ({self.holes_count} holes)"
        return f"OrderItem {self.id}"
    
    





class Materials(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='material/icons/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Thickness(models.Model):
    materials = models.ForeignKey(Materials, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
   


class OrderPlate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tatalArea = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    totalPerimeter = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    thickness = models.ForeignKey(Thickness, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    totalDrilingHoles = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"OrderPlate {self.id} - {self.user.first_name}"


class OrderItemPlate(models.Model):
    order = models.ForeignKey(OrderPlate, on_delete=models.CASCADE, related_name='plate_items')
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='order_plate/icons/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    points = models.JSONField()
    drillingHole = models.JSONField()
    closed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"OrderItemPlate {self.id} - {self.name}"