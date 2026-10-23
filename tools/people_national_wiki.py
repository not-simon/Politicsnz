"""Shared Wikipedia/Commons API helper with backoff for people_national_* scripts."""
import json, urllib.request, urllib.parse, time, random
UA = {'User-Agent': 'PoliticsNZResearch/1.0 (personal research; national people profiles)'}
def api(params, host='en.wikipedia.org'):
    params = {**params, 'format': 'json'}
    url = f'https://{host}/w/api.php?' + urllib.parse.urlencode(params)
    for i in range(10):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
            time.sleep(1.0)
            if 'error' in r and r['error'].get('code') in ('ratelimited', 'maxlag', 'internal_api_error_DBQueryError'):
                time.sleep(15 * (i + 1)); continue
            return r
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503): raise
            time.sleep(min(120, 8 * (i + 1)) + random.random() * 5)
        except Exception:
            time.sleep(10 * (i + 1))
    raise RuntimeError('rate limited: ' + url)
def fetch_bytes(url):
    for i in range(10):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503): raise
            time.sleep(min(120, 8 * (i + 1)) + random.random() * 5)
    raise RuntimeError('rate limited: ' + url)
