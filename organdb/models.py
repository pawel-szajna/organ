from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()


class City(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    region = models.ForeignKey(Region)


class Location(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Builder(models.Model):
    name = models.CharField(max_length=40)
    biography = models.TextField()
    born = models.DateField()
    died = models.DateField()


class Keyboard(models.Model):
    name = models.CharField(max_length=30)
    pedalboard = models.BooleanField()
    min_note = models.CharField(max_length=2)
    max_note = models.CharField(max_length=2)
    order = models.IntegerField()


class StopType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()


class StopFamily(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()


class Stop(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    length = models.CharField(max_length=5)
    reed = models.BooleanField()
    keyboard = models.ForeignKey(Keyboard)
    type = models.ForeignKey(StopType)


class Sample(models.Model):
    file = models.FileField(upload_to='samples/')
    description = models.TextField()


class Instrument(models.Model):
    build_date = models.DateField()
    key_action = models.CharField(max_length=20)
    stop_action = models.CharField(max_length=20)
    stops = models.IntegerField()
    keyboards = models.IntegerField()
    pedalboard = models.BooleanField()
    description = models.TextField()
    builder = models.ForeignKey(Builder)
    published = models.BooleanField()


class Work(models.Model):
    type = models.CharField(max_length=60)
    year = models.IntegerField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)
    builder = models.ForeignKey(Builder)


class Performer(models.Model):
    name = models.CharField(max_length=40)
    born = models.DateField()
    died = models.DateField()
    biography = models.TextField()
    photo = models.ImageField()


class Recording(models.Model):
    file = models.FileField(upload_to='recordings/')
    description = models.TextField()
    performer = models.ForeignKey(Performer)
    instrument = models.ForeignKey(Instrument)


class Concert(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)


class Photo(models.Model):
    file = models.ImageField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)


class Performance(models.Model):
    concert = models.ForeignKey(Concert)
    performer = models.ForeignKey(Performer)


class StopMembership(models.Model):
    type = models.ForeignKey(StopType)
    family = models.ForeignKey(StopFamily)
