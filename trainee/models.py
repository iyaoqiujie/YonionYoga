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
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.models import Image
from wagtail.search import index
from course.models import CoursePage

# Create your models here.


class TraineeIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:
        verbose_name = '学员列表页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        traineepages = self.get_children().live().order_by('-first_published_at')
        wallpaper = Image.objects.filter(tags__name="学员壁纸").order_by('-created_at')[0]
        paginator = Paginator(traineepages, 3) # Show 3 resources per page
        page = request.GET.get('page')
        try:
            traineepages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            traineepages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            traineepages = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context['traineepages'] = traineepages
        context['wallpaper'] = wallpaper
        return context


class TraineePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'TraineePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class TraineeTagIndexPage(Page):
    class Meta:
        verbose_name = '学员动态页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        traineepages = None
        if tag is None or tag == '':
            traineepages = TraineePage.objects.all().order_by('-first_published_at')
        else:
            traineepages = TraineePage.objects.filter(tags__name=tag).order_by('-first_published_at')

        cate = request.GET.get('cate')
        if cate and cate != '':
            traineepages = traineepages.filter(category=cate).order_by('-first_published_at')

        # Workshop
        umaylike = CoursePage.objects.filter(category='workshop')[:6]
        wallpaper = Image.objects.filter(tags__name="学员壁纸").order_by('-created_at')[0]
        paginator = Paginator(traineepages, 9) # Show 9 resources per page
        page = request.GET.get('page')
        try:
            traineepages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            traineepages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            traineepages = paginator.page(paginator.num_pages)

        # Update template context
        context = super().get_context(request)
        context['tag'] = tag
        context['cate'] = cate
        context['umaylike'] = umaylike
        context['traineepages'] = traineepages
        context['wallpaper'] = wallpaper
        return context


class TraineePage(Page):
    CATEGORY_CHOICES = (
        ('story', '蜕变故事'),
        ('picture', '瑜伽图片'),
        ('video', '光影瑜伽'),
    )
    date = models.DateField('发表日期')
    category = models.CharField('类别', choices=CATEGORY_CHOICES, max_length=16, default='picture')
    name = models.CharField('姓名', max_length=32, blank=True)
    age = models.CharField('年龄', max_length=8, default='保密')
    occupation = models.CharField('职业', max_length=16, default='自由职业者')
    intro = RichTextField('简介', max_length=128, blank=True)
    body = StreamField([
        ('标题', blocks.CharBlock(classname="full title")),
        ('段落', blocks.RichTextBlock()),
        ('图片', ImageChooserBlock()),
    ])
    tags = ClusterTaggableManager(through=TraineePageTag, blank=True)

    class Meta:
        verbose_name = '学员详情页'
        verbose_name_plural = verbose_name

    def thumbnail_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def main_doc(self):
        gallery_item = self.gallery_docs.first()
        if gallery_item:
            return gallery_item.doc
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="内容属性"),
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('age'),
            FieldPanel('occupation'),
            FieldPanel('intro'),
            FieldPanel('category'),
        ], heading='学员简介'),
        StreamFieldPanel('body'),
        InlinePanel('gallery_images', label='Gallery images'),
        InlinePanel('gallery_docs', label='Gallery documents')
    ]

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="学员壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class TraineePageGalleryImage(Orderable):
    page = ParentalKey(TraineePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='缩略图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class TraineePageGalleryDocument(Orderable):
    page = ParentalKey(TraineePage, on_delete=models.CASCADE, related_name='gallery_docs')
    doc = models.ForeignKey(
        'wagtaildocs.Document', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+', verbose_name='视频文档'
    )
    caption = models.CharField('文档说明', blank=True, max_length=256)

    panels = [
        DocumentChooserPanel('doc'),
        FieldPanel('caption'),
    ]
