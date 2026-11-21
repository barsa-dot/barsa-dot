from pathlib import Path
import html, math
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
def svg(w,h,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
def text(x,y,s,size=14,c='#392523',weight='normal'):
 return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{c}" font-weight="{weight}">{html.escape(s)}</text>'
def rect(x,y,w,h,c,r=0,stroke='none'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" rx="{r}" stroke="{stroke}"/>'
def header():
 s=rect(0,0,1000,230,'#FFF8ED',20)+rect(0,0,1000,38,'#B52A45',16)
 s+=text(24,25,'BARSA / PERSONAL WORKSPACE',12,'#FFF8ED')+text(826,25,'CREATE · EXPLORE',11,'#F4DC83')
 s+=text(30,102,'Ideas in motion.',41,weight='bold')+text(30,158,'Built one step at a time.',41,weight='bold')
 s+=text(32,202,'Barsarani Sahoo  /  Developer · Student · Storyteller',15)
 s+=rect(782,70,185,112,'#F4DC83',15)+text(799,98,'CURRENT MODE',10)
 s+=text(799,127,'Always learning.',16,weight='bold')+text(799,155,'Open to ideas ↗',12)
 (A/'header.svg').write_text(svg(1000,230,s))
def nav(name,label,kind):
 s=rect(1,1,298,83,'#B52A45',12)
 if kind=='portfolio':
  s+=rect(19,24,34,25,'#F4DC83',4)+rect(28,17,16,9,'none',3,'#F4DC83')
 elif kind=='linkedin':s+=text(19,53,'in',31,'#F4DC83','bold')
 else:
  s+=rect(22,17,27,38,'none',3,'#F4DC83')
  for y in [28,36,44]:s+=rect(28,y,15,2,'#F4DC83')
 s+=text(70,37,label,18,'#FFF8ED','bold')+text(70,61,'LINK COMING SOON' if kind=='resume' else 'OPEN ↗',10,'#F4DC83')
 (A/f'{name}.svg').write_text(svg(300,85,s))
def card(name,title,caption,phase):
 s=rect(1,1,318,238,'#FFF8ED',16,'#DBB6AB')+rect(17,17,286,112,'#F4DC83',12)
 coral='#B52A45';teal='#B52A45'
 if name=='authordna':
  s+=rect(107,30,94,84,'#fffdf8',7)
  for i in range(4):
   width=max(1,min(63,(phase*100-i*14)%90))
   s+=rect(119,46+i*16,width,3,teal,1)
  s+=f'<path d="M207 37L222 52L174 100L156 104L160 87Z" fill="{coral}"/>'
 elif name=='tasknest':
  s+=rect(103,28,116,90,'#fffdf8',8)
  for i in range(3):
   y=47+i*25;s+=rect(116,y-6,13,13,'none',3,teal)+rect(141,y-2,58-i*8,4,teal,2)
   if phase>i/4:s+=f'<path d="M118 {y}l4 4 8-10" fill="none" stroke="{coral}" stroke-width="3"/>'
 else:
  s+=f'<circle cx="149" cy="65" r="26" fill="none" stroke="{teal}" stroke-width="6"/><path d="M169 86l25 25" stroke="{teal}" stroke-width="9" stroke-linecap="round"/>'
  s+=text(140,75,'?',28,coral,'bold')
 s+=text(21,165,title,25,weight='bold')+text(22,191,caption,12)
 s+=text(22,221,'IN DEVELOPMENT' if name=='factcheckai' else 'OPEN LIVE APP ↗',10,teal,'bold')
 return svg(320,240,s)
def toolkit():
 s=rect(1,1,998,259,'#FFF8ED',18,'#DBB6AB')
 s+=text(25,35,'THE TOOLBOX',12,'#B52A45','bold')+text(25,69,'A few things I build with.',28,weight='bold')
 panels=[('01 / LANGUAGES',['C · C++ · Python','JavaScript · TypeScript','SQL']),('02 / FRAMEWORKS',['React · Tailwind CSS','FastAPI · Node.js','Web interfaces & APIs']),('03 / TOOLS',['Git · GitHub · VS Code','From first idea','to working project'])]
 for i,(title,lines) in enumerate(panels):
  x=24+i*325;s+=rect(x,94,303,143,'#F4DC83' if i==1 else '#fffdf8',12,'#DBB6AB')
  s+=text(x+16,121,title,11,'#B52A45','bold')
  for j,line in enumerate(lines):s+=text(x+16,153+j*27,line,15 if j<2 else 12)
 (A/'toolkit.svg').write_text(svg(1000,260,s))
if __name__=='__main__':
 header();nav('portfolio','Portfolio','portfolio');nav('linkedin','LinkedIn','linkedin');nav('resume','Resume','resume');toolkit()
 for name,title,caption in [('authordna','AuthorDNA','Writing meets analysis.'),('tasknest','TaskNest','Plans meet progress.'),('factcheckai','FactCheckAI','Questions meet evidence.')]:
  folder=Path('modular-frames')/name;folder.mkdir(parents=True,exist_ok=True)
  for i in range(24):
   content=card(name,title,caption,(i%18)/18)
   cairosvg.svg2png(bytestring=content.encode(),write_to=str(folder/f'{i:03}.png'))
 print('Rendered independent navigation and project assets')
