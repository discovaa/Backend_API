from django.db import models


from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from django.conf import settings
from decimal import Decimal
from ckeditor_uploader.fields import RichTextUploadingField
from html import unescape
from django.utils.html import strip_tags, mark_safe
from django_ckeditor_5.fields import CKEditor5Field



STATUS = (
    ("live", "Live"),
    ("in_review", "In review"),
    ("pending", "Pending"),
    ("cancelled", "Cancelled"),
    ("finished", "Finished"),
)

AVAILABILITY = (
    ("open", "Open Now"),
    ("closed", "Closed"),
    ("unavailable", "Unavailable"),
)


class Category(models.Model):
    cid = ShortUUIDField(length=5, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    image = models.ImageField(upload_to="category", blank=True, null=True, default="category.jpg")
    title = models.CharField(max_length=1000)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Category"

    def __str__(self):
        return f"{self.title}"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))



class Service(models.Model):
    sid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    image = models.ImageField(upload_to="auth_api.user_directory_path", default="service.jpg")
    user = models.ForeignKey("auth_api.User", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000)
    description = CKEditor5Field(config_name='extends')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=1.99)
    keywords = TaggableManager()
    phone = models.CharField(max_length=1000)
    
    address = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    zipcode = models.CharField(max_length=1000)
    longitude = models.CharField(max_length=1000)
    latitude = models.CharField(max_length=1000)

    # Opending and Closing Time
    monday_open = models.TimeField(auto_now_add=False)
    monday_close = models.TimeField(auto_now_add=False)
    monday_available = models.BooleanField(default=True)

    tuesday_open = models.TimeField(auto_now_add=False)
    tuesday_close = models.TimeField(auto_now_add=False)
    tuesday_available = models.BooleanField(default=True)


    wednesday_open = models.TimeField(auto_now_add=False)
    wednesday_close = models.TimeField(auto_now_add=False)
    wednesday_available = models.BooleanField(default=True)


    thursday_open = models.TimeField(auto_now_add=False)
    thursday_close = models.TimeField(auto_now_add=False)
    thursday_available = models.BooleanField(default=True)


    friday_open = models.TimeField(auto_now_add=False)
    friday_close = models.TimeField(auto_now_add=False)
    friday_available = models.BooleanField(default=True)


    saturday_open = models.TimeField(auto_now_add=False)
    saturday_close = models.TimeField(auto_now_add=False)
    saturday_available = models.BooleanField(default=True)


    sunday_open = models.TimeField(auto_now_add=False)
    sunday_close = models.TimeField(auto_now_add=False)
    sunday_available = models.BooleanField(default=True)
    availability = models.CharField(choices=AVAILABILITY, max_length=100, default="open")
    
    
    liked = models.ManyToManyField("auth_api.User", related_name="participants", blank=True)
    status = models.CharField(choices=STATUS, max_length=100, default="in_review")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Service"

    def __str__(self):
        return f"{self.title}"
    
    def service_image(self):
        return mark_safe('<img src="%s" width="50" height="50" object-fit: cover; />' % (self.image.url))




class Feature(models.Model):
    service_feature = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name="service_feature")
    title = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    sfid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz1231234567890")

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Service Features"

    def __str__(self):
        return f"{self.title}"
    
    
class Gallery(models.Model):
    service_gallery = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name="service_gallery")
    image = models.ImageField(upload_to="auth_api.user_directory_path", default="gallery.jpg")
    title = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    gid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz1231234567890")

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Service Images"

    def __str__(self):
        return f"{self.title}"
    
    def gallery_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))



