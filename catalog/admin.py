from django import forms
from django.contrib import admin

from .cache import invalidate_instance_cache, invalidate_instances_cache
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
from .storage import img_upload


class CacheInvalidationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        old_obj = None
        if change and obj.pk:
            old_obj = obj.__class__.objects.filter(pk=obj.pk).first()

        if old_obj:
            invalidate_instance_cache(old_obj, include_related=True)

        super().save_model(request, obj, form, change)
        invalidate_instance_cache(obj)

    def delete_model(self, request, obj):
        invalidate_instance_cache(obj, include_related=True)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        invalidate_instances_cache(queryset, include_related=True)
        super().delete_queryset(request, queryset)


class UrlUploadForm(forms.ModelForm):
    upload_fields = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.base_fields = cls.base_fields.copy()
        cls.declared_fields = cls.declared_fields.copy()
        for upload_name, (model_field, _folder) in cls.upload_fields.items():
            upload_field = forms.FileField(
                required=False,
                label=f"{model_field.replace('_', ' ').title()} file upload",
                help_text="Choose a file to upload to Supabase. The returned URL will be saved in PostgreSQL.",
            )
            cls.base_fields[upload_name] = upload_field
            cls.declared_fields[upload_name] = upload_field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for upload_name, (model_field, _folder) in self.upload_fields.items():
            url_field = self.fields[model_field]
            url_field.required = False
            url_field.label = f"{url_field.label} URL (saved in PostgreSQL)"
            url_field.help_text = "This is the Supabase public URL saved in PostgreSQL."
            self.fields[upload_name].label = (
                f"{url_field.label.replace(' URL (saved in PostgreSQL)', '')} file upload"
            )

    def clean(self):
        cleaned_data = super().clean()
        for upload_name, (model_field, _folder) in self.upload_fields.items():
            model_field_obj = self._meta.model._meta.get_field(model_field)
            saved_url = cleaned_data.get(model_field)
            uploaded_file = cleaned_data.get(upload_name)

            if not model_field_obj.blank and not saved_url and not uploaded_file:
                self.add_error(
                    upload_name,
                    forms.ValidationError(
                        f"Upload a file or enter a URL for {model_field_obj.verbose_name}."
                    ),
                )
        return cleaned_data


class UrlUploadAdmin(CacheInvalidationAdmin):
    upload_fields = {}

    def get_fields(self, request, obj=None):
        fields = [
            field
            for field in super().get_fields(request, obj)
            if not field.endswith("_upload") or field in self.upload_fields
        ]
        for upload_name, (model_field, _folder) in self.upload_fields.items():
            if upload_name in fields:
                continue

            if model_field in fields:
                field_index = fields.index(model_field)
                fields.insert(field_index + 1, upload_name)
            else:
                fields.append(upload_name)

        return fields

    def save_model(self, request, obj, form, change):
        for upload_name, (model_field, folder) in self.upload_fields.items():
            uploaded_file = form.cleaned_data.get(upload_name)
            if uploaded_file:
                setattr(obj, model_field, img_upload(uploaded_file, folder))
        super().save_model(request, obj, form, change)


class CategoryAdminForm(UrlUploadForm):
    upload_fields = {"thumbnail_upload": ("thumbnail", "categories")}

    class Meta:
        model = Category
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(UrlUploadAdmin):
    form = CategoryAdminForm
    upload_fields = CategoryAdminForm.upload_fields


class SubCategoryAdminForm(UrlUploadForm):
    upload_fields = {"thumbnail_upload": ("thumbnail", "categories")}

    class Meta:
        model = SubCategory
        fields = "__all__"


@admin.register(SubCategory)
class SubCategoryAdmin(UrlUploadAdmin):
    form = SubCategoryAdminForm
    upload_fields = SubCategoryAdminForm.upload_fields


class CoolFontAdminForm(UrlUploadForm):
    upload_fields = {"thumbnail_upload": ("thumbnail", "diy/cool-fonts")}

    class Meta:
        model = CoolFont
        fields = "__all__"


@admin.register(CoolFont)
class CoolFontAdmin(UrlUploadAdmin):
    form = CoolFontAdminForm
    upload_fields = CoolFontAdminForm.upload_fields


