#!/usr/bin/env python3
"""Profile SVGs: retrofuturist horizon + liquid-glass lens + neumorphic cards.
System fonts only (zero font bytes), no large blur filters, CSS opacity/transform animation only.
Run: python3 build_assets.py  ->  ../assets/*.svg"""
import html, os, textwrap
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'); os.makedirs(O, exist_ok=True)
F = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,Helvetica,Arial,sans-serif"
X = html.escape
BG, INK, MUT, HOT = '#0b0c10', '#f5f5f7', 'rgba(245,245,247,.62)', '#ff7a59'
def st(*a): return ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{p}"/>' for o, c, p in a)
D = (f'<linearGradient id="s" x1="0" y1="0" x2="1" y2="1">{st((0,"#1c1f27",1),(1,"#111319",1))}</linearGradient>'
     f'<linearGradient id="w" x1="0" y1="0" x2="1" y2="1">{st((0,"#0a0b0f",1),(1,"#181b22",1))}</linearGradient>'
     f'<linearGradient id="e" x1="0" y1="0" x2="1" y2="1">{st((0,"#fff",.45),(.5,"#fff",.04),(1,"#fff",.2))}</linearGradient>'
     f'<linearGradient id="a" x1="0" y1="0" x2="0" y2="1">{st((0,"#ffc371",1),(.5,"#ff5e8a",1),(1,"#7c5cff",1))}</linearGradient>'
     f'<radialGradient id="g">{st((0,"#ff5e8a",.55),(1,"#ff5e8a",0))}</radialGradient>'
     '<filter id="n" x="-8%" y="-8%" width="120%" height="125%"><feDropShadow dx="-5" dy="-5" stdDeviation="6" flood-color="#303542" flood-opacity=".5"/>'
     '<feDropShadow dx="7" dy="8" stdDeviation="8" flood-color="#000" flood-opacity=".75"/></filter>')
K = ('@keyframes tw{50%{opacity:.2}}.t{animation:tw 5s ease-in-out infinite}'
     '@keyframes up{from{opacity:0;transform:translateY(14px)}}.u{animation:up .9s cubic-bezier(.16,1,.3,1) both}'
     '@keyframes fl{from{transform:translateY(0);opacity:0}20%{opacity:1}to{transform:translateY(var(--d,200px));opacity:.15}}.f{animation:fl 4s cubic-bezier(.55,0,1,1) infinite}'
     '@keyframes br{50%{opacity:.55}}.b{animation:br 6s ease-in-out infinite}'
     '@keyframes rp{from{transform:scale(.4);opacity:.8}to{transform:scale(1.7);opacity:0}}.rp{transform-box:fill-box;transform-origin:center;animation:rp 3.6s ease-out infinite}'
     '@keyframes rt{to{transform:rotate(360deg)}}.rt{transform-box:fill-box;transform-origin:center;animation:rt 20s linear infinite}'
     '@keyframes eq{50%{transform:scaleY(.3)}}.eq{transform-box:fill-box;transform-origin:center;animation:eq 1.2s ease-in-out infinite}'
     '@keyframes rl{to{transform:translateX(-40px)}}.rl{animation:rl 1s linear infinite}'
     '@keyframes sd{0%{transform:translateX(0);opacity:1}55%{transform:translateX(300px);opacity:1}70%,100%{transform:translateX(300px);opacity:0}}.sd{animation:sd 4s ease-in-out infinite}'
     '@keyframes hv{50%{transform:translateY(-4px)}}.hv{animation:hv 5s ease-in-out infinite}'
     '@keyframes gr{from{transform:scaleX(0)}}.gr{transform-box:fill-box;transform-origin:left;animation:gr 2s cubic-bezier(.5,0,.2,1) .4s both}'
     '@keyframes pp{from{opacity:0;transform:scale(.3)}}.pp{transform-box:fill-box;transform-origin:center;animation:pp .6s cubic-bezier(.3,1.5,.5,1) both}'
     '@keyframes sl{from{transform:translateX(0);opacity:0}15%{opacity:1}to{transform:translateX(750px);opacity:0}}.sl{animation:sl 4s ease-in-out 2.4s infinite}'
     '.sh{animation:sw 10s ease-in-out infinite}@keyframes sw{0%,55%{transform:translateX(-200px) skewX(-20deg)}100%{transform:translateX(1100px) skewX(-20deg)}}'
     '.d{stroke-dasharray:1 1;animation:dr 6s ease-in-out infinite}@keyframes dr{0%{stroke-dashoffset:1}35%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:1}}')

