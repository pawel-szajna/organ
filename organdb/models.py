from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    def __str__(self):
        return 'Region: {}'.format(self.name)


class City(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    region = models.ForeignKey(Region)

    def __str__(self):
        return 'City: {}'.format(self.name)


class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.ForeignKey(City)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return 'Location: {}, {}'.format(self.name, self.city.name)


class Builder(models.Model):
    name = models.CharField(max_length=40)
    biography = models.TextField()
    born = models.DateField(blank=True, null=True)
    died = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Builder: {}'.format(self.name)


class Instrument(models.Model):
    build_date = models.DateField()
    key_action = models.CharField(max_length=20)
    stop_action = models.CharField(max_length=20)
    stops = models.IntegerField()
    keyboards = models.IntegerField()
    pedalboard = models.BooleanField()
    description = models.TextField()
    additional_features = models.TextField()
    builder = models.ForeignKey(Builder)
    location = models.ForeignKey(Location)
    published = models.BooleanField()

    def __str__(self):
        return 'Instrument: {}'.format(self.location)


class Keyboard(models.Model):
    class Meta:
        ordering = ['order']
    name = models.CharField(max_length=30)
    pedalboard = models.BooleanField()
    min_note = models.CharField(max_length=2)
    max_note = models.CharField(max_length=2)
    instrument = models.ForeignKey(Instrument)
    order = models.IntegerField()

    def __str__(self):
        return 'Keyboard: {} ({}, {})'.format(self.name, self.instrument.location.name,
                                              self.instrument.location.city.name)


class StopType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return 'Stop type: {}'.format(self.name)


class StopFamily(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return 'Stop family: {}'.format(self.name)


class Stop(models.Model):
    class Meta:
        ordering = ['number']
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    length = models.CharField(max_length=5, blank=True, null=True)
    reed = models.BooleanField()
    keyboard = models.ForeignKey(Keyboard)
    type = models.ForeignKey(StopType)

    def __str__(self):
        return '{}, {} - {} - {}. {} {}\''.format(self.keyboard.instrument.location.name,
                                                  self.keyboard.instrument.location.city.name,
                                                  self.keyboard.name, self.number, self.name, self.length)


class Sample(models.Model):
    file = models.FileField(upload_to='samples/')
    description = models.TextField()
    stop_type = models.ForeignKey(StopType)

    def __str__(self):
        return 'Sample #{} ({})'.format(self.id, self.stop_type.name)


class Work(models.Model):
    type = models.CharField(max_length=60)
    year = models.IntegerField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)
    builder = models.ForeignKey(Builder)

    def __str__(self):
        return 'Work by {} on {}, {} ({})'.format(self.builder.name, self.instrument.location.name,
                                                  self.instrument.location.city.name, self.year)


class Performer(models.Model):
    name = models.CharField(max_length=40)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)
    biography = models.TextField()
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return 'Performer: {}'.format(self.name)


class Recording(models.Model):
    file = models.FileField(upload_to='recordings/')
    description = models.TextField()
    performer = models.ForeignKey(Performer)
    instrument = models.ForeignKey(Instrument)


class Concert(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)


class Photo(models.Model):
    file = models.ImageField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)

    def __str__(self):
        return 'Photo: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name, self.description)


class Performance(models.Model):
    concert = models.ForeignKey(Concert)
    performer = models.ForeignKey(Performer)


class StopMembership(models.Model):
    type = models.ForeignKey(StopType)
    family = models.ForeignKey(StopFamily)
