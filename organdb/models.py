from django_markdown.models import MarkdownField
from django.db import models


class Region(models.Model):
    """
    A region which groups cities.
    """
    name = models.CharField(max_length=30, unique=True, verbose_name='nazwa')

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regiony'
        ordering = ['name']

    def __str__(self):
        return 'Województwo {}'.format(self.name)


class City(models.Model):
    """
    A city, belonging to a region, which groups locations.
    """
    name = models.CharField(max_length=30, verbose_name='nazwa')
    region = models.ForeignKey(Region, verbose_name='region')

    class Meta:
        verbose_name = 'miejscowość'
        verbose_name_plural = 'miejscowości'
        ordering = ['region', 'name']

    def __str__(self):
        return '{}, {}'.format(self.name, self.region.name)


class Location(models.Model):
    """
    A location, belonging to a city, which can be home of any number (but usually one) instrument. A location
    is associated with an address and, optionally, coordinates for Google Maps map display.
    """
    name = models.CharField(max_length=70, verbose_name='nazwa')
    address = models.CharField(max_length=100, verbose_name='adres')
    city = models.ForeignKey(City, verbose_name='miejscowość')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                   verbose_name='szerokość geograficzna')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                    verbose_name='długość geograficzna')

    class Meta:
        verbose_name = 'lokalizacja'
        verbose_name_plural = 'lokalizacje'
        ordering = ['city', 'name']

    def __str__(self):
        return '{}, {}'.format(self.name, self.city.name)


class Builder(models.Model):
    """
    An organ builder who can be either set as a specific instrument's builder or as the person responsible for
    some work done on an instrument.
    """
    name = models.CharField(max_length=40, verbose_name='nazwisko')
    first_name = models.CharField(blank=True, null=True, max_length=40, verbose_name='imię')
    biography = MarkdownField(verbose_name='biografia')
    born = models.DateField(blank=True, null=True, verbose_name='data urodzenia')
    died = models.DateField(blank=True, null=True, verbose_name='data śmierci')

    class Meta:
        verbose_name = 'organmistrz'
        verbose_name_plural = 'organmistrzowie'
        ordering = ['name', 'first_name']

    def __str__(self):
        return self.name


class Instrument(models.Model):
    """
    An instrument. This model represents a single instrument and contains information about its basic properties,
    such as build date, action, number of keyboards etc. A comment field is provided for the option to differentiate
    several instruments in the same location.
    """
    ACTION_CHOICES = [
        ('mechaniczna', 'mechaniczna'),
        ('pneumatyczna', 'pneumatyczna'),
        ('elektro-pneumatyczna', 'elektro-pneumatyczna'),
        ('elektryczna', 'elektryczna'),
    ]

    build_date = models.IntegerField(blank=True, null=True, verbose_name='rok budowy')
    comment = models.CharField(max_length=80, blank=True, null=True, verbose_name='komentarz',
                               help_text='Wykorzystywany do rozróżnienia kilku instrumentów znajudjących się '
                                         'w tej samej lokalizacji.')
    key_action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='traktura gry')
    stop_action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='traktura rejestrów')
    stops = models.IntegerField(verbose_name='głosy',
                                help_text='Liczba głosów w instrumencie (bez uwzględnienia urządzeń takich jak '
                                          'połączenia, termolo).')
    keyboards = models.IntegerField(verbose_name='manuały', help_text='Liczba manuałów w insturmencie.')
    pedalboard = models.BooleanField(verbose_name='pedał')
    description = MarkdownField(verbose_name='opis')
    additional_features = models.TextField(blank=True, null=True, verbose_name='dodatkowe urządzenia',
                                           help_text='Opis dodatkowych urządzeń (wolne kombinacje, połączenia itp.).')
    builder = models.ForeignKey(Builder, blank=True, null=True, verbose_name='budowniczy')
    location = models.ForeignKey(Location, verbose_name='lokalizacji')

    class Meta:
        verbose_name = 'instrument'
        verbose_name_plural = 'instrumenty'
        ordering = ['location', '-stops']

    def __str__(self):
        return '{}, {} ({})'.format(self.location.city.name, self.location.name, self.comment)

    def region_name(self):
        return self.location.city.region.name

    region_name.short_description = 'województwo'


