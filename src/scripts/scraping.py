from bs4 import BeautifulSoup
import os
import pprint
import re
import requests
import sys
from urllib.parse import urljoin
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.utils.constants import BASE_URL


def regex_key_book_info(key: str) -> str:
    """
    Responsável por formatar o nome do campo da tabela de informações
    do produto para que ele vire uma chave adequada para o dicionário
    de informações sobre o livro.

    Args:
        key (str): Nome da informação na tabela de informações do livro.

    Returns:
        Nome formatado.
    """
    # Substituir espaços e parênteses/pontos por underscore no
    # nome convertido em letras minúsculas.
    key = re.sub(r"[()\s\.]+", "_", key.lower())
    return key.strip("_")


def get_book_info(book_url: str) -> dict:
    """
    Realiza o scraping da página específica do livro.

    Args:
        book_url (str): URL do livro.

    Retruns:
        Dicionário com as informações do livro.
    """
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'lxml')
    infos = dict()

    infos['title'] = soup.find('h1').text.strip()
    infos['rating'] = soup.select_one('.star-rating')['class'][1]
    infos['category'] = soup.select('ul.breadcrumb li')[2].text.strip()

    description_tag = soup.select_one('#product_description ~ p')
    infos['description'] = (
            description_tag.text.strip()
            if description_tag else 'No description'
        )

    image_rel_url = soup.select_one('.item img')['src']
    infos['image_url'] = urljoin(book_url, image_rel_url)

    table = soup.select_one('table.table.table-striped')
    table_data = {
            regex_key_book_info(row.th.text.strip()): row.td.text.strip()
            for row in table.find_all('tr')
        }
    infos = {**infos, **table_data}

    return infos


def scrape_books(pages: int = 50) -> list:
    """
        Varre o número de páginas passado como parametro pages para obter
        os links das páginas de cada livro e então chama a função que faz
        o web scraping da pagina do livro.

    Args:
        pages (opcional, int): Número de páginas onde coletaremos os livros.

    Returns:
        list: Lista de dicionários com as informações do livros presentes
        nas páginas que foram percorridas.
    """
    books = []
    for page in range(1, pages + 1):
        url = f'{BASE_URL}page-{page}.html'
        # Recupera a pagina com requests e cria um objeto scraping
        # com o BeautifulSoup e lxml por ser mais robusto.
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        book_links = soup.select('h3 a')
        for link in book_links:
            book_url = urljoin(BASE_URL, link['href'])
            book_data = get_book_info(book_url)
            books.append(book_data)

    return books


if __name__ == "__main__":
    books_info = scrape_books(pages=2)
    for book in books_info:
        pprint.pprint(book)
