#!/usr/bin/env python3
"""Crude wikitext -> readable prose (refs/templates/tables stripped) for reviewing Wikipedia articles.
Usage: python3 -I tools/minor_parties_prose.py <file.wikitext> [max_chars]"""
import re, sys
t = open(sys.argv[1]).read()
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
t = re.sub(r"<ref[^>]*/>", "", t)
t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
for _ in range(6):
    t = re.sub(r"\{\{(?:efn|sfn|cite|Cite|refn|citation|Citation|nbsp|Infobox|infobox|Use |use |Short|short|Main|main|See also|further|Further|More citations|Portal|portal|Reflist|reflist|Wide image|Clear|clear|Multiple image|multiple image|Nowrap|nowrap|Political|Politics|ubl|Ubl|Election|Party|Composition|Conservatism|Sidebar|Pp|pp|Refimprove|Update|update|Dead link|Webarchive|Unreliable|Excessive|Notelist|notelist|Commons|commons|Official website)[^{}]*\}\}", "", t, flags=re.S)
t = re.sub(r"\{\|.*?\|\}", "[TABLE]", t, flags=re.S)
t = re.sub(r"\[\[(?:File|Image):[^\[\]]*(?:\[\[[^\]]*\]\][^\[\]]*)*\]\]", "", t)
t = re.sub(r"\[\[([^\]|]*)\|([^\]]*)\]\]", r"\2", t)
t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
t = re.sub(r"'''?", "", t)
t = re.sub(r"\n{2,}", "\n", t)
print(t[:n])
