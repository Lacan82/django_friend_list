# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt
from django.db import models
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    # def books_reviewed(self):
    #     return self.model.reviews_left.all().values('book').distict()

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('name fields must be letter characters only')
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in name used")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")
        if re.search(r"[!@$&{1,5}]", post_data['password']) is None:
            errors.append("Password should contain one of !@$&")
        try:
            datetime.datetime.strptime(post_data['dob'], '%Y-%m-%d').date()
        except ValueError:
            errors.append("Please enter a valid birthday")
        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                alias=post_data['alias'],
                email=post_data['email'],
                dob=post_data['dob'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    objects = UserManager()

    def __str__(self):
        return self.email


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='Owner')

    @classmethod
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        print new_friend
        friend.users.add(new_friend)
        # Creates a symmetrical relationship
        friend, created = cls.objects.get_or_create(
            current_user=new_friend)
        friend.users.add(current_user)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
        # Removes the symmetrical relationship
        friend, created = cls.objects.get_or_create(
            current_user=new_friend)
        friend.users.remove(current_user)
