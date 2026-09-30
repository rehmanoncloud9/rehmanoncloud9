#!/usr/bin/env python3
"""Generates the animated, fluid-morphic glass SVG assets for the GitHub profile.
Run:  python3 build_assets.py  ->  writes ../out/assets/*.svg
Fonts (Inter) are subsetted and embedded so text renders identically everywhere."""
import base64, html, io, math, os, random
from fontTools import subset
from fontTools.ttLib import TTFont

FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
STACK = "'IF',-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,Helvetica,Arial,sans-serif"
BG, SKY, IND, VIO, TEAL, GREEN = '#070b14', '#38bdf8', '#6366f1', '#a78bfa', '#22d3ee', '#34d399'
MUTED = 'rgba(226,232,240,.62)'

_tt = {}
def ttf(w):
    if w not in _tt:
        f = TTFont(f'{FONTDIR}inter-latin-{w}-normal.woff2'); _tt[w] = (f, f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    return _tt[w]
def tw(t, size, w=400, ls=0):
    f, cm, hm, u = ttf(w)
    return sum(hm[cm.get(ord(c), cm[ord('n')])][0] for c in t) * size / u * 1.01 + ls * len(t)
def esc(t): return html.escape(t, quote=False)

# ---------- Lucide geometry (24x24) ----------
def circ(cx, cy, r): return f'M{cx-r} {cy}a{r} {r} 0 1 0 {2*r} 0a{r} {r} 0 1 0 {-2*r} 0'
def rr(x, y, w, h, r): return f'M{x+r} {y}h{w-2*r}a{r} {r} 0 0 1 {r} {r}v{h-2*r}a{r} {r} 0 0 1 {-r} {r}h{-(w-2*r)}a{r} {r} 0 0 1 {-r} {-r}v{-(h-2*r)}a{r} {r} 0 0 1 {r} {-r}z'
IC = {
 'building': ['M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z', 'M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2', 'M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2', 'M10 6h4', 'M10 10h4', 'M10 14h4', 'M10 18h4'],
 'pin': ['M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0', circ(12, 10, 3)],
 'grad': ['M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z', 'M22 10v6', 'M6 12.5V16a6 3 0 0 0 12 0v-3.5'],
 'mail': [rr(2, 4, 20, 16, 2), 'm22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7'],
 'globe': [circ(12, 12, 10), 'M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20', 'M2 12h20'],
 'shield': ['M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z', 'm9 12 2 2 4-4'],
 'video': [rr(2, 6, 14, 12, 2), 'M16 13l5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5'],
 'server': [rr(2, 2, 20, 8, 2), rr(2, 14, 20, 8, 2), 'M6 6h.01', 'M6 18h.01'],
 'cloud': ['M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z'],
 'user': [circ(12, 7, 4), 'M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'],
 'sparkle': ['M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0-1.3 1.3L12 21l-1.9-5.8a2 2 0 0 0-1.3-1.3L3 12l5.8-1.9a2 2 0 0 0 1.3-1.3Z'],
 'mic': ['M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z', 'M19 10v2a7 7 0 0 1-14 0v-2', 'M12 19v3'],
 'car': ['M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2', circ(7, 17, 2), 'M9 17h6', circ(17, 17, 2)],
 'folder': ['M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z'],
 'award': ['m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526', circ(12, 8, 6)],
 'compass': [circ(12, 12, 10), 'm16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z'],
}
def ic(name, cx, cy, size, color='#fff', sw=1.8, extra=''):
    s = size / 24
    return (f'<g transform="translate({cx-size/2:.1f} {cy-size/2:.1f}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round" {extra}>' + ''.join(f'<path d="{d}"/>' for d in IC[name]) + '</g>')

# ---------- organic blobs (SMIL path morph) ----------
def smooth(p):
    n = len(p); d = f'M{p[0][0]:.1f},{p[0][1]:.1f}'
    for i in range(n):
        a, b, c, e = p[(i-1) % n], p[i], p[(i+1) % n], p[(i+2) % n]
        d += f'C{b[0]+(c[0]-a[0])/6:.1f},{b[1]+(c[1]-a[1])/6:.1f} {c[0]-(e[0]-b[0])/6:.1f},{c[1]-(e[1]-b[1])/6:.1f} {c[0]:.1f},{c[1]:.1f}'
    return d + 'Z'
def blob(cx, cy, r, seed, n=8, j=.3):
    rnd = random.Random(seed)
    return smooth([(cx + r*(1+rnd.uniform(-j, j))*math.cos(2*math.pi*i/n), cy + r*(1+rnd.uniform(-j, j))*math.sin(2*math.pi*i/n)) for i in range(n)])
def morph_path(cx, cy, r, seed, dur, fill, op=1, j=.3, drift=.25):
    sh = [blob(cx, cy, r, seed*13+k, 8, j) for k in range(4)]; sh.append(sh[0])
    kt = ';'.join(f'{i/(len(sh)-1):.3f}' for i in range(len(sh))); ks = ';'.join(['.45 0 .55 1']*(len(sh)-1))
    dx = r*drift
    mv = (f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx:.0f} {-dx*.6:.0f};{-dx*.7:.0f} {dx*.5:.0f};0 0" '
          f'dur="{dur*1.3:.0f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.33;.66;1" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/>')
    return (f'<path d="{sh[0]}" fill="{fill}" opacity="{op}"><animate attributeName="d" dur="{dur}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="{kt}" keySplines="{ks}" values="{";".join(sh)}"/>{mv}</path>')
