"""Build a self-contained GitHub profile SVG from public data; no dependencies."""
import base64
import datetime as dt
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
USER = 'barsa-dot'
def fetch(url):
    headers = {'User-Agent': 'barsa-profile-dashboard', 'Accept': 'application/vnd.github+json'}
    token = os.environ.get('GH_TOKEN')
    if token and url.startswith('https://api.github.com/'):
        headers['Authorization'] = 'Bearer ' + token
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read()
def api(path):
    return json.loads(fetch('https://api.github.com/' + path))

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.days = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a and 'data-level' in a:
            self.days[a['data-date']] = int(a['data-level'])

def main():
    profile = api('users/' + USER)
    repos = []
    page = 1
    while True:
        batch = api(f'users/{USER}/repos?per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100: break
        page += 1
    owned = [r for r in repos if not r['fork']]
    stars = sum(r['stargazers_count'] for r in owned)
    languages = {}
    for r in owned:
        if r['language']: languages[r['language']] = languages.get(r['language'], 0) + 1
    cal = Calendar()
    cal.feed(fetch(f'https://github.com/users/{USER}/contributions').decode())
    if not cal.days: raise RuntimeError('GitHub calendar unavailable; retaining previous SVG')
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800" role="img" aria-labelledby="title desc">
<title id="title">Barsa's developer terminal</title><desc id="desc">Public GitHub activity, profile statistics and project language distribution.</desc>
<style>text{font-family:'DejaVu Sans Mono',Consolas,monospace}.muted{fill:#82918f}.green{fill:#63edab}.white{fill:#e5f5ef}.label{font-size:12px;letter-spacing:1.4px}.blink{animation:b 1.3s step-end infinite}@keyframes b{50%{opacity:0}}.portrait{animation:p 8s ease-in-out infinite}@keyframes p{0%,100%{opacity:.6}50%{opacity:1}}@media(prefers-reduced-motion:reduce){.blink,.portrait{animation:none}}</style>
<rect width="1000" height="800" rx="20" fill="#0b1113"/><rect x="1" y="1" width="998" height="798" rx="19" fill="none" stroke="#293c36"/>
<path d="M0 46H1000" stroke="#293c36"/><circle cx="25" cy="24" r="5" fill="#f17878"/><circle cx="43" cy="24" r="5" fill="#efce79"/><circle cx="61" cy="24" r="5" fill="#63edab"/>
<text x="500" y="29" text-anchor="middle" class="muted" font-size="12">barsa@github: ~ / developer-terminal</text>
<text x="35" y="85" class="green label">01 / HELLO, WORLD</text>
<text x="35" y="137" class="white" font-size="43" font-weight="bold">I'm Barsa<tspan fill="#63edab">.</tspan></text>
<text x="36" y="169" class="muted" font-size="15">Code. Curiosity. A little bit of chaos.</text>
<rect x="758" y="72" width="207" height="32" rx="16" fill="#10291e" stroke="#28583e"/><circle cx="775" cy="88" r="4" fill="#63edab" class="blink"/><text x="790" y="93" class="green" font-size="11">BUILDING &amp; LEARNING</text>
<text x="35" y="215" class="green label">02 / CONTRIBUTION SIGNAL</text>''']
    def text(x,y,s,cls='white',size=14,extra=''):
        parts.append(f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" {extra}>{html.escape(str(s))}</text>')
    dates = sorted(cal.days)
    start = dt.date.fromisoformat(dates[0]); start -= dt.timedelta(days=(start.weekday()+1)%7)
    colors = ['#182522','#16432d','#236c43','#37a663','#63edab']
    for date in dates:
        d=dt.date.fromisoformat(date); offset=(d-start).days
        x=35+(offset//7)*17.5; y=235+(offset%7)*15
        parts.append(f'<rect x="{x}" y="{y}" width="13" height="11" rx="2" fill="{colors[cal.days[date]]}"><title>{date}: activity level {cal.days[date]}/4</title></rect>')
    text(35,361,dates[0]+' → '+dates[-1], 'muted',11)
    text(965,361,'PUBLIC GITHUB CALENDAR', 'muted',10,'text-anchor="end"')
    parts.append('<path d="M35 385H965" stroke="#293c36"/>')
    # A local avatar asset makes the dashboard independent of external image widgets.
    avatar = base64.b64encode((ROOT/'assets/avatar.png').read_bytes()).decode()
    parts.append(f'<defs><clipPath id="avatar"><rect x="35" y="417" width="265" height="265" rx="12"/></clipPath><filter id="mono"><feColorMatrix type="saturate" values="0"/></filter></defs><image href="data:image/png;base64,{avatar}" x="35" y="417" width="265" height="265" clip-path="url(#avatar)" filter="url(#mono)" class="portrait"/>')
    text(35,709,'BARSA / @barsa-dot','green',13)
    text(335,421,'03 / PUBLIC REPOSITORY SNAPSHOT','green',12)
    metrics=[('REPOSITORIES',profile['public_repos']),('STARS / OWNED REPOS',stars),('FOLLOWERS',profile['followers'])]
    for i,(label,value) in enumerate(metrics):
        x=335+i*213
        parts.append(f'<rect x="{x}" y="441" width="195" height="100" rx="10" fill="#111c1a" stroke="#263c34"/>')
        text(x+17,468,label,'muted',10); text(x+17,518,value,'white',36)
    text(335,576,'REPOSITORIES BY PRIMARY LANGUAGE','muted',11)
    maximum=max(languages.values(),default=1)
    for i,(lang,count) in enumerate(sorted(languages.items(),key=lambda x:-x[1])[:5]):
        y=601+i*23
        text(335,y,lang,'white',12)
        parts.append(f'<rect x="455" y="{y-10}" width="450" height="9" rx="4" fill="#182522"/><rect x="455" y="{y-10}" width="{450*count/maximum}" height="9" rx="4" fill="#63edab"/>')
        text(948,y,count,'muted',12,'text-anchor="end"')
    parts.append('<path d="M35 739H965" stroke="#293c36"/>')
    text(35,771,'$ keep building. keep becoming.','green',13)
    text(965,771,'SYNCED '+dt.datetime.now(dt.timezone.utc).strftime('%d %b %Y / UTC').upper(),'muted',10,'text-anchor="end"')
    parts.append('</svg>')
    (ROOT/'assets/dashboard.svg').write_text('\n'.join(parts))
    print('Generated dashboard from',len(repos),'repos and',len(cal.days),'calendar days')
if __name__=='__main__': main()
