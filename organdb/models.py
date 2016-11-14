from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='nazwa')
    description = models.TextField(verbose_name='opis')

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regiony"
        ordering = ['name']

    def __str__(self):
        return 'Region: {}'.format(self.name)


class City(models.Model):
    name = models.CharField(max_length=30, verbose_name='nazwa')
    description = models.TextField(verbose_name='opis')
    region = models.ForeignKey(Region, verbose_name='region')

    class Meta:
        verbose_name = "miejscowość"
        verbose_name_plural = "miejscowości"
        ordering = ['name']

    def __str__(self):
        return 'Miejscowość: {}'.format(self.name)


class Location(models.Model):
    name = models.CharField(max_length=50, verbose_name='nazwa')
    address = models.CharField(max_length=100, verbose_name='adres')
    city = models.ForeignKey(City, verbose_name='miejscowość')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='szerokość geograficzna')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='długość geograficzna')

    class Meta:
        verbose_name = "lokacja"
        verbose_name_plural = "lokacje"

    def __str__(self):
        return 'Lokacja: {}, {}'.format(self.name, self.city.name)


class Builder(models.Model):
    name = models.CharField(max_length=40, verbose_name='imię i nazwisko')
    biography = models.TextField(verbose_name='biografia')
    born = models.DateField(blank=True, null=True, verbose_name='data urodzenia')
    died = models.DateField(blank=True, null=True, verbose_name='data śmierci')

    class Meta:
        verbose_name = "organmistrz"
        verbose_name_plural = "organmistrzowie"

    def __str__(self):
        return 'Organmistrz: {}'.format(self.name)


class Instrument(models.Model):
    build_date = models.DateField(verbose_name='data budowy')
    comment = models.TextField(blank=True, null=True, verbose_name='komentarz')
    key_action = models.CharField(max_length=20, verbose_name='traktura gry')
    stop_action = models.CharField(max_length=20, verbose_name='traktura rejestrów')
    stops = models.IntegerField(verbose_name='liczba głosów')
    keyboards = models.IntegerField(verbose_name='liczba klawiatur')
    pedalboard = models.BooleanField(verbose_name='pedał')
    description = models.TextField(verbose_name='opis')
    additional_features = models.TextField(verbose_name='dodatkowe urządzenia')
    builder = models.ForeignKey(Builder, blank=True, null=True, verbose_name='budowniczy')
    location = models.ForeignKey(Location, verbose_name='lokacja')
    published = models.BooleanField(verbose_name='opublikowane')

    class Meta:
        verbose_name = "instrument"
        verbose_name_plural = "instrumenty"

    def __str__(self):
        return 'Instrument: {}, {} ({})'.format(self.location.city.name, self.location.name, self.comment)


class Keyboard(models.Model):
    name = models.CharField(max_length=30, verbose_name='nazwa')
    pedalboard = models.BooleanField(verbose_name='pedał')
    min_note = models.CharField(max_length=2, blank=True, null=True, verbose_name='najniższy dźwięk')
    max_note = models.CharField(max_length=2, blank=True, null=True, verbose_name='najwyższy dźwięk')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')
    order = models.IntegerField(verbose_name='kolejność sortowania')

    class Meta:
        verbose_name = "klawiatura"
        verbose_name_plural = "klawiatury"
        ordering = ['order']

    def __str__(self):
        return 'Klawiatura: {} ({}, {})'.format(self.name, self.instrument.location.name,
                                                self.instrument.location.city.name)


class StopFamily(models.Model):
    name = models.CharField(max_length=30, verbose_name='nazwa')
    description = models.TextField(verbose_name='opis')

    class Meta:
        verbose_name = "rodzina głosów"
        verbose_name_plural = "rodziny głosów"

    def __str__(self):
        return 'Rodzina głosów: {}'.format(self.name)


