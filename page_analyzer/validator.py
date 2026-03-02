from urllib.parse import urlparse

import validators


def normalize_url(url):
    parsed = urlparse(url)
    normalize = f"{parsed.scheme}://{parsed.hostname}"
    return normalize


def validate_url(url):
    errors = {}

    checks = (
        url == "",  # пустой
        len(url) > 255,  # слишком длинный
        not validators.url(url)  # невалидный
    )

    match checks:
        case (True, _, _):
            errors['url'] = 'URL не может быть пустым'
        case (_, True, _):
            errors['url'] = 'Слишком длинный URL (должен быть короче 255 символов)'
        case (_, _, True):
            errors['url'] = 'Некорректный формат URL'

    return errors



