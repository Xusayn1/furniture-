from django.db import models
from django.utils.translation import gettext_lazy as _
from shared.models import BaseModel


class Author(BaseModel):
    full_name = models.CharField(max_length=128, verbose_name=_('full name'))
    image = models.ImageField(upload_to='authors/', verbose_name=_('image'))
    about = models.CharField(max_length=255, verbose_name=_('about'))
    professions = models.CharField(max_length=128, verbose_name=_('professions'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'authors'
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Category(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('title'))
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Tag(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('title'))

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tags'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class BlogStatus(models.TextChoices):
    PUBLISHED = "PUBLISHED", _("Published")
    DRAFT = "DRAFT", _("Draft")
    DELETED = "DELETED", _("Deleted")


class Blog(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('title'))
    short_description = models.CharField(max_length=255, verbose_name=_('short description'))
    image = models.ImageField(upload_to='blogs/', null=True, blank=True, verbose_name=_('image'))

    # this will change into rich text uploading field
    long_description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=BlogStatus.choices,
        default=BlogStatus.DRAFT
    )

    categories = models.ManyToManyField(
        Category, related_name='blogs'
    )
    tags = models.ManyToManyField(
        Tag, related_name='blogs'
    )
    authors = models.ManyToManyField(
        Author, related_name='blogs'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blogs'
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')
