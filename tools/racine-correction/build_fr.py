import re,json
L=open('dump.txt',encoding='utf8').read().split('\n')
def line(n): return L[n-1]
def normmath(t):
    t=t.strip()
    t=re.sub(r'\\sqrt\[\{\\ (\d+)\}\]',r'\\sqrt[\1]',t)
    t=re.sub(r'\\sqrt\{\\ ',r'\\sqrt{',t)
    t=t.replace('\\rightarrow','\\to').replace('\\lbrack','[').replace('\\rbrack',']')
    t=t.replace('\\Rightarrow \\ ','\\Rightarrow ').replace('\\ ou\\ ','\\ \\text{ou}\\ ')
    t=re.sub(r'\\frac(?![a-z])',r'\\dfrac',t)
    t=t.replace('\\tfrac','\\tfrac')
    t=re.sub(r'\s+',' ',t)
    # tidy unary minus spacing: "- 2" after ( { = , → "-2"
    t=re.sub(r'(?<=[\(\{=,\\])\s*-\s+(?=[\d\\a-z(])',lambda m:m.group(0).replace(' ',''),t) if False else t
    return t
MATH=re.compile(r'\$\$(.+?)\$\$|\$(.+?)\$',re.S)
def split_math(s):
    """-> (template with {k}, [maths])"""
    ms=[];out='';pos=0
    for m in MATH.finditer(s):
        out+=s[pos:m.start()]; tex=m.group(1) or m.group(2)
        ms.append(normmath(tex)); out+='{%d}'%len(ms); pos=m.end()
    out+=s[pos:]
    return out,ms
STRIP={'RAVEN-09':r'^9\)','RAVEN-10':r'^10\)1\.\s*','RAVEN-11':r'^2\.\s*','EAGLE-09':r'^9\.\s+','EAGLE-10':r'^10\.\s+','EAGLE-11':r'^11\.\s+','EAGLE-12':r'^12\.\s+','PHOENIX-01':r'^1\s+','PHOENIX-02':r'^2\s+','PHOENIX-03':r'^3\)\s*'}
SSTRIP={'RAVEN-09':r'^9','RAVEN-10':r'^10\s+'}
def items_of(lines, mode, eid):
    res=[];first=True;lab=0
    for n in lines:
        raw=line(n)
        depth=len(raw)-len(raw.lstrip(' '))
        raw=raw.strip(); isq=raw.startswith('> ')
        if isq: raw=raw[2:]
        pre=''
        if mode=='stmt':
            if not first:
                if depth>=6: pre='abcdef'[lab]+') '; lab+=1
                elif depth>=4: pre='• '
        else:
            if isq: pre='• '
        parts=[p.strip() for p in re.split(r'\s*⏎\s*',raw) if p.strip()]
        for k,part in enumerate(parts):
            if mode=='sol' and first and k==0:
                rx=STRIP.get(eid,r'^\d+\.\s+'); part=re.sub(rx,'',part)
                part=re.sub(r'^B\. ','B. ',part)
            if mode=='sol' and re.match(r'^11\.\s+B',part): part=re.sub(r'^11\.\s+','',part)
            if mode=='stmt' and first and k==0 and eid in SSTRIP: part=re.sub(SSTRIP[eid],'',part)
            tpl,ms=split_math(part)
            if re.fullmatch(r'\{1\}',tpl.strip()) and len(ms)==1 and not pre:
                res.append({'x':ms[0]})
            else:
                res.append({'t':(pre if k==0 else '')+tpl.strip(),'m':ms})
        first=False
    return res
RANGES={
 'chick':([164+i for i in range(10)],[[175],[176],[177],[178],[179],[180],[181],[182],[183],[184,185,186,187]]),
 'chicken':([189+i for i in range(10)],[[200,201,202],[203,204,205],[206,207,208],[209,210],[211,212,213],[214],[215],[216],[217],[218,219,220,221,222]]),
 'raven':([[224],[225],[226],[227],[228],[229],[230],[231],[232,233,234,235],[236],[237]],[[239,240],[241,242],[243,244],[245,246,247,248],[249,250,251,252],[253,254,255,256],[257,258,259],[260,261,262],[263,264,265,266,267,268,269,270],[271,272],[273,274,275,276,277,278]]),
 'eagle':([[281],[282],[283],[284],[285],[286],[287],[288,289,290],[291,292,293],[294,295,296],[298],[299,300,301,302]],[[304,305,306,307,308,309],[310,311],[312,313],[314,315],[316,317],[319,320,321,322,323],[324,325,326],[327,328,329,330,331],[332,333,334],[335,336,337,338,339,340,341,342],[344,345,346,347,348,349,350,351,352,353,354,355],[356,357,358,359,360,361,362,363,364,365,366]]),
 'phoenix':([[369],[371],[373]],[[375,376,377,378,379,380,381,382,383,384],[385,386,387,388,389,390,391,392,393,394,395,396,397],[398,399,400,401]]),
}
EX=[]
for tier,(st,so) in RANGES.items():
    for i,(s,c) in enumerate(zip(st,so)):
        s=s if isinstance(s,list) else [s]
        eid='%s-%02d'%(tier.upper(),i+1); EX.append({'id':eid,'stmt':items_of(s,'stmt',eid),'sol':items_of(c,'sol',eid)})
json.dump(EX,open('fr_raw.json','w'),ensure_ascii=False,indent=1)
print(len(EX))
