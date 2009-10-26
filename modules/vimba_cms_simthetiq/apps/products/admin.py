# encoding: utf-8
from django.contrib import admin
from vimba_cms_simthetiq.apps.products.models import MediaTagsTranslation, ProductContent, DomainElement, MediaTags, FileFormat, ProductPage, Image, Video, DomainPage, Category, GalleryPage
#from vimba_cms.apps.www.models import Content

# -- PRODUCTS
# -----------

def delete_selected(modeladmin, request, queryset):
    for product in queryset:
        selected_product = ProductPage.objects.get(id=product.id)
        selected_product.delete()

delete_selected.short_description = "Delete selected product(s)"

def delete_all_product(modeladmin, request, queryset):
    for product in ProductPage.objects.all():
        #print("deleting product %s " % product)
        try:
            selected_product = ProductPage.objects.get(id=product.id)
            selected_product.delete()
        except:
            print("product not found %s" % product)
delete_all_product.short_description = "Delete all product(s)"

class MediaTagsTranslationInline(admin.StackedInline):
    model = MediaTagsTranslation
    extra = 1
    fields = ('language','tagname', )

class MediaTagsAdmin(admin.ModelAdmin):
    inlines = [MediaTagsTranslationInline]

class FileFormatAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['tags']
    list_display = ['name', 'description']

class VideoAdmin(admin.ModelAdmin):
    pass

class DomainElementInline(admin.StackedInline):
    filter_horizontal = ["images"]
    model = DomainElement
    extra = 2

class DomainPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (( None,
                   { 'fields': ('name', 'slug', 'status', 'description', 'keywords', 'language') }),
                 ('Contents ', 
                  { 'fields': ('content', 'video', 'file_format')}),
                 )
    inlines = [DomainElementInline]

# PRODUCT PAGE

class ProductContentInline(admin.StackedInline):
    model = ProductContent
    extra = 1

class ProductPageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [ ProductContentInline ]
    list_filter = ['category', 'status']
    # for debug 
    #list_display = ['name', 'previous', 'next', 'category', 'status']
    #production
    list_display = ['name', 'previous','next', 'category', 'status', 'original_image']
    actions = [delete_selected, delete_all_product]
    filter_horizontal = ["images", "videos"]
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (( 'Page information',
                   { 'fields': ('name', 'slug', 'status', 'description','language',  'keywords', 'default') }),
                 ('Product information ', 
                    { 'fields': ('product_description', 'category', 'product_id', 'polygon',
                                'texture_format', 'texture_resolution','file_format', 'similar_products','previous', 'next')}
                 ),
                 ('Product Media', 
                    { 'fields': ('original_image', 'images', 'videos',)}
                 ),
                )


class CategoryAdmin(admin.ModelAdmin):
    pass

#class ProductInformationInline(admin.StackedInline):
    #filter_horizontal = ["images"]
#    model = ProductInformation 
#    extra = 1
#    fields = ('language','description', 'note', 'keywords', )

#class ProductAdmin(admin.ModelAdmin):
 #   inlines = [ ProductInformationInline ]
 #   prepopulated_fields = {"slug": ("name",)}
#    filter_horizontal = ('images', 'videos')


class GalleryPageAdmin(admin.ModelAdmin):
    pass


# PRODUCTS
admin.site.register(MediaTags, MediaTagsAdmin)
admin.site.register(FileFormat, FileFormatAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(DomainPage, DomainPageAdmin)
admin.site.register(ProductPage, ProductPageAdmin)
#admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GalleryPage, GalleryPageAdmin)

# LICENCES
#class LicenceAdmin(admin.ModelAdmin):
 #   pass

#admin.site.register(Licence, LicenceAdmin)