class KeyboardAdminForm(UrlUploadForm):
    upload_fields = {
        "preview_upload": ("preview_url", "keyboards"),
        "keyboard_upload": ("keyboard_bg", "keyboards"),
        "normalkey_upload": ("normal_key_bg", "keyboards"),
        "specialty_upload": ("specialty_keys_bg", "keyboards"),
        "backspace_upload": ("backspace_key_bg", "keyboards"),
        "uppercase_upload": ("uppercase_letter_bg", "keyboards"),
        "numberbutton_upload": ("number_button_bg", "keyboards"),
        "emoji_upload": ("emoji_button_bg", "keyboards"),
        "commabutton_upload": ("comma_button_bg", "keyboards"),
        "enterbutton_upload": ("enter_button_bg", "keyboards"),
    }

    class Meta:
        model = Keyboard
        fields = "__all__"


@admin.register(Keyboard)
class KeyboardAdmin(UrlUploadAdmin):
    form = KeyboardAdminForm
    upload_fields = KeyboardAdminForm.upload_fields


class WallpaperAdminForm(UrlUploadForm):
    upload_fields = {
        "image_upload": ("image_url", "wallpapers"),
        "preview_upload": ("preview_url", "wallpapers"),
    }

    class Meta:
        model = Wallpaper
        fields = "__all__"


@admin.register(Wallpaper)
class WallpaperAdmin(UrlUploadAdmin):
    form = WallpaperAdminForm
    upload_fields = WallpaperAdminForm.upload_fields


class ThemeAdminForm(UrlUploadForm):
    upload_fields = {"preview_upload": ("preview_url", "themes")}

    class Meta:
        model = Theme
        fields = "__all__"


@admin.register(Theme)
class ThemeAdmin(UrlUploadAdmin):
    form = ThemeAdminForm
    upload_fields = ThemeAdminForm.upload_fields


class ThemeIconAdminForm(UrlUploadForm):
    upload_fields = {
        "preview_upload": ("preview_url", "themes"),
        "icon_upload": ("icon_image", "themes"),
    }

    class Meta:
        model = ThemeIcon
        fields = "__all__"


@admin.register(ThemeIcon)
class ThemeIconAdmin(UrlUploadAdmin):
    form = ThemeIconAdminForm
    upload_fields = ThemeIconAdminForm.upload_fields


class DiyImageAdminForm(UrlUploadForm):
    upload_fields = {"image_upload": ("image_url", "diy/images")}

    class Meta:
        model = DiyImage
        fields = "__all__"


@admin.register(DiyImage)
class DiyImageAdmin(UrlUploadAdmin):
    form = DiyImageAdminForm
    upload_fields = DiyImageAdminForm.upload_fields


class DiyKeyAdminForm(UrlUploadForm):
    upload_fields = {
        "image_upload": ("image_url", "diy/keys"),
        "special_key_upload": ("special_key_bg", "diy/keys"),
    }

    class Meta:
        model = DiyKey
        fields = "__all__"


@admin.register(DiyKey)
class DiyKeyAdmin(UrlUploadAdmin):
    form = DiyKeyAdminForm
    upload_fields = DiyKeyAdminForm.upload_fields


class DiyFontAdminForm(UrlUploadForm):
    upload_fields = {"font_upload": ("font_file", "diy/fonts")}

    class Meta:
        model = DiyFont
        fields = "__all__"


@admin.register(DiyFont)
class DiyFontAdmin(UrlUploadAdmin):
    form = DiyFontAdminForm
    upload_fields = DiyFontAdminForm.upload_fields


class DiyEffectAdminForm(UrlUploadForm):
    upload_fields = {
        "gif_upload": ("gif_url", "diy/effects"),
        "preview_upload": ("preview_url", "diy/effects"),
    }

    class Meta:
        model = DiyEffect
        fields = "__all__"


@admin.register(DiyEffect)
class DiyEffectAdmin(UrlUploadAdmin):
    form = DiyEffectAdminForm
    upload_fields = DiyEffectAdminForm.upload_fields


class DiySoundAdminForm(UrlUploadForm):
    upload_fields = {
        "sound_upload": ("sound_file", "diy/sounds"),
        "preview_upload": ("preview_url", "diy/sounds"),
    }

    class Meta:
        model = DiySound
        fields = "__all__"


@admin.register(DiySound)
class DiySoundAdmin(UrlUploadAdmin):
    form = DiySoundAdminForm
    upload_fields = DiySoundAdminForm.upload_fields
