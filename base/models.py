import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from .managers import MemberManager


'''
    Member: Class representing NA members.
    Also used as the Django Auth user class.
'''


class Member(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True,
                             primary_key=True,
                             serialize=False,
                             verbose_name='ID')
    # Mandatory Fields
    username = models.CharField(unique=True,
                                blank=False,
                                max_length=254)
    password = models.CharField(max_length=254)

    #
    email = models.EmailField(unique=True,
                              blank=True,
                              null=True,
                              default=None)
    first_name = models.CharField(max_length=127,
                                  blank=True,
                                  null=True,
                                  default=None)
    last_name = models.CharField(max_length=254,
                                 blank=True,
                                 null=True,
                                 default=None)
    mobile_number = PhoneNumberField(unique=True,
                                     blank=True,
                                     null=True,
                                     default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_specialworker = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.datetime.now,
                                       verbose_name='date joined')
    last_login = models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name='last login')

    USERNAME_FIELD = 'username'

    objects = MemberManager()


'''Group: the base NA group.'''


class NAGroup(models.Model):
    name = models.CharField(max_length=256,
                            primary_key=True)
    # authorizes = models.ManyToManyField('self',
    #                                     blank=True)

    # XA positions
    secretary = models.ForeignKey(Member,
                                  models.SET_NULL,
                                  related_name='secretary_user',
                                  null=True,
                                  blank=True)
    treasurer = models.ForeignKey(Member,
                                  models.SET_NULL,
                                  related_name='treasurer_user',
                                  null=True,
                                  blank=True)
    service_rep = models.ForeignKey(Member,
                                    models.SET_NULL,
                                    related_name='ser_user',
                                    null=True,
                                    blank=True)


'''Codes: NA Recovery Meeting Codes.'''


class Codes(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)


'''Address: US Based Meeting Site Address'''


class Address(models.Model):
    street = models.CharField(max_length=256)
    specific = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = USStateField()
    zipcode = USZipCodeField()


# TODO class Location
# class Location(models.Model):
#     address = models.ForeignKey(Address,
#                                 on_delete=models.CASCADE)
#     lat = models.FloatField()
#     lon = models.FloatField()


'''NB: A meeting is defined by single weekly or greater recurrence.'''


class MeetingTime(models.Model):
    MON = 0
    TUE = 1
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7
    DAYS_OF_WEEK = [
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
        (SAT, 'Saturday'),
        (SUN, 'Sunday'),
    ]

    dow = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField(default=datetime.time(hour=18))
    dur = models.DurationField(default=datetime.timedelta(hours=1))
    # TODO: location = models.ForeignKey('Location', on_delete=models.PROTECT)
    addr = models.ForeignKey('Address',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)


class Meeting(models.Model):
    # The group name is usually the meeting name. If this group has multiple meetings with different names,
    # use the name field.
    group = models.ForeignKey(NAGroup,
                              on_delete=models.PROTECT)
    # name = models.CharField(max_length=256, default=None, blank=False)
    time = models.ForeignKey('MeetingTime',
                             on_delete=models.CASCADE,
                             blank=False)
    addr = models.ForeignKey('Address',
                             on_delete=models.PROTECT,
                             blank=False)
    codes = models.ManyToManyField(Codes)
