import inspect
import json
import os
import sys
from typing import Any, Dict, Generator, List, Optional, Tuple, TypedDict


class Country(TypedDict, total=False):
    alpha_2: str
    alpha_3: str
    common_name: str
    flag: str
    name: str
    numeric: str
    official_name: str


class Language(TypedDict, total=False):
    alpha_2: str
    alpha_3: str
    bibliographic: str
    common_name: str
    name: str


class Currency(TypedDict, total=False):
    alpha_3: str
    name: str
    numeric: str


class CountrySubdivision(TypedDict, total=False):
    code: str
    name: str
    parent: str
    type: str


class FormerCountry(TypedDict, total=False):
    alpha_2: str
    alpha_3: str
    alpha_4: str
    comment: str
    name: str
    numeric: str
    withdrawal_date: str


class ExtendedLanguage(TypedDict, total=False):
    alpha_2: str
    alpha_3: str
    bibliographic: str
    common_name: str
    inverted_name: str
    name: str
    scope: str
    type: str


class LanguageFamily(TypedDict, total=False):
    alpha_3: str
    name: str


class ScriptName(TypedDict, total=False):
    alpha_4: str
    name: str
    numeric: str


def get_script_dir(follow_symlinks: bool = True) -> str:
    if getattr(sys, "frozen", False):  # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


BASE_DIR = get_script_dir()

LOCALES_DIR = f"{BASE_DIR}/share/locale"


class ISO:
    iso_key: str
    data: List[Dict[str, str]]

    def __init__(self, iso_key: str) -> None:
        self.iso_key = iso_key
        with open(
            f"{BASE_DIR}/share/iso-codes/json/iso_{self.iso_key}.json", encoding="utf-8"
        ) as iso_file:
            self.data = json.load(iso_file)[self.iso_key]

    def __len__(self) -> int:
        return len(self.data)

    def _name_from_index(self, index: str) -> Generator[Any, None, None]:
        return ((element[index], element["name"]) for element in self.data)

    def _sorted_by_index(self, index: str) -> List[Tuple[str, Any]]:
        return sorted(
            [(element[index], element) for element in self.data if index in element],
            key=lambda x: x[0],
        )

    def get(self, **kwargs: str) -> Optional[Dict[str, str]]:
        try:
            key: str = next(iter(kwargs))
            return [
                element
                for element in self.data
                if key in element and kwargs[key] in element[key]
            ][0]
        except IndexError:
            return {}

    @property
    def items(self) -> List[Any]:
        return self.data


class Countries(ISO):
    @property
    def by_alpha_2(self) -> List[Tuple[str, Country]]:
        return self._sorted_by_index(index="alpha_2")

    @property
    def by_alpha_3(self) -> List[Tuple[str, Country]]:
        return self._sorted_by_index(index="alpha_3")

    @property
    def by_common_name(self) -> List[Tuple[str, Country]]:
        return self._sorted_by_index(index="common_name")

    @property
    def by_name(self) -> List[Tuple[str, Country]]:
        return self._sorted_by_index(index="name")

    @property
    def by_numeric(self) -> List[Tuple[str, Country]]:
        return self._sorted_by_index(index="numeric")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_2")

    @property
    def items(self) -> List[Country]:
        return super().items


class Languages(ISO):
    @property
    def by_alpha_3(self) -> List[Tuple[str, Language]]:
        return self._sorted_by_index(index="alpha_3")

    @property
    def by_name(self) -> List[Tuple[str, Language]]:
        return self._sorted_by_index(index="name")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_3")

    @property
    def items(self) -> List[Language]:
        return super().items


class Currencies(ISO):
    @property
    def by_alpha_3(self) -> List[Tuple[str, Currency]]:
        return self._sorted_by_index(index="alpha_3")

    @property
    def by_name(self) -> List[Tuple[str, Currency]]:
        return self._sorted_by_index(index="name")

    @property
    def by_numeric(self) -> List[Tuple[str, Currency]]:
        return self._sorted_by_index(index="numeric")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_3")

    @property
    def items(self) -> List[Currency]:
        return super().items


class SubdivisionsCountries(ISO):
    @property
    def by_code(self) -> List[Tuple[str, CountrySubdivision]]:
        return self._sorted_by_index(index="code")

    @property
    def by_name(self) -> List[Tuple[str, CountrySubdivision]]:
        return self._sorted_by_index(index="name")

    @property
    def by_type(self) -> List[Tuple[str, CountrySubdivision]]:
        return self._sorted_by_index(index="type")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="code")

    @property
    def items(self) -> List[CountrySubdivision]:
        return super().items


class FormerCountries(ISO):
    @property
    def by_alpha_2(self) -> List[Tuple[str, FormerCountry]]:
        return self._sorted_by_index(index="alpha_2")

    @property
    def by_alpha_3(self) -> List[Tuple[str, FormerCountry]]:
        return self._sorted_by_index(index="alpha_3")

    @property
    def by_alpha_4(self) -> List[Tuple[str, FormerCountry]]:
        return self._sorted_by_index(index="alpha_4")

    @property
    def by_name(self) -> List[Tuple[str, FormerCountry]]:
        return self._sorted_by_index(index="name")

    @property
    def by_numeric(self) -> List[Tuple[str, FormerCountry]]:
        return self._sorted_by_index(index="numeric")

    @property
    def by_withdrawal_date(self) -> List[Tuple[str, FormerCountry]]:
        return self._sorted_by_index(index="withdrawal_date")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_2")

    @property
    def items(self) -> List[FormerCountry]:
        return super().items


class ExtendedLanguages(ISO):
    @property
    def by_alpha_3(self) -> List[Tuple[str, ExtendedLanguage]]:
        return self._sorted_by_index(index="alpha_3")

    @property
    def by_name(self) -> List[Tuple[str, ExtendedLanguage]]:
        return self._sorted_by_index(index="name")

    @property
    def by_scope(self) -> List[Tuple[str, ExtendedLanguage]]:
        return self._sorted_by_index(index="scope")

    @property
    def by_type(self) -> List[Tuple[str, ExtendedLanguage]]:
        return self._sorted_by_index(index="type")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_3")

    @property
    def items(self) -> List[ExtendedLanguage]:
        return super().items


class LanguageFamilies(ISO):
    @property
    def by_alpha_3(self) -> List[Tuple[str, LanguageFamily]]:
        return self._sorted_by_index(index="alpha_3")

    @property
    def by_name(self) -> List[Tuple[str, LanguageFamily]]:
        return self._sorted_by_index(index="name")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_3")

    @property
    def items(self) -> List[LanguageFamily]:
        return super().items


class ScriptNames(ISO):
    @property
    def by_alpha_4(self) -> List[Tuple[str, ScriptName]]:
        return self._sorted_by_index(index="alpha_4")

    @property
    def by_name(self) -> List[Tuple[str, ScriptName]]:
        return self._sorted_by_index(index="name")

    @property
    def by_numeric(self) -> List[Tuple[str, ScriptName]]:
        return self._sorted_by_index(index="numeric")

    @property
    def name(self) -> Generator[Tuple[str, str], None, None]:
        return self._name_from_index(index="alpha_4")

    @property
    def items(self) -> List[ScriptName]:
        return super().items


countries = Countries("3166-1")
languages = Languages("639-2")
currencies = Currencies("4217")
subdivisions_countries = SubdivisionsCountries("3166-2")
former_countries = FormerCountries("3166-3")
extendend_languages = ExtendedLanguages("639-3")
language_families = LanguageFamilies("639-5")
script_names = ScriptNames("15924")
