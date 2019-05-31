# -*- coding: utf-8 -*-

from django.db import models
from django.shortcuts import render
from django.utils import timezone
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
from certificate.forms import CertQueryForm
import pysnooper

# Create your models here.


class CertIndexPage(Page):
    intro = RichTextField('简介', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    class Meta:
        verbose_name = '证书列表页'
        verbose_name_plural = verbose_name


class Cert(models.Model):
    id = models.BigAutoField(primary_key=True)
    cert_id = models.CharField(verbose_name='证书编号', max_length=32, unique=True)
    user_name = models.CharField(verbose_name='证书持有人姓名', max_length=32, blank=False)
    user_id = models.CharField(verbose_name='证书持有人身份证', max_length=64, unique=True)
    issue_date = models.DateField(verbose_name='证书签署时间', default=timezone.now)
    program = models.CharField(verbose_name='培训项目', max_length=64, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = 'Certificate'
        verbose_name = '瑜伽教练证书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '姓名:[{}], 证书编号:[{}]'.format(self.user_name, self.cert_id)


class CertQueryPage(Page):
    date = models.DateField('发表日期', auto_now_add=True)
    intro = RichTextField('简介', max_length=128, blank=True)

    class Meta:
        verbose_name = '证书查询页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="证书壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context

    def serve(self, request):
        # Context
        wallpaper = Image.objects.filter(tags__name="证书壁纸").order_by('-created_at')[0]
        umaylike = CoursePage.objects.filter(category='workshop')[:6]
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        context['umaylike'] = umaylike
        context['page'] = self

        if request.method == 'POST':
            form = CertQueryForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    my_cert = Cert.objects.get(cert_id=cd['cert_id'])
                    if my_cert.user_name != cd['user_name']:
                        context['err_info'] = '编号[{}]的证书持有者姓名与[{}]不符'.format(cd['cert_id'], cd['user_name'])
                        return render(request, 'certificate/cert_query_err.html', context)

                    context['cert'] = my_cert
                    return render(request, 'certificate/cert_detail.html', context)

                except Cert.DoesNotExist:
                    context['err_info'] = '编号[{}]的证书不存在'.format(cd['cert_id'])
                    return render(request, 'certificate/cert_query_err.html', context)
            else:
                form = CertQueryForm()
                context['form'] = form
                return render(request, 'certificate/cert_query_page.html', context)
        else:
            form = CertQueryForm()
            context['form'] = form
            return render(request, 'certificate/cert_query_page.html', context)


class CertHelpPage(Page):
    date = models.DateField('发表日期')
    intro = RichTextField('简介', max_length=128, blank=True)
    body = StreamField([
        ('标题', blocks.CharBlock(classname="full title")),
        ('段落', blocks.RichTextBlock()),
        ('图片', ImageChooserBlock()),
    ])

    class Meta:
        verbose_name = '证书帮助页'
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
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        StreamFieldPanel('body', help_text='标题与图片居中显示，段落文字左对齐显示'),
        InlinePanel('gallery_images', label='缩略图'),
        InlinePanel('docs', label='相关文档', )
    ]

    def get_context(self, request):
        wallpaper = Image.objects.filter(tags__name="证书壁纸").order_by('-created_at')[0]
        # Update template context
        context = super().get_context(request)
        context['wallpaper'] = wallpaper
        return context


class CertHelpPageGalleryImage(Orderable):
    page = ParentalKey(CertHelpPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', verbose_name='缩略图'
    )
    caption = models.CharField('图片说明', blank=True, max_length=256)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class CertHelpPageDocument(Orderable):
    page = ParentalKey(CertHelpPage, on_delete=models.CASCADE, related_name='docs')
    doc = models.ForeignKey(
        'wagtaildocs.Document', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+', verbose_name='证书相关文档'
    )
    caption = models.CharField('文档说明', blank=True, max_length=256)

    panels = [
        DocumentChooserPanel('doc'),
        FieldPanel('caption'),
    ]

