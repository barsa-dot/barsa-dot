from pathlib import Path
import html, math
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
def svg(w,h,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
def text(x,y,s,size=14,c='#173e3c',weight='normal'):
 return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{c}" font-weight="{weight}">{html.escape(s)}</text>'
def rect(x,y,w,h,c,r=0,stroke='none'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" rx="{r}" stroke="{stroke}"/>'
def header():
 s=rect(0,0,1000,230,'#f7f3e9',20)+rect(0,0,1000,38,'#174b47',16)
 s+=text(24,25,'BARSA / PERSONAL WORKSPACE',12,'#f7f3e9')+text(826,25,'CREATE · EXPLORE',11,'#b4d5cd')
 s+=text(30,102,'Ideas in motion.',41,weight='bold')+text(30,158,'Built one step at a time.',41,weight='bold')
 s+=text(32,202,'Barsarani Sahoo  /  Developer · Student · Storyteller',15)
 s+=rect(782,70,185,112,'#e5ede6',15)+text(799,98,'CURRENT MODE',10)
 s+=text(799,127,'Always learning.',16,weight='bold')+text(799,155,'Open to ideas ↗',12)
 (A/'header.svg').write_text(svg(1000,230,s))
def nav(name,label,kind):
 s=rect(1,1,298,83,'#174b47',12)
 if kind=='portfolio':
  s+=rect(19,24,34,25,'#f6a58f',4)+rect(28,17,16,9,'none',3,'#f6a58f')
 elif kind=='linkedin':s+=text(19,53,'in',31,'#f6a58f','bold')
 else:s+=text(17,51,'</>',24,'#f6a58f','bold')
 s+=text(70,37,label,18,'#f7f3e9','bold')+text(70,61,'OPEN ↗',10,'#b4d5cd')
 (A/f'{name}.svg').write_text(svg(300,85,s))
def card(name,title,caption,phase):
 s=rect(1,1,318,238,'#f7f3e9',16,'#a9c5bc')+rect(17,17,286,112,'#e5ede6',12)
 coral='#ed947e';teal='#174b47'
 if name=='authordna':
  s+=rect(107,30,94,84,'#fffdf6',7)
  for i in range(4):
   width=max(1,min(63,(phase*100-i*14)%90))
   s+=rect(119,46+i*16,width,3,teal,1)
  s+=f'<path d="M207 37L222 52L174 100L156 104L160 87Z" fill="{coral}"/>'
 elif name=='tasknest':
  s+=rect(103,28,116,90,'#fffdf6',8)
  for i in range(3):
   y=47+i*25;s+=rect(116,y-6,13,13,'none',3,teal)+rect(141,y-2,58-i*8,4,teal,2)
   if phase>i/4:s+=f'<path d="M118 {y}l4 4 8-10" fill="none" stroke="{coral}" stroke-width="3"/>'
 else:
  s+=f'<circle cx="149" cy="65" r="26" fill="none" stroke="{teal}" stroke-width="6"/><path d="M169 86l25 25" stroke="{teal}" stroke-width="9" stroke-linecap="round"/>'
  s+=text(140,75,'?',28,coral,'bold')
 s+=text(21,165,title,25,weight='bold')+text(22,191,caption,12)
 s+=text(22,221,'IN DEVELOPMENT' if name=='factcheckai' else 'OPEN LIVE APP ↗',10,teal,'bold')
 return svg(320,240,s)
if __name__=='__main__':
 header();nav('portfolio','Portfolio','portfolio');nav('linkedin','LinkedIn','linkedin');nav('github','GitHub','github')
 for name,title,caption in [('authordna','AuthorDNA','Writing meets analysis.'),('tasknest','TaskNest','Plans meet progress.'),('factcheckai','FactCheckAI','Questions meet evidence.')]:
  folder=Path('modular-frames')/name;folder.mkdir(parents=True,exist_ok=True)
  for i in range(24):
   content=card(name,title,caption,(i%18)/18)
   cairosvg.svg2png(bytestring=content.encode(),write_to=str(folder/f'{i:03}.png'))
 print('Rendered independent navigation and project assets')
