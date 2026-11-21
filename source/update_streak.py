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
 def txt(x,y,t,size=14,c='#392523',weight='normal'):
  return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{c}" font-weight="{weight}">{html.escape(str(t))}</text>'
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="285" viewBox="0 0 1000 285"><rect width="1000" height="285" rx="18" fill="#FFF8ED"/>'
 s+=txt(25,34,'THE CONSISTENCY CLUB',12,'#B52A45','bold')+txt(25,70,'Showing up is a skill.',29,'#392523','bold')
 for i,(label,value) in enumerate([('CURRENT RUN',current),('BEST RUN IN WINDOW',longest),('ACTIVE DAYS IN WINDOW',active)]):
  x=25+i*325
  color='#B52A45' if i==0 else '#F4DC83'
  ink='#FFF8ED' if i==0 else '#392523'
  s+=f'<rect x="{x}" y="93" width="300" height="119" rx="12" fill="{color}"/>'
  s+=txt(x+18,121,label,10,ink,'bold')+txt(x+18,173,str(value),43,ink,'bold')+txt(x+116,172,'DAYS',12,ink)
  s+=f'<circle cx="{x}" cy="151" r="9" fill="#FFF8ED"/><circle cx="{x+300}" cy="151" r="9" fill="#FFF8ED"/>'
 s+=txt(25,239,'Public contribution calendar · current run includes yesterday if today is unfinished.',11,'#392523')
 s+=txt(25,262,f'Window: {days[0]} to {days[-1]} · refreshed {today.isoformat()} UTC',10,'#392523')
 s+='</svg>'
 (Path(__file__).resolve().parents[1]/'assets/streak.svg').write_text(s)
 print('Current:',current,'Longest in calendar window:',longest,'Active days:',active)
if __name__=='__main__':build()