class StopType(models.Model):
    name = models.CharField(max_length=30, verbose_name='nazwa')
    description = models.TextField(verbose_name='opis')
    families = models.ManyToManyField(StopFamily, blank=True, verbose_name='rodziny głosu')

    class Meta:
        verbose_name = "typ głosu"
        verbose_name_plural = "typy głosów"

    def __str__(self):
        return 'Typ głosu: {}'.format(self.name)


class Stop(models.Model):
    number = models.IntegerField(verbose_name='numer')
    name = models.CharField(max_length=30, verbose_name='nazwa')
    length = models.CharField(max_length=5, blank=True, null=True, verbose_name='długość piszczałki')
    reed = models.BooleanField(verbose_name='głos językowy')
    keyboard = models.ForeignKey(Keyboard, verbose_name='klawiatura')
    type = models.ForeignKey(StopType, verbose_name='typ głosu')

    class Meta:
        verbose_name = "głos"
        verbose_name_plural = "głosy"
        ordering = ['number']

    def __str__(self):
        return '{}, {} - {} - {}. {} {}\''.format(self.keyboard.instrument.location.name,
                                                  self.keyboard.instrument.location.city.name,
                                                  self.keyboard.name, self.number, self.name, self.length)


class Sample(models.Model):
    file = models.FileField(upload_to='samples/', verbose_name='plik')
    description = models.TextField(verbose_name='opis')
    stop_type = models.ForeignKey(StopType, verbose_name='typ głosu')

    class Meta:
        verbose_name = "próbka"
        verbose_name_plural = "próbki"

    def __str__(self):
        return 'Próbka #{} ({})'.format(self.id, self.stop_type.name)


class Work(models.Model):
    type = models.CharField(max_length=60, verbose_name='rodzaj prac')
    year = models.IntegerField(verbose_name='rok')
    description = models.TextField(verbose_name='opis')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')
    builder = models.ForeignKey(Builder, verbose_name='organmistrz')

    class Meta:
        verbose_name = "praca"
        verbose_name_plural = "prace"

    def __str__(self):
        return 'Praca organmistrza {} przy {}, {} ({})'.format(self.builder.name, self.instrument.location.name,
                                                               self.instrument.location.city.name, self.year)


class Performer(models.Model):
    name = models.CharField(max_length=40, verbose_name='imię i nazwisko')
    born = models.DateField(blank=True, null=True, verbose_name='data urodzenia')
    died = models.DateField(blank=True, null=True, verbose_name='data śmierci')
    biography = models.TextField(verbose_name='biografia')
    photo = models.ImageField(blank=True, null=True, verbose_name='zdjęcie')

    class Meta:
        verbose_name = "wykonawca"
        verbose_name_plural = "wykonawcy"

    def __str__(self):
        return 'Wykonawca: {}'.format(self.name)


class Recording(models.Model):
    file = models.FileField(upload_to='recordings/', verbose_name='plik')
    description = models.TextField(verbose_name='opis')
    performer = models.ForeignKey(Performer, verbose_name='wykonawca')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')

    class Meta:
        verbose_name = "nagranie"
        verbose_name_plural = "nagrania"

    def __str__(self):
        return 'Nagranie: {}, wyk. {}'.format(self.description, self.performer.name)


class Concert(models.Model):
    name = models.CharField(max_length=30, verbose_name='nazwa')
    date = models.DateField(verbose_name='data')
    description = models.TextField(verbose_name='opis')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')
    performers = models.ManyToManyField(Performer, verbose_name='wykonawcy')

    class Meta:
        verbose_name = "koncert"
        verbose_name_plural = "koncerty"

    def __str__(self):
        return 'Koncert: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name, self.date)


class Photo(models.Model):
    file = models.ImageField(verbose_name='plik')
    description = models.TextField(verbose_name='opis')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')

    class Meta:
        verbose_name = "zdjęcie"
        verbose_name_plural = "zdjęcia"

    def __str__(self):
        return 'Zdjęcie: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name, self.description)
