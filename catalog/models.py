from django.db import models
import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    type = models.CharField(
    max_length=20,
    choices=[
        ('coolfont', 'Cool Font'),
        ('keyboard', 'Keyboard'),
        ('wallpaper', 'Wallpaper'),
        ('theme', 'Theme'),
    ]
    )   
    thumbnail = models.URLField(blank=True, null=True)    
    priority = models.IntegerField(default=0)
        
    def __str__(self):
            return self.name

class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    thumbnail = models.URLField(blank=True, null=True)    
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class CoolFont(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='coolfonts')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='coolfonts', null=True, blank=True)
    premium = models.BooleanField(default=False)
    content = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)    
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
class Keyboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='keyboards')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='keyboards' , null=True, blank=True)
    premium = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_url = models.URLField(blank=True, null=True)
    text_color = models.CharField(max_length=9, default='#FFFFFFFF')  # Default to white
    key_alpha = models.FloatField(default=0.85)  # Default to 0.85
    keyboard_bg = models.URLField()
    normal_key_bg = models.URLField()
    specialty_keys_bg = models.URLField()
    backspace_key_bg = models.URLField(blank=True, null=True)
    uppercase_letter_bg = models.URLField(blank=True, null=True)
    number_button_bg = models.URLField(blank=True, null=True)
    emoji_button_bg = models.URLField(blank=True, null=True)
    comma_button_bg = models.URLField(blank=True, null=True)
    enter_button_bg = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return self.name

class Wallpaper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='wallpapers')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='wallpapers' , null=True, blank=True)
    premium = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_url = models.URLField(blank=True, null=True)
    image_url = models.URLField()

    def __str__(self):
        return self.name
    
class Theme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='themes')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='themes' , null=True, blank=True)
    premium = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_url = models.URLField(blank=True, null=True)
    keyboard = models.ForeignKey(Keyboard, on_delete=models.SET_NULL, related_name='themes', null=True, blank=True)
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.SET_NULL, related_name='themes', null=True, blank=True)

    def __str__(self):
        return self.name
    
class ThemeIcon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme_icons')
    name = models.CharField(max_length=256)
    preview_url = models.URLField(blank=True, null=True)
    icon_image = models.URLField()
    alias_id = models.CharField(max_length=256)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class DiyImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    image_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    transparent = models.FloatField(default=0.85)  # Default to 0.85
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class DiyKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    image_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    transparent = models.FloatField(default=0.9)  # Default to 0.85
    special_key_bg = models.URLField()
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class DiyFont(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    font_file = models.URLField()
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class DiyEffect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    gif_url = models.URLField()
    preview_url = models.URLField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class DiySound(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    sound_file = models.URLField()
    preview_url = models.URLField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    