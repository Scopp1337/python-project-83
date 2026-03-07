from bs4 import BeautifulSoup


def get_data(html_content):
    if not html_content:
        return {'h1': None, 'title': None, 'description': None}

    soup = BeautifulSoup(html_content, "lxml")

    h1_tag = soup.find('h1')
    h1_text = h1_tag.get_text(strip=True) if h1_tag else None

    title_tag = soup.find('title')
    title_text = title_tag.get_text(strip=True) if title_tag else None

    meta_desc = soup.find('meta', {'name': 'description'})
    desc_content = meta_desc.get('content') if meta_desc else None

    return {
        'h1': h1_text,
        'title': title_text,
        'description': desc_content
    }


def truncate_text(text, length=200):
    if not text:
        return ''
    if len(text) <= length:
        return text
    return text[:length] + '...'