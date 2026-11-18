#!/usr/bin/env python3
"""下層ページ（ワイヤーフレーム）を組み立てる。
wf-src/<slug>.html（本文のセクションだけ）を、共通のヘッダー・見出し帯・カテゴリ内メニュー・CTA・フッターで包んで <slug>.html に書き出す。
使い方: python3 tools/build_wf.py
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'wf-src')
CUR = 'https://sites.google.com/view/ll-anime/'

# (slug, ページ名, 英字, 親slug or None, 現行ページのパス or None(新規), リード)
PAGES = [
 ('about', '企業概要', 'COMPANY', None, 'kigyougaiyou', '理念・代表メッセージ・会社概要'),
 ('about-media', 'メディア掲載・受賞', 'MEDIA', 'about', 'media', '新聞・テレビ・受賞の記録'),
 ('about-media-tama', '第20回 多摩ブルー・グリーン賞 受賞', 'AWARD', 'about-media', 'media/tama_bluegreen', '「多摩みらい賞」受賞のご報告'),
 ('service', '事業内容', 'SERVICE', None, 'capacity', '対応工程と制作キャパシティ'),
 ('service-mama', 'ママクリエーターの制作体制', 'MAMA CREATORS', 'service', 'mama_capacity', '国内の在宅ママクリエーターによる制作キャパ'),
 ('service-overseas', '海外拠点 MONICHI Pictures', 'OVERSEAS', 'service', 'teikei', 'モンゴル初のアニメ作画スタジオ'),
 ('service-poster', 'ポスター制作', 'POSTER', 'service', 'poster', 'お店・医院のオリジナルポスター'),
 ('works', '制作実績', 'WORKS', None, 'jisseki', '参加作品の一覧'),
 ('academy', 'アニメーター育成プロジェクト', 'ACADEMY', None, 'ikusei', '7か月で在宅アニメーターへ'),
 ('academy-voice', '卒業生インタビュー', 'VOICE', 'academy', 'ikusei/interview2', '育成プロジェクト卒業生10名の声'),
 ('academy-voice-01', '松井美穂さん（1期生）', 'VOICE 01', 'academy-voice', 'ikusei/interview2/matsuimiho', '卒業生インタビュー'),
 ('academy-voice-02', '向山真由美さん（2期生）', 'VOICE 02', 'academy-voice', 'ikusei/interview2/mukouyama', '卒業生インタビュー'),
 ('academy-voice-03', '蕪山ゆりさん（3期生）', 'VOICE 03', 'academy-voice', 'ikusei/interview2/yuri', '卒業生インタビュー'),
 ('academy-voice-04', '福川有輝乃さん（4期生）', 'VOICE 04', 'academy-voice', 'ikusei/interview2/fukukawayukino', '卒業生インタビュー'),
 ('academy-voice-05', '香取ゆりさん（4期生）', 'VOICE 05', 'academy-voice', 'ikusei/interview2/katori', '卒業生インタビュー'),
 ('academy-voice-06', '浅芭むぎさん（5期生）', 'VOICE 06', 'academy-voice', 'ikusei/interview2/asabamugi', '卒業生インタビュー'),
 ('academy-voice-07', 'えもじの子さん（5期生）', 'VOICE 07', 'academy-voice', 'ikusei/interview2/emojinoko', '卒業生インタビュー'),
 ('academy-voice-08', 'Mさん（5期生）', 'VOICE 08', 'academy-voice', 'ikusei/interview2/M', '卒業生インタビュー'),
 ('academy-voice-09', 'S.M.さん（7期生）', 'VOICE 09', 'academy-voice', 'ikusei/interview2/s-m', '卒業生インタビュー'),
 ('academy-voice-10', 'yossyさん（7期生）', 'VOICE 10', 'academy-voice', 'ikusei/interview2/yossy', '卒業生インタビュー'),
 ('support', '子育て支援', 'SUPPORT', None, 'saport_mama', '育児支援金とパートナーシップ契約'),
 ('community', '地域活動・ワークショップ', 'COMMUNITY', None, 'workshop', 'アニメの楽しさを地域へ'),
 ('community-0928', 'イベントレポート：作画体験・業界交流会', 'EVENT REPORT', 'community', 'workshop/0928', 'CGディレクター サトウユーゾー氏を迎えて'),
 ('community-gourmet', '東大和グルメ', 'LOCAL GOURMET', 'community', 'Gourmet', 'スタッフおすすめの地元のお店'),
 ('community-gourmet-01', 'クリカ食堂（ベーグル）', 'GOURMET 01', 'community-gourmet', 'Gourmet/kurika', '東大和グルメ'),
 ('community-gourmet-02', 'ラーメン 狼煙屋', 'GOURMET 02', 'community-gourmet', 'Gourmet/noroshiya', '東大和グルメ'),
 ('community-gourmet-03', '洋食屋 パンドラ（PANDORA）', 'GOURMET 03', 'community-gourmet', 'Gourmet/PANDORA', '東大和グルメ'),
 ('community-gourmet-04', 'パン屋 Lazalee（ラザレ）', 'GOURMET 04', 'community-gourmet', 'Gourmet/Lazalee', '東大和グルメ'),
 ('community-gourmet-05', 'ステーキ＆ハンバーグ テキサス', 'GOURMET 05', 'community-gourmet', 'Gourmet/texas', '東大和グルメ'),
 ('community-gourmet-06', '貯水池 鳥山', 'GOURMET 06', 'community-gourmet', 'Gourmet/toriyama', '東大和グルメ'),
 ('community-gourmet-07', 'イタリア料理＆総菜 coloritura', 'GOURMET 07', 'community-gourmet', 'Gourmet/coloritura', '東大和グルメ'),
 ('community-gourmet-08', '浦川のお肉屋さん', 'GOURMET 08', 'community-gourmet', 'Gourmet/urakawa', '東大和グルメ'),
 ('recruit', '採用情報', 'RECRUIT', None, 'saiyo', '一緒に働く仲間を募集しています'),
 ('recruit-animator', 'デジタル作画アニメーター募集', 'ANIMATOR', 'recruit', 'saiyo/animator', 'LO・作監・原画・動画／完全在宅'),
 ('news', 'お知らせ・読みもの', 'NEWS', None, None, 'お知らせ・特集・スタッフブログ'),
 ('news-visit', '特集：主婦がアニメスタジオに行ってみた', 'FEATURE', 'news', 'seisaku', '取引先スタジオ訪問記'),
 ('news-visit-01', '第1弾 ゆめたカンパニー様', 'FEATURE 01', 'news-visit', 'seisaku/yumeta', '主婦がアニメスタジオに行ってみた'),
 ('news-visit-02', '第2弾 Voil様', 'FEATURE 02', 'news-visit', 'seisaku/voil', '主婦がアニメスタジオに行ってみた'),
 ('news-visit-03', '第3弾 ダンデライオンアニメーションスタジオ様', 'FEATURE 03', 'news-visit', 'seisaku/第3弾ダンデライオンアニメーションスタジオ様', '主婦がアニメスタジオに行ってみた'),
 ('news-blog', 'スタッフブログ', 'STAFF BLOG', 'news', 'STAFF_blog', 'スタッフの日々'),
 ('news-blog-stove', 'カフェ Stove', 'BLOG', 'news-blog', 'STAFF_blog/stove', 'スタッフブログ'),
 ('contact', 'お問い合わせ', 'CONTACT', None, None, 'ご相談・ご応募・取材のご依頼'),
]
P = {p[0]: p for p in PAGES}
ON = ' class="on"'
# グローバルナビ（現行サイトのメニュー構成に合わせる：ユーザー指示 2026-11-19）
MENU = [
 ('top-01', 'ホーム', []),
 ('academy', 'アニメーター育成プロジェクト', [('academy', '育成プロジェクト'), ('academy-voice', '卒業生インタビュー')]),
 ('about', '企業概要', []),
 ('works', '制作実績', []),
 ('recruit', '採用情報', [('recruit', '採用情報'), ('recruit-animator', 'デジタル作画アニメーター募集'), ('support', '子育て支援')]),
 ('other', 'その他', [('service', '事業内容・キャパシティ'), ('service-mama', 'ママクリエーターの制作体制'), ('service-overseas', '海外拠点 MONICHI Pictures'),
   ('service-poster', 'ポスター制作'), ('community', '地域活動・ワークショップ'), ('community-gourmet', '東大和グルメ'),
   ('news', 'お知らせ'), ('news-visit', '主婦がアニメスタジオに行ってみた'), ('news-blog', 'スタッフブログ'), ('about-media', 'メディア掲載・受賞')]),
]
# ナビ上の所属（現在地の強調用）
NAVCAT = {'academy': 'academy', 'about': 'about', 'works': 'works', 'recruit': 'recruit', 'support': 'recruit'}
# フッターのサイトマップ列（カテゴリトップ）
NAV = [('about', '企業概要'), ('service', '事業内容'), ('works', '制作実績'), ('academy', 'アニメーター育成'),
       ('support', '子育て支援'), ('community', '地域活動'), ('recruit', '採用情報'), ('news', 'お知らせ')]


def top_cat(slug):
    while P[slug][3]:
        slug = P[slug][3]
    return slug


def children(slug):
    return [p for p in PAGES if p[3] == slug]


def crumbs(slug):
    out = []
    s = slug
    while s:
        out.append(s)
        s = P[s][3]
    return list(reversed(out))


def esc(s):
    return html.escape(s, quote=True)


def page(slug, body):
    _, title, en, parent, src, lead = P[slug]
    cat = top_cat(slug)
    navcat = NAVCAT.get(cat, 'other')
    def item(key, label, subs):
        on = ON if key == navcat else ''
        if not subs:
            return f'<a href="{key}.html"{on}>{label}</a>'
        head = f'<a href="{subs[0][0] if key == "other" else key}.html"{on} aria-haspopup="true">{label}<i>▾</i></a>'
        dd = ''.join(f'<a href="{a}.html"{ON if a == slug else ""}>{esc(b)}</a>' for a, b in subs)
        return f'<div class="wf-dd">{head}<div class="wf-ddm">{dd}</div></div>'
    nav = ''.join(item(*m) for m in MENU)
    drawer = ''.join(
        (f'<a href="{k}.html">{l}</a>' if not sb else f'<p class="wf-dh">{l}</p>' + ''.join(f'<a class="wf-dsub" href="{a}.html">{esc(b)}</a>' for a, b in sb))
        for k, l, sb in MENU)
    bc = '<a href="top-01.html">トップ</a>' + ''.join(
        f' ＞ <a href="{s}.html">{esc(P[s][1])}</a>' if s != slug else f' ＞ {esc(P[s][1])}' for s in crumbs(slug))
    # カテゴリ内メニュー：カテゴリ直下＋（いる場合）同じ親を持つ兄弟
    lnav_items = [cat] + [c[0] for c in children(cat)]
    if parent and parent != cat:
        lnav_items += [c[0] for c in children(parent)] if len(children(parent)) <= 10 else []
    seen = []
    for s in lnav_items:
        if s not in seen:
            seen.append(s)
    lnav = ''
    if len(seen) > 1:
        def short(s):
            t = P[s][1]
            return t.replace('特集：', '').replace('アニメーター育成プロジェクト', '育成プロジェクト概要')
        lnav = '<nav class="wf-lnav" aria-label="カテゴリ内メニュー"><div class="wf-lnav-in">' + ''.join(
            f'<a href="{s}.html"{ON if s == slug else ""}>{esc(short(s))}</a>' for s in seen) + '</div></nav>'
    frm = (f'<a class="wf-from" href="{CUR}{src}" target="_blank" rel="noopener">現行サイト「{esc(src)}」の内容をもとに構成</a>'
           if src else '<span class="wf-from">新規ページ（現行サイトに無いページ・追加提案）</span>')
    # footer sitemap（全ページ）
    cols = []
    for s, n in NAV + [('contact', 'お問い合わせ')]:
        items = []
        def walk(x, depth):
            for c in children(x):
                items.append(f'<li><a href="{c[0]}.html">{"　" * depth}{esc(c[1])}</a></li>')
                walk(c[0], depth + 1)
        walk(s, 0)
        cols.append(f'<div><h4><a href="{s}.html">{n}</a></h4><ul>{"".join(items)}</ul></div>')
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{esc(title)}｜Lu Laforte ワイヤーフレーム</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Josefin+Sans:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/wf.css">
<link rel="stylesheet" href="assets/kari.css">
</head>
<body>
<header class="wf-hd"><div class="wf-hd-in">
<a class="wf-logo" href="top-01.html" aria-label="Lu Laforte トップへ">LOGO</a>
<nav class="wf-nav" aria-label="グローバルナビ">{nav}</nav><a class="wf-cta" href="contact.html">お問い合わせ</a>
<button class="wf-hb" type="button" aria-label="メニュー" aria-expanded="false">MENU</button>
</div><div class="wf-drawer">{drawer}<a class="wf-cta" href="contact.html">お問い合わせ</a></div></header>
<div class="wf-ttl"><div class="wf-ttl-in">
<p class="wf-bc">{bc}</p>
<p class="wf-en">{esc(en)}</p>
<h1>{esc(title)}</h1>
<p class="wf-lead">{esc(lead)}</p>
{frm}
</div></div>
{lnav}
<main>
{body}
</main>
<section class="wf-ctas"><div class="wf-in">
<p class="wf-en">CONTACT</p><h2 class="wf-h2">ご相談・お申し込みはこちら</h2>
<p>制作のご依頼、育成プロジェクトのお申し込み、採用へのご応募、取材のご依頼など、目的を選んでお問い合わせください。</p>
<div class="wf-btns"><a class="wf-btn" href="contact.html#work">制作のご相談</a><a class="wf-btn sub" href="contact.html#academy">育成のお申し込み</a><a class="wf-btn sub" href="contact.html#recruit">採用への応募</a></div>
</div></section>
<footer class="wf-ft"><div class="wf-in">
<a class="wf-logo" href="top-01.html">LOGO</a>
<p class="wf-note">株式会社Lu Laforte（ル ラフォート）／所在地：東京都東大和市（詳細確認中）<span data-kari></span>／home.lulaforte@gmail.com／平日9:00〜23:00</p>
<div class="wf-ft-cols">{"".join(cols)}</div>
<p class="wf-copy">© Lu Laforte Inc.　｜　<a href="index.html">デザイン一覧へ戻る</a>　｜　<a href="structure.html">サイト構成の考え方</a></p>
</div></footer>
<a class="wf-fab" href="contact.html">お問い<br>合わせ</a>
<div class="kari-note"><b>仮</b>文章は仮／赤枠は追加提案</div>
<script>
(function(){{var b=document.querySelector('.wf-hb'),d=document.querySelector('.wf-drawer');
b.addEventListener('click',function(){{var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o);b.textContent=o?'CLOSE':'MENU';}});}})();
</script>
</body>
</html>
'''


def main():
    missing = []
    for slug, *_ in PAGES:
        f = os.path.join(SRC, slug + '.html')
        if not os.path.exists(f):
            missing.append(slug)
            body = ('<section class="wf-sec"><div class="wf-in"><div class="wf-img wide">（作成中）</div></div></section>')
        else:
            body = open(f, encoding='utf-8').read()
        open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf-8').write(page(slug, body))
    print(f'built {len(PAGES)} pages', ('missing: ' + ', '.join(missing)) if missing else '')


if __name__ == '__main__':
    main()
