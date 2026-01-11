from django.db import models #type: ignore

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