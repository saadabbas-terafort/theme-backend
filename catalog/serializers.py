from rest_framework import serializers
from .models import Category, DiyEffect, DiyFont, DiyImage,  DiyKey,  DiySound, Keyboard, SubCategory, Theme,   Wallpaper  
from .models import ThemeIcon
from catalog.models import CoolFont

class CategorySerializer(serializers.ModelSerializer):
    has_subcategory = serializers.SerializerMethodField()
    class Meta:   
        model = Category
        fields = ['id', 'name', 'type', 'thumbnail' ,'priority' , 'has_subcategory'] 
    
    def get_has_subcategory(self, obj):
        return obj.subcategories.exists()

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  SubCategory
        fields = ['id', 'name', 'category', 'thumbnail' ,'priority' ]
        
class CoolFontSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoolFont
        fields = ['id', 'name', 'category', 'subcategory', 'premium', 'content', 'thumbnail', 'priority', 'created_at']   
class KeyboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyboard
        fields = ['id', 'name', 'category', 'subcategory','premium',  
                'priority' ,'created_at' , 'preview_url' , 'text_color' , 
                'key_alpha' , 'keyboard_bg' , 'normal_key_bg' , 
                'specialty_keys_bg' , 'backspace_key_bg' , 'uppercase_letter_bg' , 
                'number_button_bg' , 'emoji_button_bg' , 'comma_button_bg' ,
                'enter_button_bg' ]
class WallpaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallpaper
        fields = ['id', 'name', 'category', 'subcategory', 'premium', 
                'priority', 'created_at', 'preview_url', 'image_url']


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name', 'category', 'subcategory', 'premium', 
                'priority', 'created_at', 'preview_url', 'keyboard', 'wallpaper']
        
class ThemeIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeIcon
        fields = ['id', 'name', 'theme', 'preview_url' ,
                'icon_image', 'alias_id',
                'priority', 'created_at']
        
        
# class DiyImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiyImage
#         fields = ['id', 'name', 'image_url',
#                 'description', 'transparent',
#                 'priority', 'created_at']


# class DiyKeySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiyKey
#         fields = ['id', 'name', 'image_url', 
#                 'description', 'transparent', 'special_key_bg',
#                 'priority', 'created_at']
        
        
# class DiyFontSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiyFont
#         fields = ['id', 'name', 'font_file', 
#                 'priority', 'created_at']
        
# class DiyEffectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiyEffect
#         fields = ['id', 'name', 'gif_url', 
#                 'preview_url', 'priority', 'created_at']
        
        
# class DiySoundSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiySound
#         fields = ['id', 'name', 'sound_file', 
#                 'preview_url', 'priority', 'created_at']