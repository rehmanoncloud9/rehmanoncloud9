import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR=48000; DUR=30.0; N=int(SR*DUR); BPM=128; B=60/BPM
def bt(bar,beat=0): return (bar*4+beat)*B
rng=np.random.default_rng(11)
bus={k:np.zeros((N,2)) for k in ('drums','duck','music','lead','sfx')}; send=np.zeros((N,2))
def ta(d): return np.arange(int(d*SR))/SR
def mtof(m): return 440*2**((m-69)/12)
def lp(x,f,o=2): return sosfilt(butter(o,min(f,SR/2-200),'lowpass',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,'highpass',fs=SR,output='sos'),x,axis=0)
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'bandpass',fs=SR,output='sos'),x,axis=0)
def put(name,x,t0,g=1.0,pan=0.0,rev=0.0):
    i=int(round(t0*SR))
    if i>=N or i<0: return
    x=x[:N-i].copy(); fo=min(len(x),int(.01*SR)); r=np.linspace(1,0,fo)
    if x.ndim==1:
        x[-fo:]*=r; a=(pan+1)*np.pi/4; x=np.stack([x*np.cos(a),x*np.sin(a)],1)*1.414
    else: x[-fo:]*=r[:,None]
    bus[name][i:i+len(x)]+=x*g
    if rev: send[i:i+len(x)]+=x*g*rev
def kick():
    t=ta(.42); f=46+95*np.exp(-t/.035)
    body=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.2); click=np.sin(2*np.pi*1500*t)*np.exp(-t/.002)*.1
    return lp(np.tanh((body+click)*1.3),6000)*.9
def clap():
    t=ta(.35); n=bp(rng.standard_normal(len(t)),1100,3200); env=np.exp(-t/.06)*.8
    for k in (0,.009,.018): env+=.7*np.exp(-np.maximum(t-k,0)/.004)*(t>=k)
    return lp(n*env*.55+np.sin(2*np.pi*190*t)*np.exp(-t/.03)*.5,7000)*.5
def hat(open_=False):
    t=ta(.12 if open_ else .05); n=lp(hp(rng.standard_normal(len(t)),8500,4),14000)
    return n*np.exp(-t/(.045 if open_ else .012))*.5
def bass(m,d):
    t=ta(d); f=mtof(m); x=np.sin(2*np.pi*f*t)+.35*np.sin(4*np.pi*f*t)+.12*np.sin(6*np.pi*f*t)
    return lp(np.tanh(x*1.3)*np.minimum(1,t/.004)*np.exp(-t/.22),900)*.55
def pluck_chord(notes,d=.45,bright=1.0):
    t=ta(d); x=np.zeros(len(t))
    for m in notes:
        for n in range(1,7): x+=(.7**n)/n*np.sin(2*np.pi*mtof(m)*n*t)*np.exp(-t/(.16/n**.4))
    return lp(x*np.minimum(1,t/.003),3500*bright)*.16
def pad(notes,d,att=.4,rel=.4,cut=2200):
    t=ta(d); Lc=np.zeros(len(t)); Rc=np.zeros(len(t))
    for m in notes:
        for k,det in enumerate((-.004,0,.0045)):
            ph=2*np.pi*mtof(m)*(1+det)*t+k*1.3; v=np.sin(ph)+.35*np.sin(2*ph)+.15*np.sin(3*ph)
            if k==0: Lc+=v
            elif k==2: Rc+=v
            else: Lc+=.5*v; Rc+=.5*v
    env=np.minimum(1,t/att)*np.clip((d-t)/rel,0,1)
    return lp(np.stack([Lc,Rc],1),cut)*env[:,None]*.02
def piano(m,d=2.5,vel=.6):
    t=ta(d); f0=mtof(m); x=np.zeros(len(t))
    for n in range(1,9):
        fn=f0*n*np.sqrt(1+.0003*n*n)
        if fn>15000: break
        x+=vel**(1+n*.25)/n**1.3*np.sin(2*np.pi*fn*t)*np.exp(-t/(2.2/n**.75))
    return lp(x*np.minimum(1,t/.004),2500+5000*vel)*.3
def bell(m,d=1.2,g=1.0):
    t=ta(d); f=mtof(m); mod=np.sin(2*np.pi*f*3.5*t)*1.2*np.exp(-t/.08)
    return (np.sin(2*np.pi*f*t+mod)*np.exp(-t/.5)+.25*np.sin(4*np.pi*f*t)*np.exp(-t/.2))*np.minimum(1,t/.002)*.14*g