def aurora(items): return ''.join(morph_path(cx, cy, r, sd, dur, col, op) for cx, cy, r, col, op, sd, dur in items)

# ---------- SVG container ----------
class S:
    def __init__(s, w, h, title, desc=''):
        s.w, s.h, s.title, s.desc, s.defs, s.b, s.used, s.n = w, h, title, desc, [], [], {}, 0
    def uid(s, p='i'): s.n += 1; return f'{p}{s.n}'
    def add(s, x): s.b.append(x)
    def text(s, x, y, t, size, w=400, fill='#fff', anchor='start', ls=0, extra=''):
        s.used.setdefault(w, set()).update(t)
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{esc(t)}</text>')
    def reveal(s, inner, at, dy=16, dur=.9):
        return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{at}s" dur="{dur}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{at}s" dur="{dur}s" fill="freeze" '
                f'calcMode="spline" keyTimes="0;1" keySplines=".16 1 .3 1"/>{inner}</g>')
    def panel(s, x, y, w, h, r, glows, fill=BG, border=True):
        cid = s.uid('c'); gid = s.uid('bd')
        s.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
                      f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".34"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity=".16"/></linearGradient>')
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
              f'<g clip-path="url(#{cid})"><g filter="url(#b60)">{aurora(glows)}</g>'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h*.5}" fill="url(#hl)"/></g>')
        if border: s.add(f'<rect x="{x+.6}" y="{y+.6}" width="{w-1.2}" height="{h-1.2}" rx="{r}" fill="none" stroke="url(#{gid})" stroke-width="1.2"/>')
    def chip(s, x, y, t, size=13, w=500, h=None, fill='rgba(255,255,255,.07)', stroke='rgba(255,255,255,.14)', color='rgba(241,245,249,.92)', at=None, px=14):
        h = h or size*2.15; cw = tw(t, size, w) + px*2
        g = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="{fill}" stroke="{stroke}"/>'
             + s.text(x+cw/2, y+h/2+size*.36, t, size, w, color, 'middle'))
        s.add(s.reveal(g, at, 10, .7) if at is not None else g); return cw
    def render(s, name, radius=None):
        faces = ''
        for w, chars in s.used.items():
            f = TTFont(f'{FONTDIR}inter-latin-{w}-normal.woff2'); o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['kern', 'tnum']
            sb = subset.Subsetter(o); sb.populate(text=''.join(sorted(chars | set(' .')))); sb.subset(f)
            buf = io.BytesIO(); f.flavor = 'woff2'; f.save(buf)
            faces += f"@font-face{{font-family:'IF';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode(buf.getvalue()).decode()}) format('woff2')}}"
        defs = ''.join(s.defs)
        x = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}" role="img" aria-label="{esc(s.title)}">'
             f'<title>{esc(s.title)}</title><desc>{esc(s.desc or s.title)}</desc><style>{faces}text{{font-family:{STACK};font-kerning:normal}}</style>'
             f'<defs><filter id="b60" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="55"/></filter>'
             f'<filter id="b26" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="26"/></filter>'
             f'<linearGradient id="hl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>{defs}</defs>'
             + ''.join(s.b) + '</svg>')
        open(f'{OUT}/{name}.svg', 'w').write(x); print(f'{name}.svg  {len(x)/1024:.0f} KB')

