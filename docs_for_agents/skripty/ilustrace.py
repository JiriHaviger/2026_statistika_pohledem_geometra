# Ilustrace principu pro osobnosti bez volného portrétu (světlá a tmavá varianta, jpg do assets/portrety/).
# Spuštění z kořene projektu: python docs_for_agents/skripty/ilustrace.py light  a  ... dark
# Potřebuje matplotlib a numpy (pip install matplotlib). Barvy odpovídají $jh-* v hag_custom.scss a hag_dark.scss.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sys
MODE=sys.argv[1] if len(sys.argv)>1 else "light"
if MODE=="dark":
    PR="#5B9BD0"; AC="#E0903F"; CX="#9A9A9A"; TX="#E4E4E4"; BG="#1B1D20"; SUF="-dark"
else:
    PR="#4682B4"; AC="#C46F26"; CX="#7F7F7F"; TX="#3D3D3D"; BG="#FFFFFF"; SUF=""
OUT="assets/portrety/"
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":TX,"axes.labelcolor":TX,"xtick.color":TX,"ytick.color":TX,"axes.edgecolor":CX,"figure.facecolor":BG,"axes.facecolor":BG})
def save(fig,name):
    fig.savefig(OUT+name.replace(".jpg",SUF+".jpg"),dpi=100,format="jpg",facecolor=BG,pil_kwargs={"quality":88}); plt.close(fig)
data=np.array([1,2,2,2,3,3,4,5,8,11])

# Stevens: čtyři úrovně měření
fig,ax=plt.subplots(figsize=(3.4,2.6)); ax.axis("off")
rows=[("nominální","rovnost"),("ordinální","+ pořadí"),("intervalová","+ rozdíly"),("poměrová","+ podíly")]
for i,(n,t) in enumerate(rows):
    y=3-i
    ax.barh(y,1.6+i*0.6,height=0.6,color=PR,left=0.0)
    ax.text(0.08,y,n,va="center",color="white",fontsize=9,fontweight="bold")
    ax.text(1.6+i*0.6+0.1,y,t,va="center",fontsize=9)
ax.set_xlim(0,5.0); ax.set_ylim(-0.6,3.8)
ax.set_title("Čtyři úrovně měření",fontsize=10,color=TX)
save(fig,"stevens-urovne-mereni.jpg")

# Sturges: histogram s k = 4 třídami
fig,ax=plt.subplots(figsize=(3.4,2.6))
k=int(np.floor(1+np.log2(len(data))))
ax.hist(data,bins=k,color=PR,edgecolor="white")
ax.set_title(f"n = 10 → k = ⌊1 + log₂ 10⌋ = {k} třídy",fontsize=10)
ax.set_xlabel("počet vozidel",fontsize=9); ax.set_ylabel("četnost",fontsize=9)
for s_ in ("top","right"): ax.spines[s_].set_visible(False)
fig.tight_layout(); save(fig,"sturges-histogram.jpg")

# Tukey: krabicový graf
fig,ax=plt.subplots(figsize=(3.4,2.0))
q1,med,q3=2,3,4.75
ax.add_patch(plt.Rectangle((q1,0.3),q3-q1,0.4,facecolor=PR,edgecolor=PR,alpha=0.35))
ax.plot([med,med],[0.3,0.7],color=PR,lw=2.5)
ax.plot([1,q1],[0.5,0.5],color=PR,lw=1.5); ax.plot([q3,8],[0.5,0.5],color=PR,lw=1.5)
for x in (1,8): ax.plot([x,x],[0.4,0.6],color=PR,lw=1.5)
ax.plot([11],[0.5],"o",color=AC)
ax.text(11,0.78,"odlehlá",ha="center",fontsize=8,color=AC)
ax.set_ylim(0,1); ax.set_xlim(0,12); ax.set_yticks([])
ax.set_xlabel("počet vozidel",fontsize=9)
for s_ in ("top","right","left"): ax.spines[s_].set_visible(False)
ax.set_title("Box-plot",fontsize=10)
fig.tight_layout(); save(fig,"tukey-boxplot.jpg")

# Graunt: tabulka četností
fig,ax=plt.subplots(figsize=(3.4,2.6)); ax.axis("off")
xs=[1,2,3,4,5,8,11]; ns=[1,3,2,1,1,1,1]; Fs=np.cumsum(ns)
ax.set_xlim(0,3); ax.set_ylim(-0.3,len(xs)+1.3)
for j,h in enumerate(["x","n","F"]):
    ax.text(0.5+j,len(xs)+0.5,h,ha="center",va="center",fontweight="bold",color=PR,fontsize=10)
ax.plot([0.1,2.9],[len(xs)+0.05]*2,color=CX,lw=0.8)
for i,(x,n,F) in enumerate(zip(xs,ns,Fs)):
    y=len(xs)-1-i+0.5
    for j,v in enumerate([x,n,F]): ax.text(0.5+j,y,str(v),ha="center",va="center",fontsize=9)
ax.set_title("Tabulka četností",fontsize=10)
save(fig,"graunt-tabulka.jpg")
