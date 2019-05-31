from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from taggit.models import Tag
from wagtail.search import index

from wagtail.core.models import Page
from course.models import CoursePage
from mentor.models import MentorPage
from trainee.models import TraineePage

class HomePage(Page):
    body = RichTextField(blank=True)

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = verbose_name

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        tags = Tag.objects.all().order_by('name')
        course4mentor = CoursePage.objects.filter(tags__name='师资培训').order_by('-first_published_at')[:3]
        course4trainee = CoursePage.objects.filter(tags__name='名师工作坊').order_by('-first_published_at')[:3]
        coursepages = CoursePage.objects.filter(tags__name='首页展示').order_by('-first_published_at')[:3]
        mentorpages = MentorPage.objects.filter(tags__name='首页展示').order_by('-first_published_at')[:4]
        traineepages = TraineePage.objects.filter(category='story').order_by('-first_published_at')[:6]
        wallpapers = Image.objects.filter(tags__name="首页壁纸").order_by('-created_at')[:3]

        context['tags'] = tags
        context['course4mentor'] = course4mentor
        context['course4trainee'] = course4trainee
        context['coursepages'] = coursepages
        context['mentorpages'] = mentorpages
        context['traineepages'] = traineepages
        context['wallpapers'] = wallpapers
        return context

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
