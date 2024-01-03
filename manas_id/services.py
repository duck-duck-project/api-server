CYRILLIC_TO_LATIN = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
}


def transliterate_cyrillic_to_latin(text: str):
    return ''.join(CYRILLIC_TO_LATIN.get(char, '') for char in text.lower())


def get_name_transliteration(name: str) -> str:
    for character in name:
        latin_transliteration = transliterate_cyrillic_to_latin(character)
        if latin_transliteration:
            return latin_transliteration.upper()
    return ''


def get_full_name_abbreviation(full_name: str) -> str:
    name_parts = full_name.upper().split(' ')
    abbreviated_transliterated_name_parts = [
        get_name_transliteration(name) for name in name_parts
    ]
    return ''.join(abbreviated_transliterated_name_parts)