class Keyboard(models.Model):
    """
    A keyboard belonging to a specific instrument.
    """
    name = models.CharField(max_length=30, verbose_name='nazwa')
    numbered = models.BooleanField(verbose_name='głosy numerowane',
                                   help_text='Określa, czy numery głosów w tej klawiaturze są prezentowane na stronie '
                                             'instrumentu. Niezależnie od ustawienia, głosy posortowane sa według '
                                             'numeru głosu.')
    min_note = models.CharField(max_length=2, blank=True, null=True, verbose_name='najniższy dźwięk')
    max_note = models.CharField(max_length=2, blank=True, null=True, verbose_name='najwyższy dźwięk')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')
    order = models.IntegerField(verbose_name='kolejność sortowania',
                                help_text='Klawiatury danego instrumentu wyświetlane są według rosnących wartości '
                                          'tego pola.')

    class Meta:
        verbose_name = 'klawiatura'
        verbose_name_plural = 'klawiatury'
        ordering = ['order']

    def __str__(self):
        return '{} ({}, {})'.format(self.name, self.instrument.location.name,
                                    self.instrument.location.city.name)


class StopFamily(models.Model):
    """
    A stop family is used as a kind of tagging system for stop types.
    """
    name = models.CharField(max_length=30, verbose_name='nazwa')
    description = MarkdownField(verbose_name='opis')

    class Meta:
        verbose_name = 'rodzina głosów'
        verbose_name_plural = 'rodziny głosów'
        ordering = ['name']

    def __str__(self):
        return self.name

    def stop_types(self):
        return self.stoptype_set.count()

    stop_types.short_description = 'typy głosów'


class StopType(models.Model):
    """
    A stop type is an entry in stop library. A stop type can belong to any number of stop families.
    """
    name = models.CharField(max_length=30, verbose_name='nazwa')
    description = MarkdownField(verbose_name='opis')
    families = models.ManyToManyField(StopFamily, blank=True, verbose_name='rodziny głosu')

    class Meta:
        verbose_name = 'typ głosu'
        verbose_name_plural = 'typy głosów'
        ordering = ['name']

    def __str__(self):
        return self.name


class Stop(models.Model):
    """
    A stop from a specific instrument. The stop is assigned to a specific keyboard and belongs to a specific
    stop type (so that the user can go from the instrument page to the stops library and a stop type page can
    list real life examples of such stop).
    """
    number = models.IntegerField(verbose_name='numer',
                                 help_text='Numer głosu, wpływa na kolejność wyświetlania głosów w obrębie '
                                           'klawiatury, jego widoczność na stronie instrumentu jest zależna od '
                                           'ustawienia klawiatury.')
    name = models.CharField(max_length=30, verbose_name='nazwa',
                            help_text='Nazwa głosu, z wyłączeniem długości piszczałki.')
    length = models.CharField(max_length=5, blank=True, null=True, verbose_name='długość piszczałki',
                              help_text='Długość piszczałki wyrażona w stopach.')
    reed = models.BooleanField(verbose_name='głos językowy',
                               help_text='Głosy językowe zwyczajowo wyróżniane są kolorem czerwonym. Zaznaczenie tego '
                                         'pola spowoduje wyróżnienie głosu.')
    keyboard = models.ForeignKey(Keyboard, verbose_name='klawiatura')
    type = models.ForeignKey(StopType, verbose_name='typ głosu')

    class Meta:
        verbose_name = 'głos'
        verbose_name_plural = 'głosy'
        ordering = ['number']

    def __str__(self):
        return '{}, {} - {} - {}. {} {}\''.format(self.keyboard.instrument.location.name,
                                                  self.keyboard.instrument.location.city.name,
                                                  self.keyboard.name, self.number, self.name, self.length)


