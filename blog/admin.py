from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Comment)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    class Meta:
        fields = '__all__'

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    class Meta:
        fields = '__all__'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    class Meta:
        fields = '__all__'

