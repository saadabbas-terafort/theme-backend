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
from django.core.cache import cache

API_KEY = os.getenv('API_KEY')

MOBILE_THEME_CACHE_KEYS = [
    "mobile_theme_categories",
    "mobile_theme_subcategories",
    "mobile_theme_coolfont",
    "mobile_theme_Keyboardcategory",
    "mobile_theme_keyboardsubcategories",
    "mobile_theme_keyboard",
    "mobile_theme_wallpapercategories",
    "mobile_theme_wallpapersubcategories",
    "mobile_theme_wallpaper",
    "mobile_theme_Categorytheme",
    "mobile_theme_subcategoriestheme",
    "mobile_theme_theme",
    "mobile_theme_diyimage",
    "mobile_theme_diykey",
    "mobile_theme_diyfont",
    "mobile_theme_diyeffect",
    "mobile_theme_diysound",
]

class CheckPointV2(APIView):
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
            if skip < 0 or limit < 1 or limit > 100:
                return Response( {
                    "satus" : 422,
                    "data": None,
                    "massage" : "Skip Con't be nagative or limit must be At least  1 and less then 100 "
                } , status= 422)
            return skip , limit , queryset[skip:skip + limit]
    @staticmethod
    def apply_cache_filter(items, request):
            category_id = request.query_params.get('category_id')
            subcategory_id = request.query_params.get('subcategory_id')
            premium_only = request.query_params.get('premium_only')
    
            if subcategory_id:
                items = [ item for item in items
                if str(item.get("subcategory")) == str(subcategory_id) ]
            elif category_id:
                items = [ item for item in items
                if str(item.get("category")) == str(category_id)
                and item.get("subcategory") is None ]
    
            if premium_only and premium_only.lower()== "true":
                items = [item for item in items
                if item.get("premium") is True ]
            elif premium_only and premium_only.lower()== "false":
                items = [item for item in items
                if item.get("premium") is False ]
            return items
class CategoryListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_categories"
        cached_categories = cache.get(cache_key)
        # print(cached_categories)
        if cached_categories is  None:
            categories = Category.objects.prefetch_related("subcategories").all()
            serializer = CategorySerializer(categories , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Categories retrived Successfully",
                "total":len(paginated_data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)


class ArtworkSubcategoryListViewV2(APIView):
    def get(self , request ,category_id):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_subcategories"
        cached_categories = cache.get(cache_key)
        # print(cached_categories)
        if cached_categories is  None:
            categories = SubCategory.objects.filter(category_id=category_id)
            serializer = SubCategorySerializer(categories , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "SubCategories retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)

class CoolFontListViewV2(APIView):
    def get(self , request ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
    
        cache_key ="mobile_theme_coolfont"
        cached_categories = cache.get(cache_key)
        if cached_categories is  None:
                categories = CoolFont.objects.all()
                serializer = CoolFontSerializer(categories , many=True)
                data = serializer.data
                cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
        data = CheckPointV2.apply_cache_filter(data , request)
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
            "status": 200,
            "data": paginated_data,
            'massage': "CoolFonts retrived Successfully",
            "total":len(paginated_data),
            "skip": skip,
            "limit" : limit ,
                } , status=200)
        
class ArtworkDetailViewV2(APIView):
    def get(self , request ,artwork_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_coolfont_{artwork_id}"
        cached_categories = cache.get(cache_key)
                # print(cached_categories)
        if cached_categories is  None:
            try:
                category = CoolFont.objects.get(id=artwork_id)
            except CoolFont.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "CoolFont not found"
            }, status=404)
            serializer = CoolFontSerializer(category )
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "CoolFont retrived Successfully",              
                    } , status=200)


class KeyboardCategoryListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_Keyboardcategory"
        cached_keyboard = cache.get(cache_key)
        # print(cached_keyboard)
        if cached_keyboard is  None:
            keyboard = Category.objects.filter(type='keyboard')
            serializer = CategorySerializer(keyboard , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_keyboard["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': " Keyboard Categories retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
class KeyboardSubcategoryListViewV2(APIView):
    def get(self , request ,category_id):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_keyboardsubcategories"
        cached_categories = cache.get(cache_key)
        # print(cached_categories)
        if cached_categories is  None:
            categories = SubCategory.objects.filter(category_id=category_id)
            serializer = SubCategorySerializer(categories , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Keyboard SubCategories retrived Successfully",
                "total":len(paginated_data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
        
class KeyboardListViewV2(APIView):
    def get(self , request ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
    
        cache_key ="mobile_theme_keyboard"
        cached_keyboard = cache.get(cache_key)
            # print(cached_categories)
        if cached_keyboard is  None:
                keyboard = Keyboard.objects.all()
                serializer = KeyboardSerializer(keyboard , many=True)
                data = serializer.data
                cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_keyboard["data"]
        data = CheckPointV2.apply_cache_filter(data , request)
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
            "status": 200,
            "data": paginated_data,
            'massage': "Keyboard list retrived Successfully",
            "total":len(paginated_data),
            "skip": skip,
            "limit" : limit ,
                } , status=200)
        
        
class KeyboardDetailViewV2(APIView):
    def get(self , request ,keyboard_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_keyboard_{keyboard_id}"
        cached_keyboard = cache.get(cache_key)
                # print(cached_keyboard)
        if cached_keyboard is  None:
            try:
                keyboard = Keyboard.objects.get(id=keyboard_id)
            except Keyboard.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "CoolFont not found"
            }, status=404)
            serializer = KeyboardSerializer(keyboard)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_keyboard["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Keyboard retrived Successfully",              
                    } , status=200)

class wallpaperCategoryListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_wallpapercategories"
        cached_categories = cache.get(cache_key)
        # print(cached_categories)
        if cached_categories is  None:
            categories = Category.objects.filter(type='wallpaper')
            serializer = CategorySerializer(categories , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Wallpaper Categories retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)

class wallpaperSubcategoryListViewV2(APIView):
    def get(self , request ,category_id):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_wallpapersubcategories"
        cached_categories = cache.get(cache_key)
        # print(cached_categories)
        if cached_categories is  None:
            categories = SubCategory.objects.filter(category_id=category_id)
            serializer = SubCategorySerializer(categories , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_categories["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Wallpaper SubCategories retrived Successfully",
                "total":len(paginated_data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
class WallpaperListViewV2(APIView):
    def get(self , request ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
    
        cache_key ="mobile_theme_wallpaper"
        cached_wallpaper = cache.get(cache_key)
            # print(cached_categories)
        if cached_wallpaper is  None:
                wallpaper = Wallpaper.objects.all()
                serializer = WallpaperSerializer(wallpaper , many=True)
                data = serializer.data
                cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_wallpaper["data"]
        data = CheckPointV2.apply_cache_filter(data , request)
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
            "status": 200,
            "data": paginated_data,
            'massage': "wallpaper List retrived Successfully",
            "total":len(paginated_data),
            "skip": skip,
            "limit" : limit ,
                } , status=200)

class WallpaperDetailViewV2(APIView):
    def get(self , request ,wallpaper_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_wallpaper_{wallpaper_id}"
        cached_wallpaper = cache.get(cache_key)
                # print(cached_keyboard)
        if cached_wallpaper is  None:
            try:
                keyboard = Wallpaper.objects.get(id=wallpaper_id)
            except Wallpaper.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "wallpaperFont not found"
            }, status=404)
            serializer = WallpaperSerializer(keyboard)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_wallpaper["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "wallpaper retrived Successfully",              
                    } , status=200)
    
class ThemeCategoryListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_Categorytheme"
        cached_theme = cache.get(cache_key)
        # print(cached_keyboard)
        if cached_theme is  None:
            theme = Category.objects.filter(type='theme')
            serializer = CategorySerializer(theme , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_theme["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Theme Categories retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
class ThemeSubcategoryListViewV2(APIView):
    def get(self , request ,category_id):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_subcategoriestheme"
        cached_subcategories = cache.get(cache_key)
        # print(cached_categories)
        if cached_subcategories is  None:
            categories = SubCategory.objects.filter(category_id=category_id)
            serializer = SubCategorySerializer(categories , many=True)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_subcategories["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Theme SubCategories retrived Successfully",
                "total":len(paginated_data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
        
class ThemeListViewV2(APIView):
    def get(self , request ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
    
        cache_key ="mobile_theme_theme"
        cached_theme = cache.get(cache_key)
            # print(cached_categories)
        if cached_theme is  None:
                theme = Theme.objects.all()
                serializer = ThemeSerializer(theme , many=True)
                data = serializer.data
                cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_theme["data"]
        data = CheckPointV2.apply_cache_filter(data , request)
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
            "status": 200,
            "data": paginated_data,
            'massage': "Theme List retrived Successfully",
            "total":len(paginated_data),
            "skip": skip,
            "limit" : limit ,
                } , status=200)
        
class ThemeDetailViewV2(APIView):
    def get(self , request ,theme_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_theme_{theme_id}"
        cached_theme = cache.get(cache_key)
                # print(cached_keyboard)
        if cached_theme is  None:
            try:
                keyboard = Theme.objects.get(id=theme_id)
            except Theme.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "Theme not found"
            }, status=404)
            serializer = ThemeSerializer(keyboard)
            data = serializer.data
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_theme["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Theme retrived Successfully",              
                    } , status=200)
        
        
class DiyImageListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_diyimage"
        cached_diyimage = cache.get(cache_key)
        if cached_diyimage is  None:
            diy_images = DiyImage.objects.all()
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

            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diyimage["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Diy Images list retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)

class DiyImageDetailViewV2(APIView):
    def get(self , request ,image_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_diyimage_{image_id}"
        cached_diyimage = cache.get(cache_key)
        if cached_diyimage is  None:
            try:
                diy_image = DiyImage.objects.get(id=image_id)
            except DiyImage.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "Diy Image not found"
            }, status=404)
            data = {
                            "id": diy_image.id,
                            "name": diy_image.name,
                            "image_url": diy_image.image_url,
                            "description": diy_image.description,
                            "transparent": diy_image.transparent,
                            "priority": diy_image.priority,
                            "created_at": diy_image.created_at
                                    }
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diyimage["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Diy Image retrived Successfully",              
                    } , status=200)

class DiyKeyListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_diykey"
        cached_diykey = cache.get(cache_key)
        if cached_diykey is  None:
            diy_keys = DiyKey.objects.all()
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

            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diykey["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Diy Keys List retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
class DiyKeyDetailViewV2(APIView):
    def get(self , request ,key_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_diykey_{key_id}"
        cached_diykey = cache.get(cache_key)
        if cached_diykey is  None:
            try:
                diy_key = DiyKey.objects.get(id=key_id)
            except DiyKey.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "Diy Key not found"
            }, status=404)
            data = {
                            "id": diy_key.id,
                            "name": diy_key.name,
                            "image_url": diy_key.image_url,
                            "description": diy_key.description,
                            "transparent": diy_key.transparent,
                            "priority": diy_key.priority,
                            "created_at": diy_key.created_at
                                    }
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diykey["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Diy Key retrived Successfully",              
                    } , status=200)
    
class DiyFontListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_diyfont"
        cached_diyfont = cache.get(cache_key)
        if cached_diyfont is  None:
            diy_fonts = DiyFont.objects.all()
            data = []
                    
            for diy_font in diy_fonts:
                data.append({
                "id": diy_font.id,
                "name": diy_font.name,
                "font_file": diy_font.font_file,
                "priority": diy_font.priority,
                "created_at": diy_font.created_at
            })

            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diyfont["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Diy Font List retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
class DiyFontDetailViewV2(APIView):
    def get(self , request ,font_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_diyfont_{font_id}"
        cached_diyfont = cache.get(cache_key)
        if cached_diyfont is  None:
            try:
                diy_font = DiyFont.objects.get(id=font_id)
            except DiyFont.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "Diy Font not found"
            }, status=404)
            data = {
                            "id": diy_font.id,
                            "name": diy_font.name,
                            "font_file": diy_font.font_file,
                            "priority": diy_font.priority,
                            "created_at": diy_font.created_at
                                    }
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diyfont["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Diy Font retrived Successfully",              
                    } , status=200)
        
class DiyEffectListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_diyeffect"
        cached_diyeffect = cache.get(cache_key)
        if cached_diyeffect is  None:
            diy_effects = DiyEffect.objects.all()
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

            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diyeffect["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Diy Effect List retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)
        
class DiyEffectDetailViewV2(APIView):
    def get(self , request ,effect_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_diyeffect_{effect_id}"
        cached_diyeffect = cache.get(cache_key)
        if cached_diyeffect is  None:
            try:
                diy_effect = DiyEffect.objects.get(id=effect_id)
            except DiyEffect.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "Diy Effect not found"
            }, status=404)
            data ={
            "id": diy_effect.id,
            "name": diy_effect.name,
            "gif_url": diy_effect.gif_url,
            "preview_url": diy_effect.preview_url,
            "priority": diy_effect.priority,
            "created_at": diy_effect.created_at
        }
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diyeffect["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Diy Effect retrived Successfully",              
                    } , status=200)
