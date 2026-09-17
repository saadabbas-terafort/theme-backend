from django.core.cache import cache

from .models import (
    Category,
    CoolFont,
    DiyEffect,
    DiyFont,
    DiyImage,
    DiyKey,
    DiySound,
    Keyboard,
    SubCategory,
    Theme,
    ThemeIcon,
    Wallpaper,
)


MODEL_LIST_CACHE_KEYS = {
    Category: (
        "mobile_theme_categories",
        "mobile_theme_Keyboardcategory",
        "mobile_theme_wallpapercategories",
        "mobile_theme_Categorytheme",
    ),
    SubCategory: (
        "mobile_theme_categories",
        "mobile_theme_subcategories",
        "mobile_theme_keyboardsubcategories",
        "mobile_theme_wallpapersubcategories",
        "mobile_theme_subcategoriestheme",
    ),
    CoolFont: ("mobile_theme_coolfont",),
    Keyboard: ("mobile_theme_keyboard",),
    Wallpaper: ("mobile_theme_wallpaper",),
    Theme: ("mobile_theme_theme",),
    DiyImage: ("mobile_theme_diyimage",),
    DiyKey: ("mobile_theme_diykey",),
    DiyFont: ("mobile_theme_diyfont",),
    DiyEffect: ("mobile_theme_diyeffect",),
    DiySound: ("mobile_theme_diysound",),
    ThemeIcon: ("mobile_theme_theme",),
}

MODEL_DETAIL_CACHE_PREFIXES = {
    CoolFont: "mobile_theme_coolfont",
    Keyboard: "mobile_theme_keyboard",
    Wallpaper: "mobile_theme_wallpaper",
    Theme: "mobile_theme_theme",
    DiyImage: "mobile_theme_diyimage",
    DiyKey: "mobile_theme_diykey",
    DiyFont: "mobile_theme_diyfont",
    DiyEffect: "mobile_theme_diyeffect",
    DiySound: "mobile_theme_diysound",
}


def cache_exists(key):
    return cache.get(key) is not None


def delete_existing_cache_keys(keys):
    existing_keys = [key for key in set(keys) if cache_exists(key)]
    if existing_keys:
        cache.delete_many(existing_keys)


def extend_related_content_cache_keys(instance, keys):
    related_objects = []

    if isinstance(instance, Category):
        related_objects.extend(instance.coolfonts.all())
        related_objects.extend(instance.keyboards.all())
        related_objects.extend(instance.wallpapers.all())
        related_objects.extend(instance.themes.all())
        related_objects.extend(ThemeIcon.objects.filter(theme__category=instance))

    if isinstance(instance, SubCategory):
        related_objects.extend(instance.coolfonts.all())
        related_objects.extend(instance.keyboards.all())
        related_objects.extend(instance.wallpapers.all())
        related_objects.extend(instance.themes.all())
        related_objects.extend(ThemeIcon.objects.filter(theme__subcategory=instance))

    if isinstance(instance, Keyboard):
        related_objects.extend(instance.themes.all())

    if isinstance(instance, Wallpaper):
        related_objects.extend(instance.themes.all())

    for related_object in related_objects:
        keys.extend(get_instance_cache_keys(related_object))


def get_instance_cache_keys(instance, include_related=False):
    model = instance.__class__
    keys = list(MODEL_LIST_CACHE_KEYS.get(model, ()))

    detail_prefix = MODEL_DETAIL_CACHE_PREFIXES.get(model)
    if detail_prefix and instance.pk:
        keys.append(f"{detail_prefix}_{instance.pk}")

    if isinstance(instance, ThemeIcon) and instance.theme_id:
        keys.append(f"mobile_theme_theme_{instance.theme_id}")

    if include_related:
        extend_related_content_cache_keys(instance, keys)

    return keys


def invalidate_instance_cache(instance, include_related=False):
    delete_existing_cache_keys(get_instance_cache_keys(instance, include_related))


def invalidate_instances_cache(instances, include_related=False):
    keys = []
    for instance in instances:
        keys.extend(get_instance_cache_keys(instance, include_related))
    delete_existing_cache_keys(keys)
