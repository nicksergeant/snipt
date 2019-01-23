from django.contrib.auth.models import User
from snipts.models import Snipt
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase


class SniptResourceTest(ResourceTestCase):
    fixtures = ["test_entries.json"]

    def setUp(self):
        super(SniptResourceTest, self).setUp()

        # Johnny
        self.johnny = User.objects.create_user(
            "johnny", "johnny@siftie.com", "password"
        )
        ApiKey.objects.get_or_create(user=self.johnny)
        self.johnny_auth = self.create_apikey(self.johnny, self.johnny.api_key.key)
        self.johnny_private = Snipt(
            title="Private snippet for Johnny",
            lexer="text",
            public=False,
            user=self.johnny,
        )
        self.johnny_public = Snipt(
            title="Public snippet for Johnny",
            lexer="text",
            public=True,
            user=self.johnny,
        )
        self.johnny_private.save()
        self.johnny_public.save()

        # Bob
        self.bob = User.objects.create_user("bob", "bob@siftie.com", "password")
        ApiKey.objects.get_or_create(user=self.bob)
        self.bob_auth = self.create_apikey(self.bob, self.bob.api_key.key)
        self.bob_private = Snipt(
            title="Private snippet for Bob", lexer="text", public=False, user=self.bob
        )
        self.bob_public = Snipt(
            title="Public snippet for Bob", lexer="text", public=True, user=self.bob
        )
        self.bob_private.save()
        self.bob_public.save()

    def test_get_private_list(self):

        resp = self.api_client.get(
            "/api/private/snipt/", format="json", authentication=self.johnny_auth
        )

        self.assertHttpOK(resp)
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)["objects"]), 2)

    def test_get_private_detail(self):

        resp = self.api_client.get(
            "/api/private/snipt/{}/".format(self.johnny_private.pk),
            format="json",
            authentication=self.johnny_auth,
        )

        self.assertHttpOK(resp)
        self.assertValidJSONResponse(resp)
        self.assertEqual(self.deserialize(resp)["key"], self.johnny_private.key)

        # Unauthenticated request.
        resp = self.api_client.get(
            "/api/private/snipt/{}/".format(self.johnny_private.pk), format="json"
        )
        self.assertHttpUnauthorized(resp)

        # Unauthorized request.
        resp = self.api_client.get(
            "/api/private/snipt/{}/".format(self.johnny_private.pk),
            format="json",
            authentication=self.bob_auth,
        )
        self.assertHttpUnauthorized(resp)

    def test_post_private_list(self):

        new_snipt = {
            "title": "A new private snippet.",
            "lexer": "text",
            "public": False,
        }

        resp = self.api_client.post(
            "/api/private/snipt/",
            data=new_snipt,
            format="json",
            authentication=self.johnny_auth,
        )

        self.assertHttpCreated(resp)
        self.assertEqual(Snipt.objects.count(), 5)

        resp = self.api_client.get(
            "/api/private/snipt/", format="json", authentication=self.johnny_auth
        )
        self.assertEqual(len(self.deserialize(resp)["objects"]), 3)

        resp = self.api_client.get("/api/public/snipt/", format="json")
        self.assertEqual(len(self.deserialize(resp)["objects"]), 2)

    def test_get_public_list(self):

        self.assertEqual(Snipt.objects.count(), 4)

        resp = self.api_client.get("/api/public/snipt/", format="json")

        self.assertHttpOK(resp)
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)["objects"]), 2)
