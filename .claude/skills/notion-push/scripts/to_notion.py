#!/usr/bin/env python3
"""Convert a chapter .md to Notion-flavored markdown: drop H1, turn styled blocks into colored callouts.
Usage: to_notion.py chapter.md > out.md"""
import re, sys

def callout(icon, color, lines):
    return [f'<callout icon="{icon}" color="{color}">'] + ['\t' + l for l in lines] + ['</callout>']

L = open(sys.argv[1], encoding='utf-8').read().split('\n')[1:]  # strip H1 (title is a page property)
o, i = [], 0
while i < len(L):
    l = L[i]
    if l.startswith('📖 **名詞小卡'):  # bold title + bullets, ends at blank line
        body = [L[i].replace('📖 ', '', 1)]; i += 1
        while i < len(L) and L[i].strip():
            body.append(L[i]); i += 1
        o += callout('📖', 'blue_bg', body); continue
    m = re.match(r'> 🏗️ (.*)', l)
    if m: o += callout('🏗️', 'yellow_bg', [m[1]]); i += 1; continue
    m = re.match(r'> \*\*⚠️ (.*)', l)
    if m: o += callout('⚠️', 'orange_bg', ['**' + m[1]]); i += 1; continue
    m = re.match(r'> (\*\*核心思路：.*)', l)
    if m: o += callout('💡', 'green_bg', [m[1]]); i += 1; continue
    o.append(l); i += 1
print('\n'.join(o))
