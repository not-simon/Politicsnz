import sys
from bs4 import BeautifulSoup as B
s = B(open(sys.argv[1], errors='ignore').read(), 'html.parser')
for x in s(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript', 'svg', 'form']): x.decompose()
main = s.find('article') or s.find('main') or s.body or s
t = main.get_text('\n', strip=True)
print(t[:int(sys.argv[2])])
