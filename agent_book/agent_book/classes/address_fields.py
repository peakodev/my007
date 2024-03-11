from .field import Field, validator
from ..exceptions import WrongNameLengthException, WrongCountryException, EnumValueNotExist, AgentBookException
from ..enums import CountryEnum, UKRAINIAN_REGIONS, US_STATES
from abc import ABC
import re


class WrongZipException(AgentBookException):
    MSGS = {
        CountryEnum.UKRAINE: "ZIP код повинен складатися з 5 символів",
        CountryEnum.USA: "Please provide 5 digits or ZIP+4 codes (5 digits-4 digits)"
    }

    def __init__(self, country_enum):
        super().__init__(WrongZipException.MSGS[country_enum])


class WrongRegionStateException(AgentBookException):
    MSGS = {
        CountryEnum.UKRAINE: "Будьласка введіть існуючу область України",
        CountryEnum.USA: "Please provide right US state"
    }

    def __init__(self, country_enum):
        super().__init__(WrongRegionStateException.MSGS[country_enum])


def get_enum_by_value(enum_class, value):
    for member in enum_class:
        if member.value == value:
            return member
    raise EnumValueNotExist(f"{value} is not a valid value for {enum_class.__name__}")


class CountryBasedField(Field, ABC):
    def __init__(self, value, country: CountryEnum):
        if not country:
            raise WrongCountryException(value)
        self._country_enum = country
        super().__init__(value)


class AddressLine(Field):
    def _validate(self, value):
        if not (isinstance(value, str) and 3 <= len(value) <= 250):
            raise WrongNameLengthException(field='address line', value=value, max_len=250)


class ZipCode(CountryBasedField):
    __R_VALIDATORS = {
        # Regular expression to match Ukrainian ZIP codes (exactly 5 digits)
        CountryEnum.UKRAINE: r"^\d{5}$",
        # Regular expression to match U.S. ZIP codes (5 digits) or ZIP+4 codes (5 digits-4 digits)
        CountryEnum.USA: r"^\d{5}(-\d{4})?$"
    }

    def _validate(self, value):
        pattern = re.compile(ZipCode.__R_VALIDATORS.get(self._country_enum))
        if not pattern.match(value):
            raise WrongZipException(country_enum=self._country_enum)


class Region(CountryBasedField):
    _REGIONS = {
        CountryEnum.UKRAINE: UKRAINIAN_REGIONS,
        CountryEnum.USA: [item for tup in US_STATES for item in tup]
    }

    def _validate(self, value):
        if value not in self._REGIONS.get(self._country_enum):
            raise WrongRegionStateException(country_enum=self._country_enum)


class City(Field):
    def _validate(self, value):
        if not (isinstance(value, str) and 3 <= len(value) <= 50):
            raise WrongNameLengthException(field='city', value=value)


class Country(Field):

    def _validate(self, value):
        try:
            self._value = get_enum_by_value(CountryEnum, value)
        except EnumValueNotExist:
            raise WrongCountryException

    @property
    def value(self) -> CountryEnum:
        return self._value

    @value.setter
    @validator
    def value(self, value: str):
        if not self._value:
            self._validate(value)

    def __str__(self):
        return str(self.value.value)


class Address:
    def __init__(self, country, region, city, zip_code, address_line=None):
        self._country = None
        self._region = None
        self._city = None
        self._zip_code = None
        self._address_line = None
        self.country = country
        self.region = region
        self.city = city
        self.zip_code = zip_code
        self.address_line = address_line

    @property
    def country(self) -> Country:
        return self._country

    @country.setter
    def country(self, country: str):
        self._country = Country(country)

    @property
    def region(self) -> Region:
        return self._region

    @region.setter
    def region(self, region: str):
        self._region = Region(region, self._country.value)

    @property
    def city(self) -> City:
        return self._city

    @city.setter
    def city(self, city: str):
        self._city = City(city)

    @property
    def zip_code(self) -> ZipCode:
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code: str):
        self._zip_code = ZipCode(zip_code, self._country.value)

    @property
    def address_line(self) -> AddressLine:
        return self._address_line

    @address_line.setter
    def address_line(self, address_line: str):
        self._address_line = AddressLine(address_line)

    def __str__(self):
        return (f'{str(self.country)}, '
                f'{str(self.region)}, '
                f'{str(self.city)}, '
                f'{str(self.zip_code)}, '
                f'{str(self.address_line)}')
