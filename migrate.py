#!/usr/bin/python

import MySQLdb

from django.contrib.auth.models import User

from snipts.models import Comment, Snipt

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='sniptold')
cursor = conn.cursor()

def i():
    users()
    snipts()
    comments()

def users():

    print "Deleting existing users"
    users = User.objects.all()
    for u in users:
        u.delete()

    cursor.execute("SELECT * FROM auth_user")
    rows = cursor.fetchall()

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
        user.save()

    print 'Done with users'

def snipts():

    print "Deleting existing snipts"
    snipts = Snipt.objects.all()
    for s in snipts:
        s.delete()

    cursor.execute("SELECT * FROM snippet_snippet")
    rows = cursor.fetchall()

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

        snipt = Snipt(
            id=snipt_id,
            code=code,
            title=title,
            slug=slug,
            lexer=lexer,
            key=key,
            user=User.objects.get(id=user_id),
            tags=tags,
            public=public,
            created=created,
        )
        snipt.save()

    print 'Done with snipts'

def comments():

    print "Deleting existing comments"
    comments = Comment.objects.all()
    for c in comments:
        c.delete()

    cursor.execute("SELECT * FROM django_comments")
    rows = cursor.fetchall()

    for row in rows:
        snipt_id = row[2]
        user_id = row[4]
        cmt = row[8]
        created = row[9]

        try:
            comment = Comment(
                snipt=Snipt.objects.get(id=snipt_id),
                user=User.objects.get(id=user_id),
                comment=cmt,
                created=created,
            )
            comment.save()
        except:
            print "Couldn't get snipt " + str(snipt_id)

    print 'Done with comments'
