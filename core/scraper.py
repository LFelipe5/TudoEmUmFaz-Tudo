"""Bounded public-page extraction; JavaScript pages are not rendered."""
import ipaddress
import socket
from urllib.parse import urlsplit, urljoin
import requests
from bs4 import BeautifulSoup


def validate_url(url):
    parsed = urlsplit(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Enter a public HTTP or HTTPS URL without credentials.')
    if parsed.port not in (None, 80, 443):
        raise ValueError('Only standard web ports are supported.')
    addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError('Private and local network addresses are not supported.')


def scrape(url):
    # Deploy behind an outbound firewall: DNS validation alone cannot prevent DNS rebinding.
    with requests.Session() as session:
        session.headers['User-Agent'] = 'TudoEmUm/0.1 (personal page extraction)'
        for _ in range(6):
            validate_url(url)
            with session.get(url, timeout=(5, 10), stream=True, allow_redirects=False) as response:
                if response.is_redirect:
                    url = urljoin(url, response.headers['Location'])
                    continue
                response.raise_for_status()
                if 'text/html' not in response.headers.get('Content-Type', '').lower():
                    raise ValueError('This tool supports HTML pages only.')
                content = bytearray()
                for chunk in response.iter_content(16384):
                    content.extend(chunk)
                    if len(content) > 1_000_000:
                        raise ValueError('The page exceeds the 1 MB limit.')
                soup = BeautifulSoup(bytes(content), 'html.parser')
                links = []
                for anchor in soup.select('a[href]')[:100]:
                    href = urljoin(url, anchor['href'])
                    if urlsplit(href).scheme in ('http', 'https'):
                        links.append({'text': anchor.get_text(' ', strip=True) or href, 'url': href})
                return {'url': url, 'title': soup.title.get_text(' ', strip=True) if soup.title else 'Untitled',
                        'headings': [h.get_text(' ', strip=True) for h in soup.select('h1,h2,h3')[:50]], 'links': links}
    raise ValueError('The page redirected too many times.')
