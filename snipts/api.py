import datetime
import hashlib
import parsedatetime as pdt
import re
import requests
import time

from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date, urlize, linebreaksbr
from haystack.query import SearchQuerySet
from snipts.models import Favorite, Snipt
from taggit.models import Tag
from taggit.utils import edit_string_for_tags, parse_tags
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.exceptions import Unauthorized
from tastypie.fields import ListField
from tastypie.models import create_api_key
from tastypie.resources import ModelResource
from tastypie.validation import Validation

models.signals.post_save.connect(create_api_key, sender=User)


class PrivateFavoriteAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        raise Unauthorized()

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class PrivateSniptAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.is_authorized_user(bundle.request.user)

    def create_list(self, object_list, bundle):
        raise Unauthorized()

    def create_detail(self, object_list, bundle):
        user = bundle.obj.user
        if user == bundle.request.user:
            return True
        if user.profile.is_a_team:
            return user.team.user_is_member(bundle.request.user)
        return False

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        return bundle.obj.is_authorized_user(bundle.request.user)

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        return bundle.obj.is_authorized_user(bundle.request.user)


class PrivateUserProfileAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        raise Unauthorized()

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized()

    def create_detail(self, object_list, bundle):
        raise Unauthorized()

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized()


class PrivateUserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        raise Unauthorized()

    def read_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def create_list(self, object_list, bundle):
        raise Unauthorized()

    def create_detail(self, object_list, bundle):
        raise Unauthorized()

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        raise Unauthorized()

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized()


class FavoriteValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        snipt = bundle.data["snipt"]

        if Favorite.objects.filter(user=bundle.request.user, snipt=snipt).count():
            errors = "User has already favorited this snipt."

        return errors


class SniptValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if len(bundle.data["title"]) > 255:
            errors = "Title must be 255 characters or less."

        return errors


class UserProfileValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        for field in bundle.data:
            if bundle.data[field]:
                if not re.match("^[ A-Za-z0-9\/\@\._-]*$", bundle.data[field]):
                    errors[field] = (
                        "Only spaces, letters, numbers, "
                        "underscores, dashes, periods, forward "
                        'slashes, and "at sign" are valid.'
                    )

        return errors


class PublicUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        fields = ["id", "username"]
        include_absolute_url = True
        allowed_methods = ["get"]
        filtering = {"username": ["contains", "exact"]}
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data["snipts"] = "/api/public/snipt/?user=%d" % bundle.obj.id
        bundle.data["email_md5"] = hashlib.md5(
            bundle.obj.email.lower().encode("utf-8")
        ).hexdigest()
        bundle.data["snipts_count"] = Snipt.objects.filter(
            user=bundle.obj.id, public=True
        ).count()
        return bundle


class PublicTagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.filter()
        queryset = queryset.annotate(count=models.Count("taggit_taggeditem_items__id"))
        queryset = queryset.order_by("-count", "name")
        resource_name = "tag"
        fields = ["id", "name"]
        allowed_methods = ["get"]
        max_limit = 200
        cache = SimpleCache()

    def build_filters(self, filters=None, **kwargs):
        if filters is None:
            filters = {}

        orm_filters = super(PublicTagResource, self).build_filters(filters)

        if "q" in filters:
            orm_filters["slug"] = filters["q"]

        return orm_filters

    def dehydrate(self, bundle):
        bundle.data["absolute_url"] = "/public/tag/%s/" % bundle.obj.slug
        bundle.data["snipts"] = "/api/public/snipt/?tag=%d" % bundle.obj.id
        return bundle


class PublicSniptResource(ModelResource):
    user = fields.ForeignKey(PublicUserResource, "user", full=True)
    tags = fields.ToManyField(PublicTagResource, "tags", related_name="tag", full=True)

    class Meta:
        queryset = Snipt.objects.filter(public=True).order_by("-created")
        resource_name = "snipt"
        fields = [
            "id",
            "title",
            "slug",
            "lexer",
            "code",
            "description",
            "line_count",
            "stylized",
            "created",
            "modified",
            "publish_date",
            "blog_post",
            "meta",
        ]
        include_absolute_url = True
        allowed_methods = ["get"]
        filtering = {"user": "exact", "blog_post": "exact"}
        ordering = ["created", "modified"]
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data["embed_url"] = bundle.obj.get_embed_url()
        bundle.data["raw_url"] = bundle.obj.get_raw_url()
        bundle.data["full_absolute_url"] = bundle.obj.get_full_absolute_url()
        bundle.data["description_rendered"] = linebreaksbr(
            urlize(bundle.obj.description)
        )

        log_entries = bundle.obj.sniptlogentry_set.all()
        bundle_log_entries = []

        for entry in log_entries:
            bundle_log_entries.append(
                {
                    "created": entry.created,
                    "user": entry.user,
                    "code": entry.code,
                    "diff": entry.diff,
                }
            )

        bundle.data["log_entries"] = bundle_log_entries

        if "omit_code" in bundle.request.GET:
            del bundle.data["code"]

        if "omit_stylized" in bundle.request.GET:
            del bundle.data["stylized"]

        return bundle

    def build_filters(self, filters=None, **kwargs):
        if filters is None:
            filters = {}

        orm_filters = super(PublicSniptResource, self).build_filters(filters)

        if "tag" in filters:
            tag = Tag.objects.get(pk=filters["tag"])
            tagged_items = tag.taggit_taggeditem_items.all()
            orm_filters["pk__in"] = [i.object_id for i in tagged_items]

        if "q" in filters:
            sqs = SearchQuerySet().auto_query(filters["q"])
            orm_filters["pk__in"] = [i.pk for i in sqs]

        return orm_filters


class PrivateUserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = "profile"
        excludes = ["is_pro"]
        validation = UserProfileValidation()
        include_absolute_url = False
        allowed_methods = ["get", "put"]
        list_allowed_methods = []
        authentication = ApiKeyAuthentication()
        authorization = PrivateUserProfileAuthorization()
        always_return_data = True
        max_limit = 200

    def dehydrate(self, bundle):
        bundle.data["email"] = bundle.obj.user.email
        bundle.data["username"] = bundle.obj.user.username
        bundle.data["user_id"] = bundle.obj.user.id
        bundle.data["api_key"] = bundle.obj.user.api_key.key
        return bundle


class PrivateUserResource(ModelResource):
    profile = fields.ForeignKey(PrivateUserProfileResource, "profile", full=False)

    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        fields = ["id", "username", "email"]
        include_absolute_url = True
        allowed_methods = ["get"]
        list_allowed_methods = []
        authentication = ApiKeyAuthentication()
        authorization = PrivateUserAuthorization()
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data["email_md5"] = hashlib.md5(
            bundle.obj.email.lower().encode("utf-8")
        ).hexdigest()
        bundle.data["stats"] = {
            "public_snipts": Snipt.objects.filter(
                user=bundle.obj.id, public=True
            ).count(),
            "private_snipts": Snipt.objects.filter(
                user=bundle.obj.id, public=False
            ).count(),
            "total_snipts": Snipt.objects.filter(user=bundle.obj.id).count(),
            "total_views": Snipt.objects.filter(user=bundle.obj.id).aggregate(
                models.Sum("views")
            )["views__sum"],
        }

        user_snipts = Snipt.objects.filter(user=bundle.obj)
        user_tags = [snipt["tags"] for snipt in user_snipts.values("tags").distinct()]

        tags = [
            tag["name"]
            for tag in Tag.objects.filter(id__in=user_tags).values("name").distinct()
        ]

        bundle.data["tags"] = tags

        bundle.data["lexers"] = [
            snipt["lexer"] for snipt in user_snipts.values("lexer").distinct()
        ]

        return bundle


