import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.parser import get_data, truncate_text
from page_analyzer.repository import UrlRepository
from page_analyzer.validator import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def urls_index():
    url = request.form.to_dict()['url']
    errors = validate_url(url)

    match errors:
        case {'url': _}:
            flash('Ошибка! Некорректный URL', 'danger')
            return render_template('index.html'), 422

        case {}:
            normalized_url = normalize_url(url)
            repo = UrlRepository(DATABASE_URL)

            match repo.find_url(normalized_url):
                case None:
                    id = repo.add_url(normalized_url)
                    flash('Страница успешно добавлена', 'success')
                    return redirect(url_for('get_url', id=id))

                case url_info:
                    flash('Страница уже существует', 'warning')
                    return redirect(url_for('get_url', id=url_info.get('id')))


@app.route('/urls/<int:id>')
def get_url(id):
    repo = UrlRepository(DATABASE_URL)

    match repo.find_id(id):
        case None:
            abort(404)

        case url_info:
            checks = repo.get_checks(id)
            return render_template(
                'url.html',
                url_info=url_info,
                checks=checks,
                truncate=truncate_text
            )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_id(id)

    if not url_info:
        abort(404)

    try:
        response = requests.get(url_info['name'], timeout=10)
        response.raise_for_status()

        seo_data = get_data(response.text)

        repo.create_check(
            url_id=id,
            status_code=response.status_code,
            h1=seo_data['h1'],
            title=seo_data['title'],
            description=seo_data['description']
        )
        flash('Страница успешно проверена', 'success')

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('get_url', id=id))


@app.route('/urls', methods=['GET'])
def get_urls():
    repo = UrlRepository(DATABASE_URL)
    urls = repo.get_all_urls()
    last_checks = repo.get_last_check_for_urls()

    return render_template('urls.html', urls=urls, last_checks=last_checks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500