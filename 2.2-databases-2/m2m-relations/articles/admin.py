from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        flag = False
        for form in self.forms:
            if form.cleaned_data.get('is_main') and flag:
                raise ValidationError('Oсновным может быть только один Тэг')
            if form.cleaned_data.get('is_main') and not flag:
                flag = True
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 5
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    list_filter = ['title', 'published_at']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']