class Sample(models.Model):
    """
    A sample is a recording which represents sound of a single stop type.
    """
    file = models.FileField(upload_to='samples/', verbose_name='plik')
    description = models.CharField(max_length=100, verbose_name='opis')
    stop_type = models.ForeignKey(StopType, verbose_name='typ głosu')

    class Meta:
        verbose_name = 'próbka'
        verbose_name_plural = 'próbki'

    def __str__(self):
        return 'Próbka #{} ({})'.format(self.id, self.stop_type.name)


class Work(models.Model):
    """
    Work done on an instrument.
    """
    TYPE_CHOICES = (
        ('strojenie', 'strojenie'),
        ('remont', 'remont'),
        ('przebudowa', 'przebudowa'),
        ('przeniesienie', 'przeniesienie'),
        ('inne prace', 'inne prace'),
    )

    type = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name='rodzaj prac')
    year = models.IntegerField(verbose_name='rok')
    description = MarkdownField(verbose_name='opis')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')
    builder = models.ForeignKey(Builder, verbose_name='organmistrz')

    class Meta:
        verbose_name = 'praca'
        verbose_name_plural = 'prace'
        ordering = ['instrument', '-year']

    def __str__(self):
        return '{}, {}, {} ({})'.format(self.type, self.instrument.location.name,
                                        self.instrument.location.city.name, self.year)


class Performer(models.Model):
    """
    A performer can perform recordings or perform during concerts.
    """
    name = models.CharField(max_length=40, verbose_name='nazwisko')
    first_name = models.CharField(blank=True, null=True, max_length=40, verbose_name='imię')
    born = models.DateField(blank=True, null=True, verbose_name='data urodzenia')
    died = models.DateField(blank=True, null=True, verbose_name='data śmierci')
    biography = MarkdownField(verbose_name='biografia')
    photo = models.ImageField(blank=True, null=True, verbose_name='zdjęcie')

    class Meta:
        verbose_name = 'wykonawca'
        verbose_name_plural = 'wykonawcy'
        ordering = ['name', 'first_name']

    def __str__(self):
        return self.name

    def concert_count(self):
        return self.concert_set.count()

    def recording_count(self):
        return self.recording_set.count()

    concert_count.short_description = 'koncerty'
    recording_count.short_description = 'nagrania'


class Recording(models.Model):
    """
    A recording is a sound sample of a specific insturment.
    """
    file = models.FileField(upload_to='recordings/', verbose_name='plik')
    description = models.CharField(max_length=120, verbose_name='opis',
                                   help_text='Krótki komentarz na temat nagrania, np. tytuł wykonywanego utworu.')
    performer = models.ForeignKey(Performer, verbose_name='wykonawca')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')

    class Meta:
        verbose_name = 'nagranie'
        verbose_name_plural = 'nagrania'

    def __str__(self):
        return 'Nagranie: {}, wyk. {}'.format(self.description, self.performer.name)


class Concert(models.Model):
    """
    A concert is played on a specific instrument and features some performers.
    """
    name = models.CharField(max_length=30, verbose_name='nazwa')
    date = models.DateField(verbose_name='data')
    description = MarkdownField(verbose_name='opis')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')
    performers = models.ManyToManyField(Performer, verbose_name='wykonawcy')

    class Meta:
        verbose_name = 'koncert'
        verbose_name_plural = 'koncerty'
        ordering = ['date', 'name']

    def __str__(self):
        return 'Koncert: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name,
                                            self.date)


class Photo(models.Model):
    """
    A photo of an instrument.
    """
    file = models.ImageField(verbose_name='plik')
    description = models.CharField(max_length=100, verbose_name='opis')
    instrument = models.ForeignKey(Instrument, verbose_name='instrument')

    class Meta:
        verbose_name = 'zdjęcie'
        verbose_name_plural = 'zdjęcia'

    def __str__(self):
        return 'Zdjęcie: {}, {}, {}'.format(self.instrument.location.city.name, self.instrument.location.name,
                                            self.description)