def lead(m,d=.6):
    t=ta(d); f=mtof(m); x=np.sin(2*np.pi*f*t+.8*np.sin(4*np.pi*f*t)*np.exp(-t/.15))
    return x*np.minimum(1,t/.003)*np.exp(-t/.28)*.13
def popsnd(f0=900,g=1.0):
    t=ta(.14); f=f0*(.55+.45*np.exp(-t/.018))
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.035)*np.minimum(1,t/.001)*.35*g
def keytick():
    t=ta(.025); return np.sin(2*np.pi*(2800+rng.random()*1400)*t)*np.exp(-t/.003)*.12
def sub_boom(f0=44,d=2.0):
    t=ta(d); f=f0*(1+.8*np.exp(-t/.05)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.7)*np.minimum(1,t/.003)*.9
def swell(notes,d):
    x=pad(notes,d,att=.02,rel=.02,cut=5000)[::-1]; return x*(np.linspace(0,1,len(x))**2.5)[:,None]*3
def sweep_up(d,f0=300,f1=3000):
    t=ta(d); f=f0*(f1/f0)**(t/d); return (np.sin(2*np.pi*np.cumsum(f)/SR)+.3*np.sin(2*np.pi*np.cumsum(f*1.5)/SR))*(t/d)**2*.07

CH={'D':[62,66,69,73],'A':[61,64,69,71],'Bm':[62,66,69,71],'G':[62,66,67,71]}
ROOT={'D':38,'A':33,'Bm':35,'G':31}
HOOK={'D':[(0,78),(.75,81),(1.5,86),(2.5,88),(3,90)],'A':[(0,88),(.75,85),(1.5,81),(2.5,83),(3,85)],
      'Bm':[(0,86),(.75,83),(1.5,78),(2.5,81),(3,83)],'G':[(0,86),(.75,83),(1.5,79),(2.5,81),(3,83)]}
PROG=['D','A']+['D','A','Bm','G']*3+['A','D']
DROPS=[(9,3),(13,3)]                       # kick-less beats (match film KICKS)
def piano_chord(notes,t0,vel=.6,g=1.0,spread=.015):
    for i,m in enumerate(notes): put('music',piano(m,3.0,vel),t0+i*spread,g*.8,rev=.3)

# ---- intro, bars 0-1 ----
for bar in (0,1):
    c=CH[PROG[bar]]
    put('music',pad(c,4*B+.4,att=.5,rel=.5),bt(bar),1.0)
    for i,m in enumerate(c+[c[0]+12,c[2]+12,c[1]+12,c[3]]):
        put('music',piano(m-12,2.0,.42),bt(bar,i*.5),.7,rev=.35)
put('lead',bell(93,1.6),bt(0,.5),1.0,rev=.4)           # start dot
put('sfx',sweep_up(2*B,300,2600),bt(0,.5),.8)            # stroke draws
put('lead',bell(98,1.8),bt(0,2.5),1.0,rev=.4)            # end dot
put('lead',bell(86,1.4),bt(0,2.6),.5,rev=.4)             # AR monogram
for i,m in enumerate([78,81,83,85,86,90]): put('lead',lead(m,.5),bt(1,0)+i*2*B/5,.9,rev=.3)   # wordmark letters
for i in range(8): put('music',pluck_chord([78+ (i%4)*3],.3),bt(1,2)+i*B/4,.25+.1*i,rev=.2)     # building 16ths
put('sfx',swell(CH['A'],1.6*B),bt(2)-1.6*B,1.0)

# ---- groove, bars 2-14 (+ final kick at bar 15) ----
kick_times=[]
for bar in range(2,16):
    c=CH[PROG[bar]]; r=ROOT[PROG[bar]]
    if bar<15: put('duck',pad(c,4*B+.25,att=.15,rel=.3),bt(bar),.9)
    for b in range(4):
        n=bar*4+b; drop=(bar,b) in DROPS
        if bar==15 and b>0: break
        if not drop:
            put('drums',kick(),bt(bar,b),.95); kick_times.append(bt(bar,b))
        if bar==15: break
        if b in (1,3) and not drop: put('drums',clap(),bt(bar,b),.55,pan=.05)
        for h in (.5,):
            if not drop or True: put('drums',hat(),bt(bar,b+h),.13,pan=.25)
        if bar>=6:
            for q in (.25,.75): put('drums',hat()*0.6,bt(bar,b+q),.17,pan=-.2)
        put('music',bass(r,.4),bt(bar,b),.9); put('music',bass(r+12,.3),bt(bar,b+.5),.7)
        for a in (.5,) : put('music',pluck_chord(c,.45),bt(bar,b+a),.8,pan=(-.3 if b%2 else .3),rev=.2)
    if 6<=bar<=13:
        for beat,m in HOOK[PROG[bar]]:
            put('lead',lead(m,.6),bt(bar,beat),1.0,rev=.3); put('lead',lead(m,.6),bt(bar,beat+.75),.35,pan=.4,rev=.4)

