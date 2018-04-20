from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from pages.models import Page, Blog, Slider


@admin.register(Page)
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {
        'slug': (
            'title',
        )
    }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'icon',
                'content',
            ),
        }),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(Slider)
class SliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
