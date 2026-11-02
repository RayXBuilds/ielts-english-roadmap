from pathlib import Path
from html import escape
R=Path(__file__).resolve().parent
def text(x,y,s,size=17,anchor='start',color='#172b4d'):
 return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(s)}</text>'
def line(x1,y1,x2,y2,c='#acbac8',width=1,extra=''):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{width}" {extra}/>'
def box(x,y,w,h,label,c='#e6f1fb'):
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="#405770"/>'; a=label.split('|')
 for i,t in enumerate(a):s+=text(x+w/2,y+h/2+6+(i-(len(a)-1)/2)*23,t,16,'middle')
 return s
def save(w,s,h=680):
 p=R/f'W{w:02d}/assets/figure.svg';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="768" height="{768*h/1000}" viewBox="0 0 1000 {h}" role="img"><title>Original Task 1 figure W{w}</title><rect width="1000" height="{h}" fill="white"/>'+s+text(30,h-20,'Original teaching illustration • Fictional data • CC BY 4.0',14)+'</svg>\n')
def generate():
 s=text(30,40,'Evening-course enrolments at a learning centre',25)+text(90,85,'Course enrolments (not necessarily different people)',17)
 for v in range(0,401,100):
  y=520-v*.9;s+=line(100,y,930,y)+text(85,y+5,str(v),16,'end')
 xs=[145,390,635,880]
 for x,year in zip(xs,[2012,2016,2020,2024]):s+=text(x,552,str(year),17,'middle')
 for vals,c,dash,off in [([300,360,330,300],'#205d91','',-15),([150,240,300,390],'#a75b16','stroke-dasharray="9 5"',24),([100,140,140,170],'#337650','stroke-dasharray="3 5"',24)]:
  pts=' '.join(f'{x},{520-v*.9}' for x,v in zip(xs,vals));s+=f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="3" {dash}/>'
  for x,v in zip(xs,vals):s+=f'<circle cx="{x}" cy="{520-v*.9}" r="5" fill="{c}"/>'+text(x,520-v*.9+off,str(v),17,'middle',c)
 for x,l,c,d in [(110,'Languages','#205d91',''),(390,'Computing','#a75b16','stroke-dasharray="9 5"'),(690,'Cookery','#337650','stroke-dasharray="3 5"')]:s+=line(x,610,x+45,610,c,3,d)+text(x+55,616,l,17)
 save(21,s)
 s=text(30,40,'Sorting donated textiles at a community reuse centre',24)
 s+='<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#405770"/></marker></defs>'
 for x,y,w,h,t in [(355,85,290,65,'Receive donations'),(355,200,290,65,'Inspect'),(355,350,290,70,'Repair'),(355,470,290,70,'Recheck after repair'),(30,640,260,70,'Storage'),(30,810,260,75,'Distribute through|reuse programme'),(675,640,290,70,'Assess recycling|eligibility'),(505,810,210,75,'Send to recycler'),(755,810,210,75,'Disposal')]:s+=box(x,y,w,h,t,'#fff0da' if t=='Disposal' else '#e6f1fb')
 arrow='marker-end="url(#a)"'
 for co in [(500,150,500,195),(500,265,500,345),(500,420,500,465),(160,710,160,805)]:s+=line(*co,'#405770',3,arrow)
 for d in ['M355 232 H160 V635','M645 232 H820 V635','M355 505 H320 V600 H200 V635','M645 505 H740 V600 H790 V635','M760 710 V760 H610 V805','M890 710 V805']:
  s+=f'<path d="{d}" fill="none" stroke="#405770" stroke-width="3" {arrow}/>'
 s+=text(175,325,'Directly reusable',17)+text(515,310,'Repairable',17)+text(835,325,'Not repairable',16)
 s+=text(240,575,'Pass',16)+text(750,575,'Fail',16)+text(630,745,'Eligible',16)+text(900,765,'Ineligible',16)
 s+=text(30,930,'No frequency, stage duration or recycler processing method is specified.',16)
 save(22,s,980)
 s=text(30,40,'A riverside area: 2010 and 2025',25)+text(30,75,'North is up • Schematic plans, not to scale',16)
 for year,ox in [(2010,30),(2025,530)]:
  s+=text(ox+220,115,str(year),22,'middle')+f'<rect x="{ox}" y="135" width="440" height="465" fill="#f8f8f3" stroke="#405770"/>'
  s+=f'<rect x="{ox}" y="150" width="440" height="70" fill="#b5def2"/>'+text(ox+260,192,'River',19,'middle')
  s+=box(ox+55,140,45,105,'','#dedbd4')+text(ox+110,144,'Bridge',15)
  s+=box(ox,550,440,50,'Road','#dedbd4')
  if year==2010:
   s+=box(ox+30,285,180,225,'Warehouse','#e6e0d7')+box(ox+260,285,155,225,'Open ground','#f0edda')
  else:
   s+=box(ox+35,350,165,100,'Café +|visitor centre')+box(ox+270,300,155,185,'Garden','#d9ebd4')
   s+=box(ox+280,335,100,50,'Seating','#eff6e9')
   s+=line(ox+77,245,ox+435,245,'#af7928',10)+text(ox+245,278,'Riverside footpath',15,'middle')
   s+=line(ox+405,245,ox+405,550,'#af7928',9)+text(ox+290,525,'Pedestrian link',15)
 s+=text(30,630,'Existing bridge and road retained; new pedestrian routes shown in brown.',16)
 save(23,s)
 s=text(30,40,'Course formats: shares of enrolments and totals',25)+text(100,90,'Share of all course enrolments (%)',18)
 colors=['#205d91','#a75b16','#337650']
 for y,year,vals in [(170,2016,[70,20,10]),(300,2026,[40,35,25])]:
  s+=text(80,y+48,str(year),19,'end');x=110
  for v,c in zip(vals,colors):
   s+=f'<rect x="{x}" y="{y}" width="{v*8}" height="80" fill="{c}"/>'+text(x+v*4,y+48,f'{v}%',20,'middle','white');x+=v*8
 for x,l,c in zip([100,390,670],['Classroom','Online','Blended'],colors):s+=f'<rect x="{x}" y="425" width="22" height="22" fill="{c}"/>'+text(x+33,444,l,18)
 s+=text(100,500,'Year',18)+text(400,500,'Total enrolments',18)+line(100,515,910,515)
 for y,yr,v in [(550,'2016','2,000'),(595,'2026','4,000')]:s+=text(100,y,yr,19)+text(400,y,v,19)
 s+=text(100,630,'Each enrolment has one format; an individual may enrol more than once.',16)
 save(24,s)
if __name__=='__main__':generate()
