from collections import namedtuple
import datetime
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
import operator
from pytz import timezone


class FullHistoryFeed(Atom1Feed):
    """
    Use this feed type when your feed contains an entry for every post
    ever, rather than cutting off after the most recent 10. This
    generator adds the <fh:complete/> tag specified in RFC5005 ("Feed
    Paging and Archiving"), section 2 ("Complete Feeds").
    """

    def root_attributes(self):
        attrs = super(FullHistoryFeed, self).root_attributes()
        attrs['xmlns:fh'] = 'http://purl.org/syndication/history/1.0'
        return attrs

    def add_root_elements(self, handler):
        super(FullHistoryFeed, self).add_root_elements(handler)
        handler.addQuickElement('fh:complete')


PseudoPage = namedtuple('PseudoPage', [
    'title',
    'full_url',
    'owner',
    'first_published_at',
    'last_published_at',
])
PseudoPage.__doc__ = "Just enough like Wagtail's Page model to work as an item of a WagtailFeed."


class WagtailFeed(Feed):
    feed_type = FullHistoryFeed

    def get_object(self, request, page):
        return page

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.full_url

    def items(self, obj):
        items = list(obj.get_children().live())

        # add special posts that aren't stored as Wagtail pages

        staff = User.objects.filter(is_staff=True, comrade__isnull=False)
        try:
            author = staff.get(username='sage')
        except User.DoesNotExist:
            author = staff[0]

        pacific = timezone('US/Pacific')

        items.append(PseudoPage(
            title='Schedule changes for Outreachy',
            full_url=reverse('blog-schedule-changes'),
            owner=author,
            first_published_at=pacific.localize(datetime.datetime(2019, 7, 23, 15, 5, 1)),
            last_published_at=pacific.localize(datetime.datetime(2019, 7, 24, 16, 5, 38)),
        ))

        items.append(PseudoPage(
            title='Picking an Outreachy Project - December 2019 round',
            full_url=reverse('2019-12-pick-a-project'),
            owner=author,
            first_published_at=pacific.localize(datetime.datetime(2019, 10, 1, 7, 26, 0)),
            last_published_at=pacific.localize(datetime.datetime(2019, 10, 4, 12, 49, 0)),
        ))

        # put the Wagtail pages and special posts together in the right order
        items.sort(key=operator.attrgetter('first_published_at'), reverse=True)
        return items

    def item_title(self, item):
        return item.title

    item_description = None

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        try:
            return item.owner.comrade.public_name
        except ObjectDoesNotExist:
            return None

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return item.last_published_at
