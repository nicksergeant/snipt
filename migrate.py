#!/usr/bin/python

from django.utils.encoding import force_unicode

import MySQLdb

from django.contrib.auth.models import User

from snipts.models import Favorite, Snipt
from taggit.models import Tag
from tastypie.models import ApiKey 

conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='sniptold')
cursor = conn.cursor()

def i():
    users()
    create_api_keys()
    snipts()
    favs()

def users():

    print "Deleting existing users"
    users = User.objects.all()
    for u in users:
        u.delete()

    cursor.execute("SELECT * FROM auth_user")
    rows = cursor.fetchall()

    print "Adding users"

    for row in rows:
        user_id      = row[0]
        username     = row[1]
        first_name   = row[2]
        last_name    = row[3]
        email        = row[4]
        password     = row[5]
        is_staff     = row[6]
        is_active    = row[7]
        is_superuser = row[8]
        last_login   = row[9]
        date_joined  = row[10]

        user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=last_login,
            date_joined=date_joined,
        )

        print 'Saving user ' + user.username
        user.save()

    print "Done with users"

def snipts():

    print "Deleting existing snipts"
    snipts = Snipt.objects.all()
    for s in snipts:
        s.delete()

    print "Deleting existing tags"
    existing_tags = Tag.objects.all()
    existing_tagged_items = Tag.objects.all()

    for t in existing_tags:
        t.delete()

    for t in existing_tagged_items:
        t.delete()

    cursor.execute("SELECT * FROM snippet_snippet")
    rows = cursor.fetchall()

    print "Adding snipts"

    for row in rows:
        snipt_id = row[0]
        code     = row[1]
        title    = row[2]
        created  = row[3]
        user_id  = row[4]
        tags     = row[5]
        lexer    = row[6]
        public   = row[7]
        key      = row[8]
        slug     = row[9]

        title = title[:255]

        snipt = Snipt(
            id=snipt_id,
            code=code,
            title=title,
            slug=slug,
            lexer=lexer,
            key=key,
            user=User.objects.get(id=user_id),
            public=public,
            created=created,
            modified=created,
        )
        for t in parse_tag_input(tags):
            snipt.tags.add(t)

        print 'Saving snipt ' + snipt.title
        snipt.save()

    print 'Done with snipts'

def favs():

    print "Deleting existing favorites"
    favs = Favorite.objects.all()
    for f in favs:
        f.delete()

    cursor.execute("SELECT * FROM favsnipt_favsnipt")
    rows = cursor.fetchall()

    print "Adding favorites"

    for row in rows:
        fav_id   = row[0]
        snipt_id = row[1]
        user_id  = row[2]
        created  = row[3]

        fav = Favorite(
            id=fav_id,
            snipt_id=snipt_id,
            user_id=user_id,
            created=created,
            modified=created,
        )
        print 'Saving favorite ' + str(fav.id)
        fav.save()

    print 'Done with favorites'

def parse_tag_input(input):
    """
    Parses tag input, with multiple word input being activated and
    delineated by commas and double quotes. Quotes take precedence, so
    they may contain commas.

    Returns a sorted list of unique tag names.
    """
    if not input:
        return []

    input = force_unicode(input)

    # Special case - if there are no commas or double quotes in the
    # input, we don't *do* a recall... I mean, we know we only need to
    # split on spaces.
    if u',' not in input and u'"' not in input:
        words = list(set(split_strip(input, u' ')))
        words.sort()
        return words

    words = []
    buffer = []
    # Defer splitting of non-quoted sections until we know if there are
    # any unquoted commas.
    to_be_split = []
    saw_loose_comma = False
    open_quote = False
    i = iter(input)
    try:
        while 1:
            c = i.next()
            if c == u'"':
                if buffer:
                    to_be_split.append(u''.join(buffer))
                    buffer = []
                # Find the matching quote
                open_quote = True
                c = i.next()
                while c != u'"':
                    buffer.append(c)
                    c = i.next()
                if buffer:
                    word = u''.join(buffer).strip()
                    if word:
                        words.append(word)
                    buffer = []
                open_quote = False
            else:
                if not saw_loose_comma and c == u',':
                    saw_loose_comma = True
                buffer.append(c)
    except StopIteration:
        # If we were parsing an open quote which was never closed treat
        # the buffer as unquoted.
        if buffer:
            if open_quote and u',' in buffer:
                saw_loose_comma = True
            to_be_split.append(u''.join(buffer))
    if to_be_split:
        if saw_loose_comma:
            delimiter = u','
        else:
            delimiter = u' '
        for chunk in to_be_split:
            words.extend(split_strip(chunk, delimiter))
    words = list(set(words))
    words.sort()
    return words

def split_strip(input, delimiter=u','):
    """
    Splits ``input`` on ``delimiter``, stripping each resulting string
    and returning a list of non-empty strings.
    """
    if not input:
        return []

    words = [w.strip() for w in input.split(delimiter)]
    return [w for w in words if w]

def create_api_keys():
    for user in User.objects.all(): 
            ApiKey.objects.create(user=user)
