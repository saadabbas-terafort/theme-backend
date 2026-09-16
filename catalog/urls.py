from django.urls import path
from . import views
from . import views_v2
from .views_v2 import CacheInfoView

urlpatterns = [
    # ==================== ARTWORK (Cool Fonts) ====================
    path('api/public/mobile-theme/artwork/categories', views.CategoryListView.as_view(), name='artwork_categories'),
    path('api/public/mobile-theme/artwork/categories/<uuid:category_id>/subcategories', views.ArtworkSubcategoryListView.as_view(), name='artwork_subcategories'),
    path('api/public/mobile-theme/artwork', views.CoolFontListView.as_view(), name='artwork_list'),
    path('api/public/mobile-theme/artwork/<uuid:artwork_id>', views.ArtworkDetailView.as_view(), name='artwork_detail'),
    
    # ==================== KEYBOARD ====================
    path('api/public/mobile-theme/keyboard/categories', views.KeyboardCategoryListView.as_view(), name='keyboard_categories'),
    path('api/public/mobile-theme/keyboard/categories/<uuid:category_id>/subcategories', views.KeyboardSubcategoryListView.as_view(), name='keyboard_subcategories'),
    path('api/public/mobile-theme/keyboard', views.KeyboardListView.as_view(), name='keyboard_list'),
    path('api/public/mobile-theme/keyboard/<uuid:keyboard_id>', views.KeyboardDetailView.as_view(), name='keyboard_detail'),
    
    # ==================== WALLPAPER ====================
    path('api/public/mobile-theme/wallpaper/categories', views.wallpaperCategoryListView.as_view(), name='wallpaper_categories'),
    path('api/public/mobile-theme/wallpaper/categories/<uuid:category_id>/subcategories', views.wallpaperSubcategoryListView.as_view(), name='wallpaper_subcategories'),
    path('api/public/mobile-theme/wallpaper', views.WallpaperListView.as_view(), name='wallpaper_list'),
    path('api/public/mobile-theme/wallpaper/<uuid:wallpaper_id>', views.WallpaperDetailView.as_view(), name='wallpaper_detail'),
    
    
    # ==================== THEME ====================
    path('api/public/mobile-theme/theme/categories', views.ThemeCategoryListView.as_view(), name='theme_categories'),
    path('api/public/mobile-theme/theme/categories/<uuid:category_id>/subcategories', views.ThemeSubcategoryListView.as_view(), name='theme_subcategories'),
    path('api/public/mobile-theme/theme', views.ThemeListView.as_view(), name='theme_list'),
    path('api/public/mobile-theme/theme/<uuid:theme_id>', views.ThemeDetailView.as_view(), name='theme_detail'),
    # ==================== THEME Icons ====================
    
    
    
    # ==================== DIY CUSTOM KEYBOARD ====================
    path('api/public/mobile-theme/diy/images', views.DiyImageListView.as_view(), name='diy_images_list'),
    path('api/public/mobile-theme/diy/images/<uuid:image_id>', views.DiyImageDetailView.as_view(), name='diy_images_detail'),
    
    path('api/public/mobile-theme/diy/keys', views.DiyKeyListView.as_view(), name='diy_keys_list'),
    path('api/public/mobile-theme/diy/keys/<uuid:key_id>', views.DiyKeyDetailView.as_view(), name='diy_keys_detail'),
    
    path('api/public/mobile-theme/diy/fonts', views.DiyFontListView.as_view(), name='diy_fonts_list'),
    path('api/public/mobile-theme/diy/fonts/<uuid:font_id>', views.DiyFontDetailView.as_view(), name='diy_fonts_detail'),
    
    path('api/public/mobile-theme/diy/effects', views.DiyEffectListView.as_view(), name='diy_effects_list'),
    path('api/public/mobile-theme/diy/effects/<uuid:effect_id>', views.DiyEffectDetailView.as_view(), name='diy_effects_detail'),
    
    path('api/public/mobile-theme/diy/sounds', views.DiySoundListView.as_view(), name='diy_sounds_list'),
    path('api/public/mobile-theme/diy/sounds/<uuid:sound_id>', views.DiySoundDetailView.as_view(), name='diy_sounds_detail'),
    
    
    
    #*****************************************************With Caching ****************************************************************#
    
    # ==================== ARTWORK (Cool Fonts) ====================
        path('api/public/mobile-theme/artwork/categories/v2', views_v2.CategoryListViewV2.as_view(), name='artwork_categories_v2'),
        path('api/public/mobile-theme/artwork/categories/<uuid:category_id>/subcategories/v2', views_v2.ArtworkSubcategoryListViewV2.as_view(), name='artwork_subcategories_v2'),
        path('api/public/mobile-theme/artwork/v2', views_v2.CoolFontListViewV2.as_view(), name='artwork_list_v2'),
        path('api/public/mobile-theme/artwork/<uuid:artwork_id>/v2', views_v2.ArtworkDetailViewV2.as_view(), name='artwork_detail_v2'),
        
        # ==================== KEYBOARD ====================
        path('api/public/mobile-theme/keyboard/categories/v2', views_v2.KeyboardCategoryListViewV2.as_view(), name='keyboard_categories_v2'),
        path('api/public/mobile-theme/keyboard/categories/<uuid:category_id>/subcategories/v2', views_v2.KeyboardSubcategoryListViewV2.as_view(), name='keyboard_subcategories_v2'),
        path('api/public/mobile-theme/keyboard/v2', views_v2.KeyboardListViewV2.as_view(), name='keyboard_list_v2'),
        path('api/public/mobile-theme/keyboard/<uuid:keyboard_id>/v2', views_v2.KeyboardDetailViewV2.as_view(), name='keyboard_detail_v2'),
        
        # ==================== WALLPAPER ====================
        path('api/public/mobile-theme/wallpaper/categories/v2', views_v2.wallpaperCategoryListViewV2.as_view(), name='wallpaper_categories_v2'),
        path('api/public/mobile-theme/wallpaper/categories/<uuid:category_id>/subcategories/v2', views_v2.wallpaperSubcategoryListViewV2.as_view(), name='wallpaper_subcategories_v2'),
        path('api/public/mobile-theme/wallpaper/v2', views_v2.WallpaperListViewV2.as_view(), name='wallpaper_list_v2'),
        path('api/public/mobile-theme/wallpaper/<uuid:wallpaper_id>/v2', views_v2.WallpaperDetailViewV2.as_view(), name='wallpaper_detail_v2'),
        
        
        # ==================== THEME ====================
        path('api/public/mobile-theme/theme/categories/v2', views_v2.ThemeCategoryListViewV2.as_view(), name='theme_categories_v2'),
        path('api/public/mobile-theme/theme/categories/<uuid:category_id>/subcategories/v2', views_v2.ThemeSubcategoryListViewV2.as_view(), name='theme_subcategories_v2'),
        path('api/public/mobile-theme/theme/v2', views_v2.ThemeListViewV2.as_view(), name='theme_list_v2'),
        path('api/public/mobile-theme/theme/<uuid:theme_id>/v2', views_v2.ThemeDetailViewV2.as_view(), name='theme_detail_v2'),
        # ==================== THEME Icons ====================
        
        
        
        # ==================== DIY CUSTOM KEYBOARD ====================
        path('api/public/mobile-theme/diy/images/v2', views_v2.DiyImageListViewV2.as_view(), name='diy_images_list_v2'),
        path('api/public/mobile-theme/diy/images/<uuid:image_id>/v2', views_v2.DiyImageDetailViewV2.as_view(), name='diy_images_detail_v2'),
        
        path('api/public/mobile-theme/diy/keys/v2', views_v2.DiyKeyListViewV2.as_view(), name='diy_keys_list_v2'),
        path('api/public/mobile-theme/diy/keys/<uuid:key_id>/v2', views_v2.DiyKeyDetailViewV2.as_view(), name='diy_keys_detail_v2'),
        
        path('api/public/mobile-theme/diy/fonts/v2', views_v2.DiyFontListViewV2.as_view(), name='diy_fonts_list_v2'),
        path('api/public/mobile-theme/diy/fonts/<uuid:font_id>/v2', views_v2.DiyFontDetailViewV2.as_view(), name='diy_fonts_detail_v2'),
        
        path('api/public/mobile-theme/diy/effects/v2', views_v2.DiyEffectListViewV2.as_view(), name='diy_effects_list_v2'),
        path('api/public/mobile-theme/diy/effects/<uuid:effect_id>/v2', views_v2.DiyEffectDetailViewV2.as_view(), name='diy_effects_detail'),
        
        path('api/public/mobile-theme/diy/sounds/v2', views_v2.DiySoundListViewV2.as_view(), name='diy_sounds_list_v2'),
        path('api/public/mobile-theme/diy/sounds/<uuid:sound_id>/v2', views_v2.DiySoundDetailViewV2.as_view(), name='diy_sounds_detail_v2'),
        path("cache-info/", CacheInfoView.as_view()),

]
