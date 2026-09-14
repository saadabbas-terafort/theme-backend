from rest_framework.views import APIView
from rest_framework.response import Response
import os
from .models import (
    Category, SubCategory, Keyboard, Wallpaper, Theme, ThemeIcon,
    DiyImage, DiyKey, DiyFont, DiyEffect, DiySound,
)
from catalog.models import CoolFont
from .serializers import (
    CategorySerializer, SubCategorySerializer, CoolFontSerializer,
    KeyboardSerializer, WallpaperSerializer, ThemeSerializer, 
)
API_KEY = os.getenv('API_KEY')  

class CheckPoint(APIView):
    
    @staticmethod
    def check_api_key(request):
        if request.headers.get('api-key') != API_KEY:
            return Response({
            "status": 403,
            "data": None,
            "message": "Missing or invalid api-key"
        }, status=403)
        return None

    @staticmethod
    def apply_list_filter(items, request):
        category_id = request.query_params.get('category_id')
        subcategory_id = request.query_params.get('subcategory_id')
        premium_only = request.query_params.get('premium_only')

        if subcategory_id:
            items = items.filter(subcategory_id=subcategory_id)
        elif category_id:
            items = items.filter(category_id=category_id, subcategory_id__isnull=True)

        if premium_only and premium_only.lower()== 'true':
            items = items.filter(premium=True)
        elif premium_only and premium_only.lower()== 'false':
            items = items.filter(premium=False)
        return items
    @staticmethod
    def apply_pagination(queryset , request):
        try:
            skip = int(request.query_params.get("skip",0))
            limit = int(request.query_params.get("limit",100))
        except ValueError:
            return Response({
                "status" : 422,
                "data" : None,
                "massage" : "skip and Limt Must be valid integer"
            } ,status=422)
        if skip < 0 or limit < 1:
            return Response( {
                "satus" : 422,
                "data": None,
                "massage" : "Skip Con't be nagative or limit must be At least  1 "
            } , status= 422)
        return queryset[skip:skip + limit]


class CategoryListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        categories = Category.objects.all()
        categories = CheckPoint.apply_pagination(categories , request)
        if isinstance(categories, Response):
            print("Pagination Response:", categories.data)
            return categories
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Categories retrieved successfully"
        }, status=200)
        
class ArtworkSubcategoryListView(APIView):
    def get(self, request, category_id):
        if api_key_check := CheckPoint.check_api_key(request):
                return api_key_check

        subcategories = SubCategory.objects.filter(category_id=category_id)
        subcategories = CheckPoint.apply_pagination(subcategories , request)
        if isinstance(subcategories, Response):
            print("Pagination Response:", subcategories.data)
            return subcategories
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Subcategories retrieved successfully"
        }, status=200)
        
        
class CoolFontListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        fonts = CoolFont.objects.all()
        fonts = CheckPoint.apply_list_filter(fonts, request)
        serializer = CoolFontSerializer(fonts, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Cool fonts retrieved successfully"
        }, status=200)
        
        
class ArtworkDetailView(APIView):
    def get(self, request, artwork_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        try:
            artwork = CoolFont.objects.get(id=artwork_id)
        except CoolFont.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "Artwork not found"
            }, status=404)

        serializer = CoolFontSerializer(artwork)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Artwork retrieved successfully"
        }, status=200)
        
        
class KeyboardCategoryListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        categories = Category.objects.filter(type='keyboard')
        categories = CheckPoint.apply_pagination(categories , request)
        if isinstance(categories, Response):
            print("Pagination Response:", categories.data)
            return categories
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Keyboard categories retrieved successfully"
        }, status=200)
        
class KeyboardSubcategoryListView(APIView):
    def get(self, request, category_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        subcategories = SubCategory.objects.filter(category_id=category_id)
        subcategories = CheckPoint.apply_pagination(subcategories , request)
        if isinstance(subcategories, Response):
            print("Pagination Response:", subcategories.data)
            return subcategories
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Keyboard subcategories retrieved successfully"
        }, status=200)
        
        
class KeyboardListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        keyboards = Keyboard.objects.all()
        keyboards = CheckPoint.apply_list_filter(keyboards, request)
        keyboards = CheckPoint.apply_pagination(keyboards , request)
        if isinstance(keyboards, Response):
            print("Pagination Response:", keyboards.data)
            return keyboards
        serializer = KeyboardSerializer(keyboards, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Keyboards retrieved successfully"
        }, status=200)
        
class KeyboardDetailView(APIView):
    def get(self, request, keyboard_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        try:
            keyboard = Keyboard.objects.get(id=keyboard_id)
        except Keyboard.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "Keyboard not found"
            }, status=404)

        serializer = KeyboardSerializer(keyboard)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Keyboard retrieved successfully"
        }, status=200)
        
        
class wallpaperCategoryListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        categories = Category.objects.filter(type='wallpaper')
        categories = CheckPoint.apply_pagination(categories , request)
        if isinstance(categories, Response):
            print("Pagination Response:", categories.data)
            return categories
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Wallpaper categories retrieved successfully"
        }, status=200)
        
        
class wallpaperSubcategoryListView(APIView):
    def get(self, request, category_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check


        subcategories = SubCategory.objects.filter(category_id=category_id)
        subcategories = CheckPoint.apply_pagination(subcategories , request)
        if isinstance(subcategories, Response):
            print("Pagination Response:", subcategories.data)
            return subcategories
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Wallpaper subcategories retrieved successfully"
        }, status=200)
        
        
        
class WallpaperListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        wallpapers = Wallpaper.objects.all()
        wallpapers = CheckPoint.apply_list_filter(wallpapers, request)
        wallpapers = CheckPoint.apply_pagination(wallpapers , request)
        if isinstance(wallpapers, Response):
            print("Pagination Response:", wallpapers.data)
            return wallpapers

        serializer = WallpaperSerializer(wallpapers, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Wallpapers retrieved successfully"
        }, status=200)
        
class WallpaperDetailView(APIView):
    def get(self, request, wallpaper_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        try:
            wallpaper = Wallpaper.objects.get(id=wallpaper_id)
        except Wallpaper.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "Wallpaper not found"
            }, status=404)

        serializer = WallpaperSerializer(wallpaper)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Wallpaper retrieved successfully"
        }, status=200)
        
        
class ThemeCategoryListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        categories = Category.objects.filter(type='theme')
        categories = CheckPoint.apply_pagination(categories , request)
        if isinstance(categories, Response):
            print("Pagination Response:", categories.data)
            return categories
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Theme categories retrieved successfully"
        }, status=200)
        
class ThemeSubcategoryListView(APIView):
    def get(self, request, category_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        subcategories = SubCategory.objects.filter(category_id=category_id)
        subcategories = CheckPoint.apply_pagination(subcategories , request)
        if isinstance(subcategories, Response):
            print("Pagination Response:", subcategories.data)
            return subcategories
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Theme subcategories retrieved successfully"
        }, status=200)
        
class ThemeListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        themes = Theme.objects.all()
        themes = CheckPoint.apply_list_filter(themes, request)
        themes = CheckPoint.apply_pagination(themes , request)
        if isinstance(themes, Response):
            print("Pagination Response:", themes.data)
            return themes
        serializer = ThemeSerializer(themes, many=True)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Themes retrieved successfully"
        }, status=200)
        
class ThemeDetailView(APIView):
    def get(self, request, theme_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        try:
            theme = Theme.objects.get(id=theme_id)
        except Theme.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "Theme not found"
            }, status=404)

        serializer = ThemeSerializer(theme)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Theme retrieved successfully"
        }, status=200)
        
        
        
class DiyImageListView(APIView):
    def get(self, request ):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        diy_images = DiyImage.objects.all()
        diy_images = CheckPoint.apply_pagination(diy_images , request)
        if isinstance(diy_images, Response):
            print("Pagination Response:", diy_images.data)
            return diy_images
        data = []
        
        for diy_image in diy_images:
            
            data.append({
                "id": diy_image.id,
                "name": diy_image.name,
                "image_url": diy_image.image_url,
                "description": diy_image.description,
                "transparent": diy_image.transparent,
                "priority": diy_image.priority,
                "created_at": diy_image.created_at
            })
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY images retrieved successfully"
        }, status=200)
        

class DiyImageDetailView(APIView):
    def get(self, request, image_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        try:
            diy_image = DiyImage.objects.get(id=image_id)
        except DiyImage.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "DIY image not found"
            }, status=404)

        data ={
            "id": diy_image.id,
            "name": diy_image.name,
            "image_url": diy_image.image_url,
            "description": diy_image.description,
            "transparent": diy_image.transparent,
            "priority": diy_image.priority,
            "created_at": diy_image.created_at
        }
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY image retrieved successfully"
        }, status=200)
        
class DiyKeyListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        diy_keys = DiyKey.objects.all()
        diy_keys = CheckPoint.apply_pagination(diy_keys , request)
        if isinstance(diy_keys, Response):
            print("Pagination Response:", diy_keys.data)
            return diy_keys
        data = []
        
        for diy_key in diy_keys:
            data.append({
                "id": diy_key.id,
                "name": diy_key.name,
                "image_url": diy_key.image_url,
                "description": diy_key.description,
                "transparent": diy_key.transparent,
                "special_key_bg": diy_key.special_key_bg,
                "priority": diy_key.priority,
                "created_at": diy_key.created_at
            })
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY keys retrieved successfully"
        }, status=200)
        