def wrap(t, size, w, maxw):
    lines, cur = [], ''
    for word in t.split():
        trial = (cur + ' ' + word).strip()
        if tw(trial, size, w) <= maxw: cur = trial
        else: lines.append(cur); cur = word
    return lines + [cur]
def grad_text(s, gid, stops, dur=7, span=700):
    st = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    s.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{span}" y2="0" spreadMethod="repeat">{st}'
                  f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{span} 0" dur="{dur}s" repeatCount="indefinite"/></linearGradient>')

# =============================== HERO ===============================
def hero():
    s = S(1200, 540, 'Abdul Rehman: Founder & CEO of Stayza, Computer Science student at NUST',
          'Abdul Rehman builds full stack products end to end. Founder & CEO of Stayza, BS Computer Science at NUST, Islamabad.')
    W, H, cx, cy, cw, ch, R = 1200, 540, 70, 64, 1060, 412, 46
    s.defs.append(f'<clipPath id="all"><rect width="{W}" height="{H}" rx="40"/></clipPath><clipPath id="card"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="{R}"/></clipPath>'
                  f'<mask id="out"><rect width="{W}" height="{H}" fill="#fff"/><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="{R}" fill="#000"/></mask>')
    for i, (a, b, c) in enumerate([('#c7d2fe', IND, '#3730a3'), ('#bae6fd', SKY, '#0369a1'), ('#ddd6fe', VIO, '#5b21b6'), ('#a5f3fc', TEAL, '#0e7490')]):
        s.defs.append(f'<radialGradient id="og{i}" cx=".3" cy=".22" r=".95"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".18" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></radialGradient>')
    orbs = lambda: ''.join(morph_path(x, y, r, sd, dur, f'url(#og{k})', .96, .13, .12) for k, (x, y, r, sd, dur) in enumerate(
        [(102, 104, 98, 41, 15), (1116, 118, 70, 42, 17), (1098, 470, 110, 43, 19), (118, 470, 68, 44, 16)]))
    s.add(f'<g clip-path="url(#all)"><rect width="{W}" height="{H}" fill="{BG}"/>'
          f'<g filter="url(#b60)">{aurora([(230,150,270,IND,.6,1,26),(980,430,270,SKY,.5,2,30),(900,70,210,VIO,.45,3,24),(330,490,190,TEAL,.3,4,28)])}</g>'
          f'<g mask="url(#out)">{orbs()}</g>'
          f'<g clip-path="url(#card)"><g filter="url(#b26)">{orbs()}</g><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="rgba(10,14,26,.42)"/>'
          f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="rgba(255,255,255,.055)"/><rect x="{cx}" y="{cy}" width="{cw}" height="{ch*.55}" fill="url(#hl)"/></g></g>')
    s.defs.append('<linearGradient id="cb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".45" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".28"/></linearGradient>')
    s.add(f'<rect x="{cx+.75}" y="{cy+.75}" width="{cw-1.5}" height="{ch-1.5}" rx="{R}" fill="none" stroke="url(#cb)" stroke-width="1.5"/>')
    grad_text(s, 'nm', [(0, '#ffffff'), (.35, '#ffffff'), (.5, '#a5e3ff'), (.65, '#ffffff'), (1, '#ffffff')], 7, 800)
    # status pill
    t = 'Open to internships and collaborations'; pw = tw(t, 14, 600) + 62; px = 600 - pw/2
    pill = (f'<rect x="{px:.1f}" y="128" width="{pw:.1f}" height="36" rx="18" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.18)"/>'
            f'<circle cx="{px+22:.1f}" cy="146" r="4.5" fill="{GREEN}"/><circle cx="{px+22:.1f}" cy="146" r="4.5" fill="none" stroke="{GREEN}" stroke-width="1.5">'
            f'<animate attributeName="r" values="4.5;13" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>'
            + s.text(px+38, 151, t, 14, 600, 'rgba(241,245,249,.92)', ls=.2))
    s.add(s.reveal(pill, .3, 12))
    s.add(s.reveal(s.text(600, 268, 'Abdul Rehman', 100, 700, 'url(#nm)', 'middle', -3.6), .6, 26, 1.2))
    s.add(s.reveal(s.text(600, 322, 'I build full stack products, end to end, and take them to production.', 25, 400, 'rgba(226,232,240,.78)', 'middle', -.1), 1.1, 16, 1))
    s.add('<rect x="180" y="352" width="840" height="1" fill="rgba(255,255,255,.12)"/>')
    items = [('building', 'Founder & CEO, Stayza'), ('grad', 'BS Computer Science, NUST'), ('pin', 'Islamabad, Pakistan')]
    ws = [tw(t, 16, 500) + 34 for _, t in items]; gap = 44; x = 600 - (sum(ws) + gap*2)/2
    for k, ((n, t), w_) in enumerate(zip(items, ws)):
        g = ic(n, x+11, 396, 20, SKY, 1.8) + s.text(x+34, 402, t, 16, 500, 'rgba(241,245,249,.9)')
        s.add(s.reveal(g, 1.6 + k*.18, 12, .8)); x += w_ + gap
    s.render('hero')

# =============================== HEADERS ===============================
def header(name, eyebrow, title):
    s = S(1200, 124, title, eyebrow + ': ' + title)
    grad_text(s, 'ht', [(0, SKY), (.33, IND), (.66, VIO), (1, SKY)], 9, 1000)
    s.add(s.text(600, 38, eyebrow.upper(), 13, 600, '#8b949e', 'middle', 4.2))
    s.add(s.text(600, 96, title, 50, 700, 'url(#ht)', 'middle', -1.6))
    s.render(name)

# =============================== FLAGSHIP ===============================
LOGO = 'M56 18 C56 10 20 10 20 28 C20 44 60 44 60 62 C60 72 40 76 24 70'
def stayza():
    s = S(1200, 470, 'Stayza: student hostel discovery platform, in production', 'Stayza is a verified, commission-free accommodation marketplace for students and professionals in Pakistan, founded and built by Abdul Rehman.')
    s.panel(10, 10, 1180, 450, 44, [(190, 90, 230, IND, .55, 5, 24), (1040, 420, 250, SKY, .38, 6, 28), (700, 40, 170, VIO, .3, 7, 22)])
    # animated logo mark
    m = 1.3; ox, oy = 70, 44
    s.add(f'<g transform="translate({ox} {oy}) scale({m})"><path d="{LOGO}" pathLength="1" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1">'
          f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.3;.86;1" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".65 0 .35 1;0 0 1 1;.65 0 .35 1"/></path>'
          f'<circle cx="56" cy="18" r="4" fill="#fff"/><circle cx="24" cy="70" r="4" fill="#fff"/></g>')
    s.add(s.text(190, 100, 'STAYZA', 22, 300, '#fff', ls=9.5) + s.text(190, 130, 'Student hostel discovery platform', 15, 500, MUTED))
    s.add('<circle cx="1000" cy="98" r="4.5" fill="%s"/><circle cx="1000" cy="98" r="4.5" fill="none" stroke="%s" stroke-width="1.5"><animate attributeName="r" values="4.5;13" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>' % (GREEN, GREEN))
    s.add(s.text(1016, 103, 'In production', 14, 600, 'rgba(241,245,249,.9)'))
    s.add(s.reveal(s.text(78, 262, 'Discover verified accommodation', 44, 700, '#fff', ls=-1.3) + s.text(78, 314, 'with confidence, transparency, and ease.', 44, 700, 'rgba(255,255,255,.5)', ls=-1.3), .3, 20, 1.1))
    tiles = [('shield', 'Two-tier verification', 'Identity and location checks, plus a mandatory live video call.'),
             ('sparkle', 'Zero commission', 'Transparent pricing. Owners and students connect directly.'),
             ('compass', '8 cities', 'Lahore, Karachi, Islamabad, Rawalpindi and four more cities.')]
    tw_, x0 = 338, 78
    for i, (n, t, d) in enumerate(tiles):
        x = x0 + i*(tw_+16)
        g = (f'<rect x="{x}" y="346" width="{tw_}" height="86" rx="22" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.12)"/>'
             f'<circle cx="{x+40}" cy="389" r="22" fill="rgba(99,102,241,.22)"/>' + ic(n, x+40, 389, 24, '#c7d2fe', 1.8) + s.text(x+76, 380, t, 17, 700, '#fff'))
        for li, ln in enumerate(wrap(d, 13, 400, tw_-96)[:2]): g += s.text(x+76, 400+li*17, ln, 13, 400, MUTED)
        s.add(s.reveal(g, .9 + i*.2, 14, .8))
    s.render('stayza')

def timeline():
    s = S(1200, 260, 'The Stayza journey', 'Timeline: ideation and validation 2024 to 2025, platform architecture mid 2025, launch early 2026, national expansion next.')
    s.panel(10, 10, 1180, 240, 40, [(160, 200, 200, IND, .4, 8, 26), (1050, 60, 200, SKY, .3, 9, 30)])
    ev = [('2024 – 2025', 'Ideation & validation', 'Hundreds of student interviews in Islamabad.'), ('Mid 2025', 'Platform architecture', 'Verification workflows, schemas and trust badges.'),
          ('Early 2026', 'Stayza launch', 'Listings open, verification pipeline live.'), ('Next', 'National expansion', 'More education hubs and direct digital booking.')]
    xs = [150 + i*300 for i in range(4)]
    s.defs.append(f'<linearGradient id="tl" gradientUnits="userSpaceOnUse" x1="{xs[0]}" x2="{xs[-1]}" y1="0" y2="0"><stop offset="0" stop-color="{IND}"/><stop offset=".7" stop-color="{SKY}"/><stop offset="1" stop-color="{SKY}" stop-opacity=".25"/></linearGradient>')
    s.add(f'<path d="M{xs[0]} 92 H{xs[-1]}" stroke="rgba(255,255,255,.1)" stroke-width="3" stroke-linecap="round"/>'
          f'<path d="M{xs[0]} 92 H{xs[-1]}" pathLength="1" stroke="url(#tl)" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin=".3s" dur="2.4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".5 0 .2 1"/></path>'
          f'<circle r="6" fill="#fff"><animateMotion dur="5s" begin="2.7s" repeatCount="indefinite" path="M{xs[0]} 92 H{xs[-1]}"/><animate attributeName="opacity" values="0;1;1;0" dur="5s" begin="2.7s" repeatCount="indefinite"/></circle>')
    for i, ((d, t, x_), x) in enumerate(zip(ev, xs)):
        last = i == 3; at = .3 + i*.8; dash = ' stroke-dasharray="4 4"' if last else ''
        g = (f'<circle cx="{x}" cy="92" r="11" fill="{BG}" stroke="{SKY if not last else "rgba(255,255,255,.4)"}" stroke-width="3" {dash}/>'
             + (f'<circle cx="{x}" cy="92" r="4.5" fill="{SKY}"/>' if not last else '')
             + s.text(x, 60, d.upper(), 12, 600, SKY if not last else '#8b949e', 'middle', 2.4) + s.text(x, 140, t, 19, 700, '#fff', 'middle', -.3))
        for li, ln in enumerate(wrap(x_, 14, 400, 250)): g += s.text(x, 168+li*19, ln, 14, 400, MUTED, 'middle')
        s.add(s.reveal(g, at, 12, .8))
    s.render('timeline')

# =============================== PROJECT CARDS ===============================
def pcard(name, W, icon, title, sub, desc, tags, status, glow, seed):
    s = S(W, 304, title, f'{title}: {sub}. {desc}')
    s.panel(10, 10, W-20, 284, 34, [(W*.15, 30, 150, glow, .55, seed, 22), (W*.95, 260, 170, VIO if glow != VIO else SKY, .3, seed+1, 26)])
    s.add(f'<circle cx="62" cy="70" r="28" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.16)"/>' + ic(icon, 62, 70, 27, '#fff', 1.7))
    sw_ = tw(status, 12, 600) + 24
    s.add(f'<rect x="{W-40-sw_:.1f}" y="52" width="{sw_:.1f}" height="28" rx="14" fill="rgba(255,255,255,.07)" stroke="rgba(255,255,255,.14)"/>' + s.text(W-40-sw_/2, 70.5, status, 12, 600, 'rgba(241,245,249,.85)', 'middle', .2))
    s.add(s.text(38, 138, title, 26, 700, '#fff', ls=-.7) + s.text(38, 162, sub, 14, 500, SKY))
    for i, ln in enumerate(wrap(desc, 14, 400, W-76)[:3]): s.add(s.text(38, 192+i*19, ln, 14, 400, MUTED))
    x = 38
    for t in tags: x += s.chip(x, 246, t, 12, 500, 26, px=11) + 6
    s.render(name)

# =============================== STACK ===============================
def stack():
    groups = [('Languages', ['Python', 'Java', 'TypeScript', 'SQL', 'C++', 'JavaScript', 'HTML', 'CSS']),
              ('Frontend', ['React', 'Tailwind CSS', 'Flutter', 'Tauri', 'JavaFX', 'Java Swing', 'shadcn/ui', 'Framer Motion']),
              ('Backend', ['FastAPI', 'Supabase', 'Hibernate', 'Node.js', 'REST APIs', 'Supabase Auth']),
              ('Databases', ['PostgreSQL', 'MariaDB', 'SQLite', 'Firebase', 'MySQL']),
              ('Tools', ['Vercel', 'Resend', 'Git', 'GitHub', 'VS Code', 'Figma', 'Vite', 'npm', 'Linux', 'Maven', 'XAMPP']),
              ('Learning now', ['System Design', 'Distributed Systems', 'Cloud Computing', 'Cloud Deployment', 'Software Architecture', 'Design Patterns', 'Advanced React', 'Backend Engineering', 'AI'])]
    LX, CX0, RX, CH, GAP, RG = 54, 250, 1146, 34, 9, 18
    rows, y = [], 52
    for gi, (g, chips) in enumerate(groups):
        cur, xx, lines = [], CX0, []
        for c in chips:
            w = tw(c, 14, 500) + 30
            if xx + w > RX and cur: lines.append(cur); cur, xx = [], CX0
            cur.append((c, xx, w)); xx += w + GAP
        lines.append(cur); rows.append((g, y, lines)); y += len(lines)*(CH+GAP) - GAP + RG + 12
    H = y + 32
    s = S(1200, H, 'Tech stack', 'Languages, frontend, backend, databases, tools and what Abdul is learning now.')
    s.panel(10, 10, 1180, H-20, 40, [(180, 100, 230, IND, .42, 11, 26), (1050, H-80, 250, SKY, .3, 12, 30), (640, H*.5, 170, VIO, .16, 13, 24)])
    n = 0
    for gi, (g, gy, lines) in enumerate(rows):
        learn = g == 'Learning now'
        s.add(s.reveal(s.text(LX, gy+CH/2+5, g.upper(), 12, 700, GREEN if learn else '#8b949e', ls=2.8), .2 + gi*.15, 8, .7))
        if gi: s.add(f'<rect x="{LX}" y="{gy-15}" width="1092" height="1" fill="rgba(255,255,255,.07)"/>')
        for li, ln in enumerate(lines):
            for c, x, w in ln:
                s.chip(x, gy + li*(CH+GAP), c, 14, 500, CH, at=.3 + n*.045,
                       fill='rgba(52,211,153,.10)' if learn else 'rgba(255,255,255,.07)', stroke='rgba(52,211,153,.28)' if learn else 'rgba(255,255,255,.14)'); n += 1
    s.render('stack')

# =============================== NOW / RECOGNITION ===============================
def now():
    s = S(1200, 372, 'Currently and recognition', 'Currently iterating on Stayza, learning system design and cloud, preparing for internships. Recognition: Google Antigravity National Hackathon, AI Seekho 2026; Leadership Training, Punjab Boy Scouts Association.')
    s.panel(10, 10, 1180, 352, 40, [(1000, 60, 230, SKY, .38, 14, 26), (180, 320, 240, IND, .4, 15, 30)])
    tiles = [('building', 'Iterating on Stayza', 'with real users'), ('server', 'System design', 'scalable backend architecture'), ('cloud', 'Cloud deployment', 'and infrastructure'), ('user', 'Preparing for', 'software engineering internships')]
    tw_ = 268
    for i, (n, a, b) in enumerate(tiles):
        x = 44 + i*(tw_+12)
        g = (f'<rect x="{x}" y="44" width="{tw_}" height="128" rx="26" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.12)"/>'
             f'<circle cx="{x+44}" cy="94" r="26" fill="rgba(56,189,248,.14)">' + f'<animate attributeName="r" values="26;29;26" dur="{3.4+i*.3}s" repeatCount="indefinite"/></circle>' + ic(n, x+44, 94, 26, SKY, 1.8)
             + s.text(x+26, 146, a, 18, 700, '#fff', ls=-.3) + s.text(x+26, 166, b, 13, 400, MUTED))
        s.add(s.reveal(g, .2 + i*.18, 14, .8))
    s.add(s.reveal(s.text(56, 220, 'ALSO BUILDING', 12, 700, '#8b949e', ls=2.8), .9, 8, .7))
    x = 218
    for t in ['course-file-organizer · Python', 'CarRent · Qt / C++']: x += s.chip(x, 202, t, 13, 500, 30, at=1.0) + 8
    s.add('<rect x="56" y="248" width="1088" height="1" fill="rgba(255,255,255,.08)"/>')
    rec = [('award', 'Google Antigravity National Hackathon', 'AI Seekho 2026 · Google for Developers'), ('compass', 'Leadership Training', 'Punjab Boy Scouts Association')]
    for i, (n, a, b) in enumerate(rec):
        x = 56 + i*560
        g = (f'<circle cx="{x+24}" cy="{300}" r="24" fill="rgba(167,139,250,.16)"/>' + ic(n, x+24, 300, 24, '#ddd6fe', 1.7) + s.text(x+62, 296, a, 17, 700, '#fff', ls=-.2) + s.text(x+62, 318, b, 13, 400, MUTED))
        s.add(s.reveal(g, 1.2 + i*.2, 12, .8))
    s.render('now')

# =============================== PILLS + FOOTER ===============================
def pill(name, icon, label, glow, logo=False):
    s = S(300, 84, label, f'Link: {label}')
    s.panel(10, 14, 280, 56, 28, [(70, 42, 70, glow, .8, 21 + len(label), 18)], fill='#0b1120')
    if logo: s.add(f'<g transform="translate(29 26) scale(.33)"><path d="{LOGO}" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round"/><circle cx="56" cy="18" r="6" fill="#fff"/><circle cx="24" cy="70" r="6" fill="#fff"/></g>')
    elif icon == 'in': s.add(s.text(48, 49, 'in', 22, 800, '#fff', 'middle', -.5))
    else: s.add(ic(icon, 47, 42, 24, '#fff', 1.8))
    s.add(s.text(76, 48, label, 17, 600, '#fff', ls=-.2))
    s.render(name)

def footer():
    s = S(1200, 330, 'Build with purpose. Learn continuously. Ship consistently.', 'Personal motto.')
    s.defs.append('<clipPath id="all"><rect width="1200" height="330" rx="40"/></clipPath>')
    s.add(f'<g clip-path="url(#all)"><rect width="1200" height="330" fill="{BG}"/><g filter="url(#b60)">{aurora([(200,300,250,IND,.55,31,26),(620,340,240,VIO,.4,32,30),(1020,290,260,SKY,.5,33,28),(600,20,160,TEAL,.14,34,24)])}</g></g>')
    grad_text(s, 'fm', [(0, '#ffffff'), (.4, '#ffffff'), (.5, '#a5e3ff'), (.6, '#ffffff'), (1, '#ffffff')], 8, 900)
    for i, t in enumerate(['Build with purpose.', 'Learn continuously.', 'Ship consistently.']):
        s.add(s.reveal(s.text(600, 100 + i*58, t, 46, 700, 'url(#fm)', 'middle', -1.4), .3 + i*.35, 18, 1))
    s.add(s.reveal(s.text(600, 296, 'BUILD IT. BREAK IT. FIX IT. SHIP IT.', 12, 600, 'rgba(226,232,240,.5)', 'middle', 4.2), 1.6, 8, 1))
    s.add('<rect x=".75" y=".75" width="1198.5" height="328.5" rx="40" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="1.5"/>')
    s.render('footer')

if __name__ == '__main__':
    hero()
    header('h-flagship', 'Flagship project', 'Stayza'); header('h-work', 'Selected work', 'Things I have built'); header('h-stack', 'Tech stack', 'What I work with')
    header('h-now', 'Right now', 'Still levelling up'); header('h-activity', 'Activity', 'Contributions'); header('h-connect', 'Connect', 'Let’s build something')
    stayza(); timeline()
    pcard('p-raabta', 400, 'globe', 'Raabta AI', 'Multilingual service marketplace', 'Connects users with service providers. Built with a two-person team at the Google Antigravity National Hackathon.', ['Flutter', 'FastAPI', 'Firebase'], 'Hackathon build', IND, 51)
    pcard('p-jarvis', 400, 'mic', 'JARVIS OS', 'Desktop AI assistant', 'Voice interaction with local processing, built on a modular architecture.', ['Python', 'React', 'Tauri', 'SQLite'], 'Desktop', SKY, 61)
    pcard('p-crime', 400, 'shield', 'Crime Management', 'Law enforcement desktop app', 'A 48-table relational schema, Hibernate ORM mappings, role-based access control and full reporting.', ['Java', 'JavaFX', 'Hibernate', 'MariaDB'], 'Desktop', VIO, 71)
    pcard('p-carrent', 600, 'car', 'CarRent', 'Car rental management system', 'A dual-mode desktop application covering comprehensive rental operations.', ['Qt', 'C++'], 'In progress', TEAL, 81)
    pcard('p-organizer', 600, 'folder', 'Course File Organizer', 'AI-powered academic organizer', 'Classifies, organizes and indexes course documents automatically.', ['Python'], 'In progress', IND, 91)
    stack(); now()
    pill('c-linkedin', 'in', 'LinkedIn', '#0a66c2'); pill('c-email', 'mail', 'Email', '#ea4335'); pill('c-portfolio', 'globe', 'Portfolio', SKY); pill('c-stayza', None, 'stayza.pk', IND, logo=True)
    footer()
