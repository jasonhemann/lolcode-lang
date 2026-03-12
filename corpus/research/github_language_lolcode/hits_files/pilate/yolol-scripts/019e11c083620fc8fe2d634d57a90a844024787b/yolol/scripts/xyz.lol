A=1000 n=1000 pr=0 sp=0 div=(9.6+2.4*pr)*n so=1-sp o=160000 e=8*o c=""
z="origin_" mr=z+"north" br=z+"south" cr=z+"east" z+="west" sm="\nS: "
u=e*3/13 l=2*o mm=l*13/19 k=e*3/19 x/=so sm=c s=c sl="\nsignal lost"
rr="ISAN2 :_\n     " xm="\nX: " ym="\nY: " zm="\nZ: " nn=l*13/3
ej=16*sp h="Q" pj=14-pr b=0.5 p=1000000 :at=mr :bt=br :ct=cr :dt=z x=0
t=p-:a t*=t i=p-:b i*=i g=p-:c g*=g f=p-:d f*=f x/=:a*:b*:c*:d goto14
t=p-:a t*=t er=(t-el)/4 el=t x/=:a :at=br x=8 x+=(6-x)*(x<7) gotopj
i=p-:a i*=i fr=(i-fl)/4 fl=i x/=:a :at=cr x=9 x+=(6-x)*(x<7) gotopj
g=p-:a g*=g gr=(g-gl)/4 gl=g x/=:a :at=z x=10 x+=(6-x)*(x<7) gotopj
f=p-:a f*=f hr=(f-hl)/4 hl=f x/=:a :at=mr x=7 x+=(6-x)*(x<7) gotopj
st=:_!=c :_=rr+"\n\n   "+(:at-"origin_")+sl goto 11*(:a==0)*st
st=:_!=c :_=rr+"\n\n can't see\n recievers" goto 12*st
t+=er i+=fr g+=gr f+=hr
:x=(t+i)/e+g/u-f/k :y=i/l-t/mm+(g+f)/nn :z=(g+f-t-i)/o gotoej+x*so

// modified ISAN v2.5 - removes prediction, speed, and ui
// Sets :x, :y, and :z