class DiyKeyDetailView(APIView):
    def get(self, request, key_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        try:
            diy_key = DiyKey.objects.get(id=key_id)
        except DiyKey.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "DIY key not found"
            }, status=404)

        data ={
            "id": diy_key.id,
            "name": diy_key.name,
            "image_url": diy_key.image_url,
            "description": diy_key.description,
            "transparent": diy_key.transparent,
            "special_key_bg": diy_key.special_key_bg,
            "priority": diy_key.priority,
            "created_at": diy_key.created_at
        }
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY key retrieved successfully"
        }, status=200)
        
class DiyFontListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        diy_fonts = DiyFont.objects.all()
        diy_fonts = CheckPoint.apply_pagination(diy_fonts , request)
        if isinstance(diy_fonts, Response):
            print("Pagination Response:", diy_fonts.data)
            return diy_fonts
        data = []
        
        for diy_font in diy_fonts:
            data.append({
                "id": diy_font.id,
                "name": diy_font.name,
                "font_file": diy_font.font_file,
                "priority": diy_font.priority,
                "created_at": diy_font.created_at
            })
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY fonts retrieved successfully"
        }, status=200)


class DiyFontDetailView(APIView):
    def get(self, request, font_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        try:
            diy_font = DiyFont.objects.get(id=font_id)
        except DiyFont.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "DIY font not found"
            }, status=404)

        data ={
            "id": diy_font.id,
            "name": diy_font.name,
            "font_file": diy_font.font_file,
            "priority": diy_font.priority,
            "created_at": diy_font.created_at
        }
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY font retrieved successfully"
        }, status=200)
    
class DiyEffectListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check

        diy_effects = DiyEffect.objects.all()
        diy_effects = CheckPoint.apply_pagination(diy_effects , request)
        if isinstance(diy_effects, Response):
            print("Pagination Response:", diy_effects.data)
            return diy_effects
        data = []
        
        for diy_effect in diy_effects:
            data.append({
                "id": diy_effect.id,
                "name": diy_effect.name,
                "gif_url": diy_effect.gif_url,
                "preview_url": diy_effect.preview_url,
                "priority": diy_effect.priority,
                "created_at": diy_effect.created_at
            })
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY effects retrieved successfully"
        }, status=200)
    
class DiyEffectDetailView(APIView):
    def get(self, request, effect_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        try:
            diy_effect = DiyEffect.objects.get(id=effect_id)
        except DiyEffect.DoesNotExist:
            return Response({
                "status": 404,
                "data": None,
                "message": "DIY effect not found"
            }, status=404)

        data ={
            "id": diy_effect.id,
            "name": diy_effect.name,
            "gif_url": diy_effect.gif_url,
            "preview_url": diy_effect.preview_url,
            "priority": diy_effect.priority,
            "created_at": diy_effect.created_at
        }
        return Response({
            "status": 200,
            "data": data,
            "message": "DIY effect retrieved successfully"
        }, status=200)
        
class DiySoundListView(APIView):
    def get(self, request):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        
        
        
        diy_sound = DiySound.objects.all()
        diy_sound = CheckPoint.apply_pagination(diy_sound , request)
        if isinstance(diy_sound, Response):
            print("Pagination Response:", diy_sound.data)
            return diy_sound
        print(diy_sound)            

        data = []
        
        for diy_sounds in diy_sound:
            data.append({
                    "id": diy_sounds.id,
                    "name": diy_sounds.name,
                    "sound_file" : diy_sounds.sound_file,
                    "preview_url": diy_sounds.preview_url,
                    "priority": diy_sounds.priority,
                    "created_at": diy_sounds.created_at,
    })

        return Response(data)
    
    
class DiySoundDetailView(APIView):
    def get(self, request , sound_id):
        if api_key_check := CheckPoint.check_api_key(request):
            return api_key_check
        try:
            diy_sound = DiySound.objects.get(id=sound_id)
        except DiySound.DoesNotExist:
            return Response({
                        "status" : 404,
                        "data" : None,
                        "massege" : "Sound Not Found"
                        
                } , status=404)
        data = {
            "id": diy_sound.id,
            "name": diy_sound.name,
            "sound_file" : diy_sound.sound_file,
            "preview_url": diy_sound.preview_url,
            "priority": diy_sound.priority,
            "created_at": diy_sound.created_at,
            
        }
        return Response({
            "status" : 200,
            "data" : data,
            "massage" : "DIY Sound retrieved successfully"
        } , status=200)
        
        