class PrivateSniptResource(ModelResource):
    user = fields.ForeignKey(PrivateUserResource, "user", full=True)
    last_user_saved = fields.ForeignKey(
        PrivateUserResource, "last_user_saved", null=True, full=False
    )
    tags_list = ListField()
    tags = fields.ToManyField(PublicTagResource, "tags", related_name="tag", full=True)

    class Meta:
        queryset = Snipt.objects.all().order_by("-created")
        resource_name = "snipt"
        fields = [
            "id",
            "title",
            "slug",
            "lexer",
            "code",
            "description",
            "line_count",
            "stylized",
            "key",
            "public",
            "secure",
            "blog_post",
            "created",
            "modified",
            "publish_date",
            "meta",
        ]
        include_absolute_url = True
        detail_allowed_methods = ["get", "patch", "put", "delete"]
        list_allowed_methods = ["get", "post"]
        authentication = ApiKeyAuthentication()
        authorization = PrivateSniptAuthorization()
        validation = SniptValidation()
        ordering = ["created", "modified"]
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data["embed_url"] = bundle.obj.get_embed_url()
        bundle.data["raw_url"] = bundle.obj.get_raw_url()
        bundle.data["tags_list"] = edit_string_for_tags(bundle.obj.tags.all())
        bundle.data["full_absolute_url"] = bundle.obj.get_full_absolute_url()
        bundle.data["description_rendered"] = linebreaksbr(
            urlize(bundle.obj.description)
        )
        bundle.data["views"] = bundle.obj.views
        bundle.data["favs"] = bundle.obj.favs()

        if bundle.data["publish_date"]:
            bundle.data["publish_date"] = date(
                bundle.data["publish_date"], "M d, Y \\a\\t h:i A"
            )

        log_entries = bundle.obj.sniptlogentry_set.all()
        bundle_log_entries = []

        for entry in log_entries:
            bundle_log_entries.append(
                {
                    "created": entry.created,
                    "user": entry.user,
                    "code": entry.code,
                    "diff": entry.diff,
                }
            )

        bundle.data["log_entries"] = bundle_log_entries

        return bundle

    def obj_create(self, bundle, **kwargs):
        bundle.data["last_user_saved"] = bundle.request.user
        bundle.data["tags_list"] = bundle.data.get("tags")
        bundle.data["tags"] = []

        if "intended_user" in bundle.data:
            bundle.data["user"] = User.objects.get(
                username=bundle.data["intended_user"]
            )
        else:
            bundle.data["user"] = bundle.request.user

        if "blog_post" in bundle.data:
            bundle = self._clean_publish_date(bundle)

        return super(PrivateSniptResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, **kwargs):

        instance = Snipt.objects.get(pk=bundle.data["id"])

        if instance.user.profile.is_a_team:
            user = instance.user
        else:
            user = bundle.request.user

        bundle.data["created"] = None
        bundle.data["last_user_saved"] = bundle.request.user
        bundle.data["modified"] = None
        bundle.data["user"] = user

        if type(bundle.data["tags"]) == str or type(bundle.data["tags"]) == unicode:
            bundle.data["tags_list"] = bundle.data["tags"]
        else:
            bundle.data["tags_list"] = ""
        bundle.data["tags"] = ""

        if "blog_post" in bundle.data:
            bundle = self._clean_publish_date(bundle)

        return super(PrivateSniptResource, self).obj_update(bundle, **kwargs)

    def _clean_publish_date(self, bundle):
        if bundle.data["blog_post"] and "publish_date" not in bundle.data:
            bundle.data["publish_date"] = datetime.datetime.now()
        elif bundle.data["publish_date"] == "":
            bundle.data["publish_date"] = datetime.datetime.now()
        elif bundle.data["blog_post"]:
            c = pdt.Constants()
            p = pdt.Calendar(c)
            publish_date, result = p.parse(bundle.data["publish_date"])

            if result != 0:
                publish_date = time.strftime("%Y-%m-%d %H:%M:%S", publish_date)
            else:
                publish_date = datetime.datetime.now()

            bundle.data["publish_date"] = publish_date
        elif not bundle.data["blog_post"]:
            bundle.data["publish_date"] = None

        return bundle

    def build_filters(self, filters=None, **kwargs):
        if filters is None:
            filters = {}

        orm_filters = super(PrivateSniptResource, self).build_filters(filters)

        if "tag" in filters:
            tag = Tag.objects.get(pk=filters["tag"])
            tagged_items = tag.taggit_taggeditem_items.all()
            orm_filters["pk__in"] = [i.object_id for i in tagged_items]

        if "q" in filters:
            user = User.objects.get(username=filters["username"])
            sqs = SearchQuerySet().filter(author=user, content=filters["q"])
            orm_filters["pk__in"] = [i.pk for i in sqs]

        return orm_filters

    def save_m2m(self, bundle):
        tags = bundle.data.get("tags_list", [])
        if tags != "":
            bundle.obj.tags.set(*parse_tags(tags))
        else:
            bundle.obj.tags.set()


class PrivateFavoriteResource(ModelResource):
    user = fields.ForeignKey(PrivateUserResource, "user", full=True)
    snipt = fields.ForeignKey(PrivateSniptResource, "snipt", full=False)

    class Meta:
        queryset = Favorite.objects.all().order_by("-created")
        resource_name = "favorite"
        fields = ["id"]
        validation = FavoriteValidation()
        detail_allowed_methods = ["get", "post", "delete"]
        list_allowed_methods = ["get", "post"]
        authentication = ApiKeyAuthentication()
        authorization = PrivateFavoriteAuthorization()
        ordering = ["created"]
        always_return_data = True
        max_limit = 200
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data["snipt"] = "/api/public/snipt/{}/".format(bundle.obj.snipt.pk)
        return bundle

    def obj_create(self, bundle, **kwargs):
        bundle.data["user"] = bundle.request.user
        bundle.data["snipt"] = Snipt.objects.get(pk=bundle.data["snipt"])
        return super(PrivateFavoriteResource, self).obj_create(
            bundle, user=bundle.request.user, **kwargs
        )
