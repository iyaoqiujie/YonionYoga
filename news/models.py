# -*- coding: utf-8 -*-

from django.db import models
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.search import index
from course.models import CoursePage

# Create your models here.


class NewsIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:
        verbose_name = '资讯列表页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        newspages = self.get_children().live().order_by('-first_published_at')
        wallpaper = Image.objects.filter(tags__name="资讯壁纸").order_by('-created_at')[0]
        paginator = Paginator(newspages, 3) # Show 3 resources per page
        page = request.GET.get('page')
        try:
            newspages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            newspages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            newspages = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context['newspages'] = newspages
        context['wallpaper'] = wallpaper
        return context


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class NewsTagIndexPage(Page):
    class Meta:
        verbose_name = '热点资讯页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        newspages = None
        if tag is None or tag == '':
            newspages = NewsPage.objects.all().order_by('-first_published_at')
        else:
            newspages = NewsPage.objects.filter(tags__name=tag).order_by('-first_published_at')

        cate = request.GET.get('cate')
        if cate and cate != '':
            newspages = newspages.filter(category=cate).order_by('-first_published_at')

        wallpaper = Image.objects.filter(tags__name="资讯壁纸").order_by('-created_at')[0]
        # Workshop
        umaylike = CoursePage.objects.filter(category='workshop')[:6]
        paginator = Paginator(newspages, 6) # Show 6 resources per page
        page = request.GET.get('page')
        try:
            newspages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            newspages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            newspages = paginator.page(paginator.num_pages)

        # Update template context
        context = super().get_context(request)
        context['tag'] = tag
        context['cate'] = cate
        context['umaylike'] = umaylike
        context['newspages'] = newspages
        context['wallpaper'] = wallpaper
        return context


class NewsPage(Page):
    CATEGORY_CHOICES = (
        ('news', '瑜伽动态'),
        ('wiki', '瑜伽百科'),
    )
    date = models.DateField('发表日期')
    intro = models.CharField('简介', max_length=256, blank=True)
    category = models.CharField('新闻类别', choices=CATEGORY_CHOICES, max_length=16, default='infinite')
    body = StreamField([
        ('标题', blocks.CharBlock(classname="full title")),
        ('段落', blocks.RichTextBlock()),
        ('图片', ImageChooserBlock()),
    ])
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)

    class Meta:
        verbose_name = '资讯详情页'
        verbose_name_plural = verbose_name

    def thumbnail_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="内容属性"),
        MultiFieldPanel([
            FieldPanel('category'),
            FieldPanel('intro'),
        ], heading='新闻简介'),
        StreamFieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="资讯壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class NewsPageGalleryImage(Orderable):
    page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='缩略图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]