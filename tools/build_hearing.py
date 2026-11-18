#!/usr/bin/env python3
"""wf-src/_adds-*.md（追加提案の一覧）を集めて hearing.html（ヒアリング項目）を作る。"""
import os, re, html, glob, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('b', os.path.join(ROOT, 'tools/build_wf.py')); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
P = b.P
ORDER = [p[0] for p in b.PAGES]
rows = []
for f in sorted(glob.glob(os.path.join(ROOT, 'wf-src/_adds-*.md'))):
    sec_moved = False
    for line in open(f, encoding='utf-8'):
        if line.startswith('## ') and '移して' in line: sec_moved = True
        if not line.startswith('|') or line.startswith('|---') or 'ヒアリングで聞くこと' in line or '追加したセクション' in line: continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4 or sec_moved: continue
        page, item, why, ask = cells[0], cells[1], cells[2], ' | '.join(cells[3:])
        m = re.match(r'([a-z0-9\-〜]+)', page)
        slug = m.group(1) if m else ''
        if '〜' in slug: slug = slug.split('〜')[0] + ('01' if slug.endswith('-') else '')
        slug = slug if slug in P else (slug + '01' if slug + '01' in P else slug)
        rows.append((slug, page, item, why, ask))
def key(r):
    return ORDER.index(r[0]) if r[0] in ORDER else 999
rows.sort(key=key)
def md(s):
    s = html.escape(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s.replace('&lt;br&gt;', '<br>')
groups = {}
for r in rows:
    cat = b.top_cat(r[0]) if r[0] in P else 'other'
    groups.setdefault(cat, []).append(r)
CATN = dict(b.NAV + [('contact', 'お問い合わせ')])
body = ''
toc = ''
for cat in [c for c, _ in b.NAV] + ['contact', 'other']:
    if cat not in groups: continue
    name = CATN.get(cat, 'その他')
    toc += f'<a href="#c-{cat}">{name}（{len(groups[cat])}）</a>'
    trs = ''.join(
        f'<tr><td><a href="{r[0]}.html">{html.escape(P[r[0]][1]) if r[0] in P else md(r[1])}</a></td><td>{md(r[2])}</td><td class="why">{md(r[3])}</td><td class="ask"><label><input type="checkbox"> {md(r[4])}</label></td></tr>'
        for r in groups[cat])
    body += f'<section id="c-{cat}"><h2>{name}<small>{len(groups[cat])}項目</small></h2><div class="tbl"><table><thead><tr><th>ページ</th><th>追加した項目</th><th>追加した理由（調査）</th><th>ヒアリングで聞くこと</th></tr></thead><tbody>{trs}</tbody></table></div></section>'
check = open(os.path.join(ROOT, 'tools/hearing_check.html'), encoding='utf-8').read()
out = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>ヒアリング項目一覧｜Lu Laforte</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Josefin+Sans:wght@600&display=swap" rel="stylesheet">
<style>
body{{margin:0;font-family:'Noto Sans JP',sans-serif;color:#222;background:#faf7f2;line-height:1.75;font-size:14px}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 20px 80px}}
.en{{font:600 12px 'Josefin Sans',sans-serif;letter-spacing:.2em;color:#e8735a}}
h1{{font-size:clamp(24px,3.4vw,34px);margin:6px 0 10px;font-weight:900}}
.lead{{color:#555;max-width:860px}}
.toc{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 8px}}
.toc a{{padding:6px 14px;border:1px solid #222;border-radius:99px;text-decoration:none;color:#222;font-weight:700;font-size:13px;background:#fff}}
.toc a:hover{{background:#222;color:#fff}}
h2{{font-size:21px;margin:44px 0 12px;padding-bottom:6px;border-bottom:2px solid #222;display:flex;gap:10px;align-items:baseline}}
h2 small{{font-size:12px;color:#777;font-weight:500}}
.tbl{{overflow-x:auto;background:#fff;border:1px solid #e3ddd3;border-radius:10px}}
table{{width:100%;border-collapse:collapse;min-width:860px}}
th,td{{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #eee5d8}}
th{{background:#f3ece1;font-size:12px;white-space:nowrap;position:sticky;top:0}}
td:first-child{{white-space:nowrap;font-weight:700}}td:first-child a{{color:#2f7d6b}}
td.why{{color:#666;font-size:12.5px;max-width:300px}}
td.ask{{background:#fffaf2}}
td.ask label{{display:flex;gap:8px;cursor:pointer}}td.ask input{{margin-top:5px;accent-color:#2f7d6b;flex:none}}
code{{font-size:11px;background:#f3ece1;padding:0 4px;border-radius:3px}}
.check li{{margin:8px 0}}.check{{background:#fff;border:1px solid #e3ddd3;border-radius:10px;padding:14px 22px 14px 40px}}
.links a{{display:inline-flex;align-items:center;min-height:42px;padding:0 18px;border-radius:99px;background:#222;color:#fff;text-decoration:none;font-weight:700;margin:6px 6px 0 0}}
</style></head><body><div class="wrap">
<p class="en">HEARING LIST</p>
<h1>ヒアリング項目一覧</h1>
<p class="lead">下層ページのワイヤーフレームで「追加提案（テスト文）」として足した項目と、その理由（アニメ制作会社25社の調査結果）、ヒアリングで聞くことの一覧です。全{len(rows)}項目。チェック欄は画面上のメモ用で保存されません。最初に「現行サイトで見つかった食い違い」をご確認ください。</p>
<div class="links"><a href="index.html">デザイン一覧へ</a><a href="structure.html">サイト構成の考え方</a></div>
<h2>現行サイトで見つかった食い違い・要確認<small>まず確認したいこと</small></h2>
{check}
<div class="toc">{toc}</div>
{body}
</div></body></html>'''
open(os.path.join(ROOT, 'hearing.html'), 'w', encoding='utf-8').write(out)
print('rows', len(rows), {k: len(v) for k, v in groups.items()})
