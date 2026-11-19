"""新しい並びのトップ（ワイヤーフレーム）を組み立てる。
wf-src/_top-wire.html の本文を、下層と同じヘッダー・フッターで包んで top-wire.html に書き出す。
お問い合わせフォームは wf-src/contact.html のフォームをそのまま使う。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_wf as w  # noqa: E402

SLUG = 'top-wire'
w.P[SLUG] = (SLUG, 'トップ（新しい並び）', 'TOP', '', '', '')
w.NAVCAT[SLUG] = 'top-01'

body = open(os.path.join(ROOT, 'wf-src', '_top-wire.html'), encoding='utf-8').read()
contact = open(os.path.join(ROOT, 'wf-src', 'contact.html'), encoding='utf-8').read()
form = re.search(r'<section class="wf-sec wf-add alt" id="form">.*?</section>', contact, re.S).group(0)
form = (form.replace('<section class="wf-sec wf-add alt" id="form">', '<section class="wf-sec" id="contact">')
            .replace('<p class="wf-en">FORM</p>', '<p class="wf-en">11　CONTACT</p>')
            .replace('href="#privacy"', 'href="contact.html#privacy"'))
body = body.replace('@@FORM@@', form)

html = w.page(SLUG, body)
html = re.sub(r'<div class="wf-ttl">.*?</div></div>\n', '', html, flags=re.S)       # 見出し帯は不要
html = re.sub(r'<section class="wf-ctas">.*?</section>\n', '', html, flags=re.S)    # 最後にフォームがあるので共通CTAは外す
html = html.replace('<title>トップ（新しい並び）｜', '<title>トップ 新しい並び｜')
open(os.path.join(ROOT, SLUG + '.html'), 'w', encoding='utf-8').write(html)
print('built', SLUG + '.html')