def svg(n, w, h, t, body, defs=''):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{X(t)}"><title>{X(t)}</title>'
         f'<style>text{{font-family:{F}}}{K}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style><defs>{D}{defs}</defs>{body}</svg>')
    open(f'{O}/{n}.svg', 'w').write(s); print(f'{n}.svg {len(s)/1024:.1f} KB')
def T(x, y, t, sz, wt=400, f=INK, a='start', ls=0):
    return f'<text x="{x}" y="{y}" font-size="{sz}" font-weight="{wt}" fill="{f}" text-anchor="{a}" letter-spacing="{ls}">{X(t)}</text>'
def card(x, y, w, h, r=32, sf='s'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{sf})" filter="url(#n)"/>'
            f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="url(#e)" stroke-opacity=".5"/>')
def well(x, y, w, h, r=22):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#w)"/>'
            f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="#fff" stroke-opacity=".06"/>')
def grid(y0, y1, cx=600, w=1200):
    v = ''.join(f'<path d="M{cx+i*36} {y0}L{cx+i*170} {y1}"/>' for i in range(-17, 18))
    h = ''.join(f'<path class="f" style="animation-delay:-{k*.57:.2f}s" d="M0 {y0}H{w}"/>' for k in range(7))
    return f'<g stroke="#ff4f9a" stroke-opacity=".38" stroke-width="1.2" fill="none" style="--d:{y1-y0}px">{v}{h}</g>'

def hero():
    bars = ''.join(f'<rect x="420" y="{350+i*i*1.3+i*4:.0f}" width="360" height="{2+i*1.2:.1f}"/>' for i in range(1, 7))
    stars = ''.join(f'<circle class="t" cx="{(i*263+40)%1160}" cy="{(i*97)%240+14}" r="1.3" fill="#fff" style="animation-delay:{i*.37:.1f}s"/>' for i in range(18))
    cx, cy, cw, ch = 140, 50, 920, 290
    u = lambda t, a: f'<g class="u" style="animation-delay:{a}s">{t}</g>'
    d = (f'<linearGradient id="k" x1="0" y1="0" x2="0" y2="1">{st((.25,BG,1),(1,"#4a1646",1))}</linearGradient>'
         f'<linearGradient id="h" x1="0" y1="0" x2="0" y2="1">{st((0,"#fff",.18),(.5,"#fff",0))}</linearGradient>'
         f'<linearGradient id="hs">{st((0,"#fff",0),(.5,"#fff",.1),(1,"#fff",0))}</linearGradient>'
         f'<linearGradient id="c2" x1="0" y1="0" x2="0" y2="1">{st((0,"#fff",1),(1,"#aeb3c4",1))}</linearGradient>'
         f'<mask id="m"><rect width="1200" height="600" fill="#fff"/><g fill="#000">{bars}</g></mask>'
         '<clipPath id="o"><rect width="1200" height="600" rx="36"/></clipPath>'
         f'<clipPath id="c"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="48"/></clipPath>')
    glass = (f'<g clip-path="url(#c)"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="{BG}" fill-opacity=".5"/>'
             f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="url(#h)"/><rect class="sh" x="{cx}" y="{cy}" width="120" height="{ch}" fill="url(#hs)"/></g>'
             f'<rect x="{cx+.75}" y="{cy+.75}" width="{cw-1.5}" height="{ch-1.5}" rx="48" fill="none" stroke="url(#e)" stroke-width="1.5"/>')
    b = (f'<g clip-path="url(#o)"><rect width="1200" height="600" fill="{BG}"/><rect width="1200" height="430" fill="url(#k)"/>{stars}'
         '<ellipse class="b" cx="600" cy="430" rx="560" ry="150" fill="url(#g)"/><circle class="hv" cx="600" cy="430" r="170" fill="url(#a)" mask="url(#m)"/>'
         f'<path d="M0 430L90 396L170 422L260 376L350 430ZM850 430L930 384L1010 414L1090 372L1200 430Z" fill="{BG}"/>'
         f'<rect y="430" width="1200" height="170" fill="{BG}"/>{grid(430, 600)}<path d="M0 430H1200" stroke="#ff7aa8" stroke-opacity=".7"/>'
         + u(glass, 0) + u(T(600, 162, 'Abdul Rehman', 88, 700, 'url(#c2)', 'middle', -3), .3)
         + u(T(600, 214, 'I build full stack products, end to end, and take them to production.', 24, 400, 'rgba(245,245,247,.78)', 'middle'), .5)
         + u('<rect x="260" y="246" width="680" height="1" fill="#fff" fill-opacity=".14"/>' + T(600, 286, 'Founder & CEO, Stayza · BS Computer Science, NUST · Islamabad, Pakistan', 17, 500, 'rgba(245,245,247,.9)', 'middle'), .7) + '</g>')
    svg('hero', 1200, 600, 'Abdul Rehman: Founder & CEO of Stayza, Computer Science student at NUST. I build full stack products, end to end, and take them to production.', b, d)

def stayza():
    b = card(10, 10, 1180, 490, 44)
    b += ('<path class="d" d="M56 18C56 10 20 10 20 28C20 44 60 44 60 62C60 72 40 76 24 70" pathLength="1" transform="translate(70 52)" fill="none" stroke="url(#a)" stroke-width="6" stroke-linecap="round"/>'
          + T(150, 98, 'Stayza', 34, 700, INK, ls=-.8) + T(150, 126, 'Student hostel discovery platform', 16, 500, MUT)
          + '<g class="u" style="animation-delay:.2s">' + T(64, 204, 'Discover verified accommodation', 42, 700, INK, ls=-1.2) + T(64, 252, 'with confidence, transparency, and ease.', 42, 700, 'rgba(245,245,247,.45)', ls=-1.2) + '</g>')
    for i, (n, l, d) in enumerate([('2', 'tier verification', 'Identity and location checks plus a live video call.'), ('0%', 'commission', 'Owners and students connect directly.'), ('8', 'cities', 'Lahore, Karachi, Islamabad, Rawalpindi and more.')]):
        x = 64 + i * 368
        b += f'<g class="u" style="animation-delay:{.4+i*.15}s">' + well(x, 284, 352, 104) + T(x + 28, 340, n, 46, 700, 'url(#a)', ls=-1) + T(x + 100, 322, l, 18, 600)
        for j, ln in enumerate(textwrap.wrap(d, 32)): b += T(x + 100, 344 + j * 18, ln, 13, 400, MUT)
        b += '</g>'
    b += '<rect x="100" y="434" width="1000" height="3" fill="url(#w)"/><rect class="gr" x="100" y="434" width="750" height="3" fill="url(#a)"/><circle class="sl" cx="100" cy="435.5" r="5" fill="#fff"/>'
    for i, (y_, l) in enumerate([('2024–25', 'Ideation and validation'), ('Mid 2025', 'Platform architecture'), ('Early 2026', 'Launch'), ('Next', 'National expansion')]):
        x = 100 + i * 333.3
        b += f'<circle class="pp" style="animation-delay:{.6+i*.5}s" cx="{x:.0f}" cy="436" r="7" fill="{BG if i == 3 else "#ffc371"}" stroke="#ff5e8a" stroke-width="2"/>' + T(f'{x:.0f}', 466, y_, 14, 600, INK, 'middle') + T(f'{x:.0f}', 486, l, 13, 400, MUT, 'middle')
    svg('stayza', 1200, 510, 'Stayza: student hostel discovery platform. Two-tier verification, zero commission, 8 cities. Timeline: ideation 2024 to 2025, architecture mid 2025, launch early 2026, national expansion next.', b)

G = {'a': '<circle cx="-5" r="9"/><circle cx="5" r="9"/>', 'b': '<circle r="11"/><circle r="4"/>', 'c': '<path d="M0-12L10-8V2C10 8 4 12 0 14C-4 12-10 8-10 2V-8Z"/>',
     'd': '<path d="M-12 4V-2L-8-8H6L12-2V4Z"/><circle cx="-6" cy="6" r="2.5"/><circle cx="6" cy="6" r="2.5"/>', 'e': '<path d="M-12-8H-3L0-5H12V10H-12Z"/>'}
# one scene per project: Raabta = liquid glass, JARVIS = retro HUD, Crime = blueprint, CarRent = road illustration, Organizer = neumorphic files
def sc_raabta(sw, c):
    o = ''.join(f'<circle cx="{sw*f:.0f}" cy="32" r="{r}" fill="url(#x)" fill-opacity=".3" stroke="#fff" stroke-opacity=".4"/>' for f, r in [(.3, 22), (.5, 26), (.7, 22)])
    return o + ''.join(f'<circle class="rp" style="animation-delay:{k*1.8}s" cx="{sw*.5:.0f}" cy="32" r="26" fill="none" stroke="{c}" stroke-width="1.5"/>' for k in (0, 1))
def sc_jarvis(sw, c):
    m, bars = sw / 2, ''
    for i in range(12):
        x = 14 + i * (sw - 28) / 11
        if abs(x - m) > 36:
            h = 10 + (i * 7 % 4) * 8
            bars += f'<rect class="eq" style="animation-delay:{i*.11:.2f}s" x="{x:.0f}" y="{32-h/2}" width="3" height="{h}" rx="1.5" fill="{c}"/>'
    return (bars + f'<circle class="rt" cx="{m}" cy="32" r="24" fill="none" stroke="url(#x)" stroke-width="2" stroke-dasharray="3 5"/>'
            f'<circle cx="{m}" cy="32" r="14" fill="none" stroke="{c}" stroke-opacity=".5"/><circle class="b" cx="{m}" cy="32" r="7" fill="url(#x)"/>')
def sc_crime(sw, c):
    P = [(.12, 22), (.32, 44), (.52, 18), (.72, 44), (.9, 22)]
    o = f'<polyline points="{" ".join(f"{sw*f:.0f},{y}" for f, y in P)}" fill="none" stroke="{c}" stroke-opacity=".5" stroke-dasharray="3 3"/>'
    for i, (f, y) in enumerate(P):
        cl = 'class="t" ' if i == 2 else ''
        o += f'<rect {cl}x="{sw*f-10:.0f}" y="{y-7}" width="20" height="14" rx="3" fill="#101a33" stroke="url(#x)"/>'
    return o
def sc_car(sw, c):
    return (f'<circle cx="{sw*.85:.0f}" cy="30" r="15" fill="url(#x)" fill-opacity=".85"/><rect y="44" width="{sw}" height="20" fill="#120d0a"/>'
            f'<g class="rl"><path d="M0 54H{sw+80}" stroke="{c}" stroke-width="2" stroke-dasharray="18 22"/></g>'
            f'<g class="hv"><g transform="translate({sw*.45:.0f} 8)"><path d="M0 36H46V28L38 20H16L8 28H0Z" fill="#1c1410" stroke="url(#x)" stroke-width="2" stroke-linejoin="round"/>'
            f'<circle cx="11" cy="37" r="5" fill="#0b0c10" stroke="{c}" stroke-width="2"/><circle cx="35" cy="37" r="5" fill="#0b0c10" stroke="{c}" stroke-width="2"/></g></g>')
def sc_org(sw, c):
    fo = ''.join(f'<path transform="translate({sw-150+k*46} 22)" d="M0 8H10L13 5H32V34H0Z" fill="#0f2a1e" stroke="{c}" stroke-opacity="{.9 if k == 1 else .4}" stroke-width="1.5"/>' for k in range(3))
    sh = ''.join(f'<g class="sd" style="animation-delay:{k*1.3}s"><rect x="40" y="18" width="20" height="26" rx="4" fill="url(#x)"/><path d="M45 26H55M45 32H52" stroke="#0b0c10" stroke-opacity=".5" stroke-linecap="round"/></g>' for k in range(3))
    return fo + sh
TH = {'p-raabta': ('#5eead4', '#22d3ee', '#6366f1', '#0d2a30', sc_raabta), 'p-jarvis': ('#7dd3fc', '#38bdf8', '#2563eb', '#0c1a30', sc_jarvis),
      'p-crime': ('#fbbf24', '#f59e0b', '#ef4444', '#111b38', sc_crime), 'p-carrent': ('#fde047', '#fb923c', '#ef4444', '#2c1a10', sc_car),
      'p-organizer': ('#86efac', '#34d399', '#059669', '#0f2a1e', sc_org)}
def pcard(n, w, g, title, sub, desc, tags, status):
    c1, c2, c3, tint, sc = TH[n]; sw = w - 154
    d = (f'<linearGradient id="x" x1="0" y1="0" x2="0" y2="1">{st((0,c1,1),(.5,c2,1),(1,c3,1))}</linearGradient>'
         f'<linearGradient id="y" x1="0" y1="0" x2="1" y2="1">{st((0,tint,1),(1,"#0f1116",1))}</linearGradient>'
         '<pattern id="bp" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#fff" fill-opacity=".14"/></pattern>'
         f'<clipPath id="q"><rect width="{sw}" height="64" rx="18"/></clipPath>')
    b = card(8, 8, w - 16, 288, 30, 'y') + well(36, 36, 64, 64, 20)
    b += f'<g class="hv"><g transform="translate(68 68)" fill="none" stroke="url(#x)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{G[g]}</g></g>'
    b += f'<g transform="translate(118 36)">{well(0, 0, sw, 64, 18)}<g clip-path="url(#q)"><rect width="{sw}" height="64" fill="url(#bp)"/>{sc(sw, c1)}</g></g>'
    b += T(36, 140, title, 26, 700, ls=-.6) + T(36, 166, sub, 14, 500, c2)
    for i, l in enumerate(textwrap.wrap(desc, int((w - 72) / 7.1))[:3]): b += T(36, 196 + i * 20, l, 14, 400, MUT)
    svg(n, w, 304, f'{title}: {sub}. {desc}', '<g class="u">' + b + T(36, 270, ' · '.join(tags), 13, 500, c1) + '</g>', d)

def btn(n, label):
    svg(n, 300, 84, label, '<g class="u">' + card(8, 8, 284, 68, 24) + T(34, 49, label, 18, 600, ls=-.2) + T(264, 49, '↗', 18, 400, MUT, 'end') + '</g>')

def footer():
    b = ('<g clip-path="url(#o)">' f'<rect width="1200" height="220" fill="{BG}"/><ellipse cx="600" cy="110" rx="520" ry="90" fill="url(#g)"/>{grid(110, 220)}'
         '<path d="M0 110H1200" stroke="#ff7aa8" stroke-opacity=".6"/>' + T(600, 84, 'Build with purpose. Learn continuously. Ship consistently.', 34, 700, 'url(#a)', 'middle', -1) + '</g>')
    svg('footer', 1200, 220, 'Build with purpose. Learn continuously. Ship consistently.', b, '<clipPath id="o"><rect width="1200" height="220" rx="36"/></clipPath>')

if __name__ == '__main__':
    hero(); stayza(); footer()
    pcard('p-raabta', 400, 'a', 'Raabta AI', 'Multilingual service marketplace', 'Connects users with service providers. Built with a two-person team at the Google Antigravity National Hackathon.', ['Flutter', 'FastAPI', 'Firebase'], 'Hackathon build')
    pcard('p-jarvis', 400, 'b', 'JARVIS OS', 'Desktop AI assistant', 'Voice interaction with local processing, built on a modular architecture.', ['Python', 'React', 'Tauri', 'SQLite'], 'Desktop')
    pcard('p-crime', 400, 'c', 'Crime Management', 'Law enforcement desktop app', 'A 48-table relational schema, Hibernate ORM mappings, role-based access control and full reporting.', ['Java', 'JavaFX', 'Hibernate', 'MariaDB'], 'Desktop')
    pcard('p-carrent', 600, 'd', 'CarRent', 'Car rental management system', 'A dual-mode desktop application covering comprehensive rental operations.', ['Qt', 'C++'], 'In progress')
    pcard('p-organizer', 600, 'e', 'Course File Organizer', 'AI-powered academic organizer', 'Classifies, organizes and indexes course documents automatically.', ['Python'], 'In progress')
    for n, l in [('c-linkedin', 'LinkedIn'), ('c-email', 'Email'), ('c-portfolio', 'Portfolio'), ('c-stayza', 'stayza.pk')]: btn(n, l)
