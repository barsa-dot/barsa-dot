"""Render a custom streak timeline from GitHub's public contribution calendar."""
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import html
class Calendar(HTMLParser):
 def __init__(self): super().__init__();self.days={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='td' and 'data-date' in a and 'data-level' in a:self.days[a['data-date']]=int(a['data-level'])
def build():
 req=Request('https://github.com/users/barsa-dot/contributions',headers={'User-Agent':'barsa-streak-timeline'})
 with urlopen(req,timeout=30) as r:raw=r.read().decode()
 p=Calendar();p.feed(raw)
 if not p.days:raise RuntimeError('No contribution calendar returned; keeping existing display')
 days=sorted(p.days);today=datetime.now(timezone.utc).date();end=today
 if p.days.get(end.isoformat(),0)==0:end-=timedelta(days=1)
 current=0;d=end
 while p.days.get(d.isoformat(),0)>0:current+=1;d-=timedelta(days=1)
 longest=run=0;previous=None
 for value in days:
  date=datetime.fromisoformat(value).date()
  if p.days[value]>0:run=run+1 if previous and date-previous==timedelta(days=1) else 1
  else:run=0
  longest=max(longest,run);previous=date
 active=sum(v>0 for v in p.days.values())
 def txt(x,y,t,size=14,c='#173e3c',weight='normal'):
  return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{c}" font-weight="{weight}">{html.escape(str(t))}</text>'
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="310" viewBox="0 0 1000 310"><rect x="1" y="1" width="998" height="308" rx="18" fill="#f7f3e9" stroke="#a9c5bc"/>'
 s+=txt(25,35,'THE DAILY THREAD',13,weight='bold')+txt(25,64,'Small steps. A visible trail.',25,weight='bold')
 for i,(label,value) in enumerate([('CURRENT STREAK',current),('LONGEST IN WINDOW',longest),('ACTIVE DAYS IN WINDOW',active)]):
  x=25+i*326;s+=txt(x,98,label,10)+txt(x,143,f'{value} days',31,weight='bold')
 start=today-timedelta(days=27)
 for i in range(28):
  d=start+timedelta(days=i);level=p.days.get(d.isoformat(),0);x=25+i*34
  if i<27:s+=f'<path d="M{x+24} 192h10" stroke="#b5cfc6" stroke-width="2"/>'
  color=['#e2e8df','#c5ded3','#83b9a3','#418779','#174b47'][level]
  s+=f'<rect x="{x}" y="180" width="24" height="24" rx="12" fill="{color}"><title>{d.isoformat()}: {"active" if level else "no public activity"}</title></rect>'
  if i%7==0:s+=txt(x,226,d.strftime('%d %b'),10)
 s+=txt(25,258,'Last 28 days · darker nodes mean more contribution activity.',12)
 s+=txt(25,282,f'Public calendar · window {days[0]} to {days[-1]} · refreshed {today.isoformat()} UTC',10)
 s+='</svg>'
 (Path(__file__).resolve().parents[1]/'assets/streak.svg').write_text(s)
 print('Current:',current,'Longest in calendar window:',longest,'Active days:',active)
if __name__=='__main__':build()
