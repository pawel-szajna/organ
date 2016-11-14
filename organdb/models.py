from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regiony"
        ordering = ['name']

    def __str__(self):
        return 'Region: {}'.format(self.name)


class City(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    region = models.ForeignKey(Region)

    class Meta:
        verbose_name = "miejscowość"
        verbose_name_plural = "miejscowości"
        ordering = ['name']

    def __str__(self):
        return 'Miejscowość: {}'.format(self.name)


class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.ForeignKey(City)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        verbose_name = "lokacja"
        verbose_name_plural = "lokacje"

    def __str__(self):
        return 'Lokacja: {}, {}'.format(self.name, self.city.name)


class Builder(models.Model):
    name = models.CharField(max_length=40)
    biography = models.TextField()
    born = models.DateField(blank=True, null=True)
    died = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "organmistrz"
        verbose_name_plural = "organmistrzowie"

    def __str__(self):
        return 'Organmistrz: {}'.format(self.name)


class Instrument(models.Model):
    build_date = models.DateField()
    comment = models.TextField(blank=True, null=True)
    key_action = models.CharField(max_length=20)
    stop_action = models.CharField(max_length=20)
    stops = models.IntegerField()
    keyboards = models.IntegerField()
    pedalboard = models.BooleanField()
    description = models.TextField()
    additional_features = models.TextField()
    builder = models.ForeignKey(Builder, blank=True, null=True)
    location = models.ForeignKey(Location)
    published = models.BooleanField()

    class Meta:
        verbose_name = "instrument"
        verbose_name_plural = "instrumenty"

    def __str__(self):
        return 'Instrument: {}, {} ({})'.format(self.location.city.name, self.location.name, self.comment)


class Keyboard(models.Model):
    name = models.CharField(max_length=30)
    pedalboard = models.BooleanField()
    min_note = models.CharField(max_length=2)
    max_note = models.CharField(max_length=2)
    instrument = models.ForeignKey(Instrument)
    order = models.IntegerField()

    class Meta:
        verbose_name = "klawiatura"
        verbose_name_plural = "klawiatury"
        ordering = ['order']

    def __str__(self):
        return 'Klawiatura: {} ({}, {})'.format(self.name, self.instrument.location.name,
                                                self.instrument.location.city.name)


class StopType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "typ głosu"
        verbose_name_plural = "typy głosów"

    def __str__(self):
        return 'Typ głosu: {}'.format(self.name)


class StopFamily(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "rodzina głosów"
        verbose_name_plural = "rodziny głosów"

    def __str__(self):
        return 'Rodzina głosów: {}'.format(self.name)


class Stop(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    length = models.CharField(max_length=5, blank=True, null=True)
    reed = models.BooleanField()
    keyboard = models.ForeignKey(Keyboard)
    type = models.ForeignKey(StopType)

    class Meta:
        verbose_name = "głos"
        verbose_name_plural = "głosy"
        ordering = ['number']

    def __str__(self):
        return '{}, {} - {} - {}. {} {}\''.format(self.keyboard.instrument.location.name,
                                                  self.keyboard.instrument.location.city.name,
                                                  self.keyboard.name, self.number, self.name, self.length)


class Sample(models.Model):
    file = models.FileField(upload_to='samples/')
    description = models.TextField()
    stop_type = models.ForeignKey(StopType)

    class Meta:
        verbose_name = "próbka"
        verbose_name_plural = "próbki"

    def __str__(self):
        return 'Próbka #{} ({})'.format(self.id, self.stop_type.name)


class Work(models.Model):
    type = models.CharField(max_length=60)
    year = models.IntegerField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)
    builder = models.ForeignKey(Builder)

    class Meta:
        verbose_name = "praca"
        verbose_name_plural = "prace"

    def __str__(self):
        return 'Praca organmistrza {} przy {}, {} ({})'.format(self.builder.name, self.instrument.location.name,
                                                               self.instrument.location.city.name, self.year)


class Performer(models.Model):
    name = models.CharField(max_length=40)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)
    biography = models.TextField()
    photo = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = "wykonawca"
        verbose_name_plural = "wykonawcy"

    def __str__(self):
        return 'Wykonawca: {}'.format(self.name)


class Recording(models.Model):
    file = models.FileField(upload_to='recordings/')
    description = models.TextField()
    performer = models.ForeignKey(Performer)
    instrument = models.ForeignKey(Instrument)

    class Meta:
        verbose_name = "nagranie"
        verbose_name_plural = "nagrania"

    def __str__(self):
        return 'Nagranie: {}, wyk. {}'.format(self.description, self.performer.name)


class Concert(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)

    class Meta:
        verbose_name = "koncert"
        verbose_name_plural = "koncerty"

    def __str__(self):
        return 'Koncert: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name, self.date)


class Photo(models.Model):
    file = models.ImageField()
    description = models.TextField()
    instrument = models.ForeignKey(Instrument)

    class Meta:
        verbose_name = "zdjęcie"
        verbose_name_plural = "zdjęcia"

    def __str__(self):
        return 'Zdjęcie: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name, self.description)


class Performance(models.Model):
    concert = models.ForeignKey(Concert)
    performer = models.ForeignKey(Performer)

    class Meta:
        verbose_name = "występ"
        verbose_name_plural = "występy"

    def __str__(self):
        return 'Występ {} w {}'.format(self.performer.name, self.concert)


class StopMembership(models.Model):
    type = models.ForeignKey(StopType)
    family = models.ForeignKey(StopFamily)

    class Meta:
        verbose_name = "przynależność głosu"
        verbose_name_plural = "przynależności głosów"

    def __str__(self):
        return 'Przynależność głosu {} do rodziny {}'.format(self.type.name, self.family.name)
