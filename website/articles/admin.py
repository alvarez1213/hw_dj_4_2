from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope


class ScopesInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_ismain = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main', False) == True:
                count_ismain += 1
            if count_ismain > 1:
                raise ValidationError('Основной тег может быть только один')

        if count_ismain == 0:
            raise ValidationError('Укажите основной тег')

        return super().clean()


class ScopesInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopesInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', ]
    list_filter = ['published_at', ]
    inlines = [ScopesInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


