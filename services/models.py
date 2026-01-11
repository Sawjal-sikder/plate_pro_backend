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
    CART_ITEM_TYPE = (
        ("variant", "Plate Variant"),
        ("drilling", "Drilling Service"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20, choices=CART_ITEM_TYPE)

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

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"CartItem {self.id} - {self.item_type}"
