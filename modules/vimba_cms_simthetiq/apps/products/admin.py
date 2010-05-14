# encoding: utf-8
from django.contrib import admin
from django import forms
from vimba_cms_simthetiq.tools.widgets.admin_image_widget import AdminImageWidget
from vimba_cms_simthetiq.apps.products.models import Kind, Domain, DISCountry, Category, StandardNavigationGroup
from vimba_cms_simthetiq.apps.products.models import MediaTagsTranslation, MediaTags, FileFormat, ProductPage, ProductContent,Image, Video  
    #DomainPage, DomainElement, GalleryPage
#from vcms.apps.www.models import Content

# -- PRODUCTS
# -----------

class MediaTagsTranslationInline(admin.StackedInline):
    model = MediaTagsTranslation
    extra = 1
    fields = ('language','tagname', )

class MediaTagsAdmin(admin.ModelAdmin):
    inlines = [MediaTagsTranslationInline]

class FileFormatAdmin(admin.ModelAdmin):
    def delete_selected(self, request, queryset):
        for ff in queryset:
            selected_ff = FileFormat.objects.get(id=ff.id)
            selected_ff.delete()

    delete_selected.short_description = "Delete selected File format(s)"
    actions = [delete_selected]

class ImageAdminForm(forms.ModelForm):
    file = forms.FileField(widget=AdminImageWidget)
    thumbnail = forms.FileField(widget=AdminImageWidget)
    class Meta:
        model = Image

class ImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    search_fields = ['name']
    list_filter = ['tags']
    list_display = ['name', 'description']
    
    def delete_selected(self, request, queryset):
        for img in queryset:
            selected_img = Image.objects.get(id=img.id)
            selected_img.delete()

    delete_selected.short_description = "Delete selected images(s)"
    actions = [delete_selected]

class VideoAdminForm(forms.ModelForm):
    thumbnail = forms.ImageField(widget=AdminImageWidget)
    class Meta:
        model = Video

class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    def delete_selected(self, request, queryset):
        for vid in queryset:
            selected_vid = Video.objects.get(id=vid.id)
            selected_vid.delete()

    delete_selected.short_description = "Delete selected video(s)"
    actions = [delete_selected]

# DOMAIN PAGE 
"""
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
    
    def delete_selected(self, request, queryset):
        for dp in queryset:
            selected_dp = DomainPage.objects.get(id=dp.id)
            selected_dp.delete()

    delete_selected.short_description = "Delete selected Domain page(s)"
    actions = [delete_selected]
admin.site.register(DomainPage, DomainPageAdmin)
"""
# PRODUCT PAGE

class ProductContentInline(admin.StackedInline):
    model = ProductContent
    extra = 1

class ProductPageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [ ProductContentInline ]
    list_filter = ['category', 'status']
    # for debug 
    # list_display = ['name', 'previous', 'next', 'category', 'status']
    # production
    list_display = ['id', 'name', 'previous','next', 'category', 'status', 'original_image']
    filter_horizontal = ["images", "videos"]
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (( 'Page information',
                   { 'fields': ('name', 'slug', 'status', 'description','language',  'keywords', 'default') }),
                 ('DIS',
                    {'fields': ('category', 'used_in', 'dis_country', 'dis_subcategory_id', 'dis_specific_id',)}),
                 ('Product information ', 
                    { 'fields': ('product_description',  'polygon',
                                'texture_format', 'texture_resolution','file_format', 'similar_products','previous', 'next')}
                 ),
                 ('Product Media', 
                    { 'fields': ('original_image', 'images', 'videos',)}
                 ),
                )

    def delete_selected(self, request, queryset):
        for product in queryset:
            selected_product = ProductPage.objects.get(id=product.id)
            selected_product.delete()

    delete_selected.short_description = "Delete selected product(s)"
    
    def delete_all_product(self, request, queryset):
        for product in ProductPage.objects.all():
            #print("deleting product %s " % product)
            try:
                selected_product = ProductPage.objects.get(id=product.id)
                selected_product.delete()
            except:
                pass
                #print("product not found %s" % product)
    
    delete_all_product.short_description = "Delete all product(s)"

    def reorder_all_product(self, request, queryset):
        ProductPage.objects.reorder_product_position()
    
    reorder_all_product.short_description = "Reorder previous/next of all product(s) - might be slow"
    
    def reorder_selected_product(self, request, queryset):
        for product in queryset:
            product.save()
    
    reorder_selected_product.short_description = "Reorder previous/next of selected product(s) - might be slow"
    
    actions = [delete_selected, reorder_all_product, reorder_selected_product]

class KindAdmin(admin.ModelAdmin):
    search_fields = ['name', 'dis_id']
    list_filter = ['dis_id', 'name']
    
class DomainAdmin(admin.ModelAdmin):
    search_fields = ['name', 'dis_id']
    list_filter = ['dis_id', 'name']
    
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'dis_id']
    list_filter = ['kind', 'domain', 'compact_navigation']
    fieldsets = (( 'DIS',
                   { 'fields': ('kind', 'domain','name', 'dis_id', ) }),
                 ('Compact',
                    {'fields': ('compact_navigation',)}
                  ),)

    def delete_selected(self, request, queryset):
        for category in queryset:
            selected_category = Category.objects.get(id=category.id)
            selected_category.delete()

    delete_selected.short_description = "Delete selected Category(ies)"
    actions = [delete_selected]

    
class StandardNavigationGroupAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(StandardNavigationGroup, StandardNavigationGroupAdmin)

class DISCountryAdmin(admin.ModelAdmin):
    pass
admin.site.register(DISCountry, DISCountryAdmin)


#class ProductInformationInline(admin.StackedInline):
    #filter_horizontal = ["images"]
#    model = ProductInformation 
#    extra = 1
#    fields = ('language','description', 'note', 'keywords', )

#class ProductAdmin(admin.ModelAdmin):
 #   inlines = [ ProductInformationInline ]
 #   prepopulated_fields = {"slug": ("name",)}
#    filter_horizontal = ('images', 'videos')

"""
class GalleryPageAdmin(admin.ModelAdmin):
    pass
admin.site.register(GalleryPage, GalleryPageAdmin)
"""

# PRODUCTS
admin.site.register(MediaTags, MediaTagsAdmin)
admin.site.register(FileFormat, FileFormatAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(ProductPage, ProductPageAdmin)
#admin.site.register(Product, ProductAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Category, CategoryAdmin)

# LICENCES
#class LicenceAdmin(admin.ModelAdmin):
 #   pass

#admin.site.register(Licence, LicenceAdmin)