class DiySoundListViewV2(APIView):
    def get(self , request):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check

        cache_key ="mobile_theme_diysound"
        cached_diysound = cache.get(cache_key)
        if cached_diysound is  None:
            diy_sounds = DiySound.objects.all()
            data = []      
            for diy_sound in diy_sounds:
                data.append({
                    "id": diy_sound.id,
                    "name": diy_sound.name,
                    "sound_file" : diy_sound.sound_file,
                    "preview_url": diy_sound.preview_url,
                    "priority": diy_sound.priority,
                    "created_at": diy_sound.created_at,
                })
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diysound["data"]
        pagination = CheckPointV2.apply_pagination(data , request)
        if isinstance(pagination , Response):
            return pagination
        skip , limit ,paginated_data = pagination
        return Response({
                "status": 200,
                "data": paginated_data,
                'massage': "Diy Sound List retrived Successfully",
                "total":len(data),
                "skip": skip,
                "limit" : limit ,
            } , status=200)

class DiySoundDetailViewV2(APIView):
    def get(self , request ,sound_id ):
        if api_key_check :=CheckPointV2.check_api_key(request):
            return api_key_check
        
        cache_key =f"mobile_theme_diysound_{sound_id}"
        cached_diysound = cache.get(cache_key)
        if cached_diysound is  None:
            try:
                diy_sound = DiySound.objects.get(id=sound_id)
            except DiySound.DoesNotExist:
                return Response({
                "status": 404,
                "data": None,
                "message": "Diy Sound not found"
            }, status=404)
            data = {
            "id": diy_sound.id,
            "name": diy_sound.name,
            "sound_file" : diy_sound.sound_file,
            "preview_url": diy_sound.preview_url,
            "priority": diy_sound.priority,
            "created_at": diy_sound.created_at,
            
        }
            cache.set(cache_key , {"data": data} , timeout=300)
        else:
            data = cached_diysound["data"]
    
        return Response({
                "status": 200,
                "data": data,
                'massage': "Diy Sound retrived Successfully",              
                    } , status=200)
        
        
class CacheInfoView(APIView):

    def get(self, request):
        if api_key_check := CheckPointV2.check_api_key(request):
            return api_key_check

        cache_entries = []

        for key in MOBILE_THEME_CACHE_KEYS:
            cached_data = cache.get(key)
            if cached_data is None:
                continue

            items = cached_data.get("data", []) if isinstance(cached_data, dict) else cached_data
            cache_entries.append({
                "cache_key": key,
                "total_items": len(items) if hasattr(items, "__len__") else None,
                "data": items,
            })

        if not cache_entries:
            return Response({
                "status": 404,
                "data": [],
                "message": "No mobile theme cache data found. Call the v2 APIs first to create cache."
            }, status=404)

        return Response({
            "status": 200,
            "data": cache_entries,
            "message": "Cache information retrieved successfully"
        })
