from django.db import models
from django.contrib.auth.models import User, Group

class User_Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  phone_number = models.TextField(max_length=10)
  profile_img = models.ImageField(upload_to="User_profiles", default="man.png")

  def __str__(self):
    return self.user.username

class Category(models.Model):
  title = models.TextField(max_length=20)
  tag = models.TextField(max_length=20)
  category_img = models.ImageField(upload_to="Category_images", default="cereal.png")

  class Meta:
    ordering = ('title', )
    verbose_name_plural = "Categories"

  def __str__(self):
    return self.title

class Brand(models.Model):
  name = models.TextField(max_length=20)

  def __str__(self):
    return self.name

class Item(models.Model):
  category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
  brand = models.ForeignKey(Brand, related_name="items",  on_delete=models.CASCADE)
  name = models.TextField(max_length=30, null=False)
  tag = models.TextField(max_length=10, null=False)
  quantity = models.IntegerField(default=0)
  price = models.FloatField(default=0.00)
  item_img = models.ImageField(upload_to="Item_images", default="no-pictures.png")

  def __str__(self):
    return self.name
