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

# Create your models here.


class CourseIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        coursepages = self.get_children().live().order_by('-first_published_at')
        wallpaper = Image.objects.filter(tags__name="课程壁纸").order_by('-created_at')[0]
        paginator = Paginator(coursepages, 3) # Show 3 resources per page
        page = request.GET.get('page')
        try:
            coursepages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            coursepages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            coursepages = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context['coursepages'] = coursepages
        context['wallpaper'] = wallpaper
        return context

    class Meta:
        verbose_name = '课程列表页'
        verbose_name_plural = verbose_name


class CoursePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'CoursePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class CourseTagIndexPage(Page):
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        coursepages = None
        if tag is None or tag == '':
            coursepages = CoursePage.objects.all().order_by('-first_published_at')
        else:
            coursepages = CoursePage.objects.filter(tags__name=tag).order_by('-first_published_at')

        cate = request.GET.get('cate')
        if cate and cate != '':
            coursepages = coursepages.filter(category=cate).order_by('-first_published_at')
        wallpaper = Image.objects.filter(tags__name="课程壁纸").order_by('-created_at')[0]
        paginator = Paginator(coursepages, 6) # Show 6 resources per page
        page = request.GET.get('page')
        try:
            coursepages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            coursepages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            coursepages = paginator.page(paginator.num_pages)

        # Update template context
        context = super().get_context(request)
        context['tag'] = tag
        context['cate'] = cate
        context['coursepages'] = coursepages
        context['wallpaper'] = wallpaper
        return context

    class Meta:
        verbose_name = '热门课程页'
        verbose_name_plural = verbose_name


class CoursePage(Page):
    CATEGORY_CHOICES = (
        ('faculty', '师资培训'),
        ('workshop', '名师工作坊'),
    )
    date = models.DateField('发表日期')
    intro = models.CharField('简介', max_length=256)
    plan = models.CharField('课程安排', max_length=64, default='每月-开课')
    category = models.CharField('课程类别', choices=CATEGORY_CHOICES, max_length=16, default='workshop')
    advantage = models.CharField('课程优势', max_length=256, blank=True)
    body = StreamField([
        ('标题', blocks.CharBlock(classname="full title")),
        ('段落', blocks.RichTextBlock()),
        ('图片', ImageChooserBlock()),
    ])
    tags = ClusterTaggableManager(through=CoursePageTag, blank=True)

    class Meta:
        verbose_name = '课程详情页'
        verbose_name_plural = verbose_name

    def main_image(self):
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
            FieldPanel('intro'),
            FieldPanel('plan'),
            FieldPanel('advantage'),
            FieldPanel('category'),
        ], heading='课程介绍'),
        StreamFieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="课程壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class CoursePageGalleryImage(Orderable):
    page = ParentalKey(CoursePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='缩略图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

