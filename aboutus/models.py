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


class AboutusIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:
        verbose_name = '关于我们总览页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        wallpaper = Image.objects.filter(tags__name="资讯壁纸").order_by('-created_at')[0]

        # make the variable 'resources' available on the template
        context['wallpaper'] = wallpaper
        return context


class ClassRoomPage(Page):
    date = models.DateField('发表日期')
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        InlinePanel('classroom_images', label="学习环境"),
    ]

    class Meta:
        verbose_name = '学习环境页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="学习环境壁纸").order_by('-created_at')[0]

        items = self.classroom_images.all()
        paginator = Paginator(items, 6) # Show 6 resources per page
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)

        # Update template context
        context = super().get_context(request)
        context['items'] = items
        context['wallpaper'] = wallpaper
        return context


class ClassRoomPageGalleryImage(Orderable):
    page = ParentalKey(ClassRoomPage, on_delete=models.CASCADE, related_name='classroom_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='简图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class EventBlock(blocks.StructBlock):
    date = blocks.DateBlock('日期')
    event = blocks.CharBlock('事件', max_length=32)
    direction = blocks.ChoiceBlock(choices=(
                ('left', '向左'),
                ('right', '向右'),
            ), default='left')

    class Meta:
        template = 'aboutus/milestone_block.html'


class MilestonePage(Page):
    date = models.DateField('发表日期')
    body = StreamField([
        ('milestone_list', blocks.ListBlock(EventBlock)),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = '发展历程页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="发展历程壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class AboutusPage(Page):
    date = models.DateField('发表日期')
    body = StreamField([
        ('标题', blocks.CharBlock(classname="full title")),
        ('段落', blocks.RichTextBlock()),
        ('图片', ImageChooserBlock()),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = '关于我们页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="关于我们壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class ContactusIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:
        verbose_name = '联系我们列表页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        wallpaper = Image.objects.filter(tags__name="联系我们壁纸").order_by('-created_at')[0]
        contactuspages = ContactusPage.objects.all().order_by('-first_published_at')
        paginator = Paginator(contactuspages, 6) # Show 6 resources per page
        page = request.GET.get('page')
        try:
            contactuspages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contactuspages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contactuspages = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context['wallpaper'] = wallpaper
        context['contactuspages'] = contactuspages
        return context


class ContactusPage(Page):
    date = models.DateField('发表日期')
    name = models.CharField('名称', max_length=128)
    addr = models.CharField('地址', max_length=128)
    phone = models.CharField('电话', max_length=32)
    traffic_route = models.CharField('交通路线', max_length=256, blank=True)
    longitude = models.FloatField('经度', default=118.104776)
    latitude = models.FloatField('纬度', default=24.47439)

    class Meta:
        verbose_name = '联系我们详情页'
        verbose_name_plural = verbose_name

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('addr'),
        index.SearchField('phone'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('addr'),
            FieldPanel('phone'),
            FieldPanel('traffic_route'),
        ], heading="学校简介"),
        MultiFieldPanel([
            FieldPanel('longitude'),
            FieldPanel('latitude')
        ]),
        InlinePanel('gallery_images', label='缩略图'),
    ]

    def thumbnail_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="联系我们壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context

    class Meta:
        verbose_name = '联系我们'
        verbose_name_plural = verbose_name


class ContactusPageGalleryImage(Orderable):
    page = ParentalKey(ContactusPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='缩略图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class CobranchIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:
        verbose_name = '合作机构列表页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        wallpaper = Image.objects.filter(tags__name="合作机构壁纸").order_by('-created_at')[0]
        cobranchpages = CobranchPage.objects.all().order_by('-first_published_at')
        paginator = Paginator(cobranchpages, 6) # Show 6 resources per page
        page = request.GET.get('page')
        try:
            cobranchpages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            cobranchpages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            cobranchpages = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context['wallpaper'] = wallpaper
        context['cobranchpages'] = cobranchpages
        return context


class CobranchPage(Page):
    date = models.DateField('发表日期')
    name = models.CharField('名称', max_length=128)
    addr = models.CharField('地址', max_length=128)
    phone = models.CharField('电话', max_length=32)
    traffic_route = models.CharField('交通路线', max_length=256, blank=True)
    longitude = models.FloatField('经度', default=118.104776)
    latitude = models.FloatField('纬度', default=24.47439)

    class Meta:
        verbose_name = '合作机构详情页'
        verbose_name_plural = verbose_name

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('addr'),
        index.SearchField('phone'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('addr'),
            FieldPanel('phone'),
            FieldPanel('traffic_route'),
        ], heading="机构简介"),
        MultiFieldPanel([
            FieldPanel('longitude'),
            FieldPanel('latitude')
        ]),
        InlinePanel('gallery_images', label='缩略图'),
    ]

    def thumbnail_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="合作机构壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class CobranchPageGalleryImage(Orderable):
    page = ParentalKey(CobranchPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='缩略图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]