# ---- drop outs + payoffs ----
for (bar,b),nxt in zip(DROPS,[(10,0),(14,0)]):
    t0=bt(bar,b); chord=CH[PROG[bar+1]]
    put('sfx',swell(chord,B),t0,1.0); put('sfx',sweep_up(B,400,3500),t0,.9)
    put('sfx',sub_boom(),bt(*nxt),1.0); piano_chord([m for m in chord]+[chord[0]+12],bt(*nxt),.75,1.0)

# ---- ui sounds (exact visual beats) ----
for i,(bar,b) in enumerate([(4,0),(4,2)]): put('lead',bell(93+i*5,1.2),bt(bar,b),.7,rev=.3)          # Stayza mark dots
for i,(bar,b) in enumerate([(4,2),(4,3),(5,0)]): put('sfx',popsnd(800+i*110),bt(bar,b),.9)             # cards
for i,(bar,b) in enumerate([(6,2),(6,3),(7,0),(7,1)]): put('sfx',popsnd(780+i*95),bt(bar,b),.9)         # system tiles
for i in range(16):
    put('sfx',keytick(),bt(8,2)+i*B/4,.9)
    if i%4==0: put('sfx',popsnd(880+i*18),bt(8,2)+i*B/4,.5)                                              # tool chips
put('sfx',popsnd(1150),bt(10,.5),.9)                                                                     # second glyph
for i in range(4): put('sfx',popsnd(820+i*100),bt(12)+i*B/2,.9)                                          # build tiles
put('lead',bell(93,1.4),bt(14,1),.8,rev=.4); put('lead',bell(98,1.6),bt(14,2),.8,rev=.4)                # close ring
for i,m in enumerate([78,81,86,90]): put('lead',lead(m,.4),bt(14,3)+i*B/4,.6,rev=.3)                     # tagline
put('sfx',sub_boom(41,2.4),bt(15),1.0); piano_chord(CH['D']+[50,74],bt(15),.85,1.0,.015)
put('duck',pad(CH['D']+[50],2.6,att=.05,rel=1.2,cut=3000),bt(15),1.1); put('lead',lead(90,1.6),bt(15),1.0,rev=.5)
put('sfx',popsnd(1000),bt(15),.9); put('lead',bell(98,2.0),bt(15,.05),.8,rev=.5)                          # CTA press

# ---- sidechain, reverb, master ----
duck=np.ones(N)
for k in kick_times:
    i=int(k*SR); dt=np.arange(int(.5*SR))/SR; e=1-.7*np.exp(-dt/.085); m=min(len(e),N-i); duck[i:i+m]=np.minimum(duck[i:i+m],e[:m])
bus['duck']*=duck[:,None]
ir_t=ta(2.6); ir=rng.standard_normal((len(ir_t),2))*np.exp(-ir_t/.55)[:,None]; ir=lp(ir,5000); ir=np.vstack([np.zeros((int(.015*SR),2)),ir]); ir/=np.abs(ir).sum()*.02+1e-9
wet=np.stack([fftconvolve(send[:,c],ir[:,c])[:N] for c in (0,1)],1)
mix=bus['drums']*.95+bus['duck']*1.0+bus['music']*.9+bus['lead']*1.0+bus['sfx']*.95+wet*.35
mix=hp(mix,28); fo=int(.9*SR); mix[-fo:]*=np.linspace(1,0,fo)[:,None]**1.5
mix/=np.percentile(np.abs(mix),99.95)+1e-9; mix=np.tanh(mix*1.05)/np.tanh(1.05)*.891
wavfile.write('audio.wav',SR,(mix*32767).astype(np.int16))
x=mix.mean(1); from scipy.signal import welch
fr,p=welch(x,SR,nperseg=8192); print('>6k %.2f%%'%(100*p[fr>6000].sum()/p.sum()))
print(' '.join(f'{20*np.log10(np.sqrt((x[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}' for i in range(30)))
