#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,re,statistics
from pathlib import Path
from collections import Counter,defaultdict

COMPOSITES=sorted(['cth','ckh','cph','cfh','ch','sh','iin','in','ee'],key=len,reverse=True)
HPAT=re.compile(r'^<(?P<page>f\d+[rv]\d*)>\s+<!\s*(?P<meta>.*?)>')
VPAT=re.compile(r'^<(?P<loc>f\d+[rv]\d*\.\d+),(?P<code>[^>]*)>\s+(?P<body>.*)$')
BAD=re.compile(r'[^a-z]')

def clean(body):
    body=body.replace('<->','.')
    body=re.sub(r'<[^>]*>','.',body)
    return [p for p in re.split(r'[.,\s]+',body.lower()) if p and not BAD.search(p)]

def coll(t):
    out=[];i=0
    while i<len(t):
        for c in COMPOSITES:
            if t.startswith(c,i): out.append(c);i+=len(c);break
        else: out.append(t[i]);i+=1
    return tuple(out)

def lev1(a,b):
    if abs(len(a)-len(b))>1:return False
    if len(a)==len(b):return sum(x!=y for x,y in zip(a,b))==1
    if len(a)>len(b):a,b=b,a
    return any(a==b[:i]+b[i+1:] for i in range(len(b)))

def edit1_fraction(types):
    types=list(set(types)); hit=set(); by=defaultdict(list)
    for t in types:by[len(t)].append(t)
    for L,arr in by.items():
        cand=arr+by.get(L-1,[])+by.get(L+1,[])
        for a in arr:
            for b in cand:
                if a!=b and lev1(a,b): hit.add(a); break
    return len(hit)/len(types) if types else 0.0

def entropy(vals):
    c=Counter(vals);n=sum(c.values())
    return -sum((v/n)*math.log2(v/n) for v in c.values() if v) if n else 0.0

def near_prev10(tokens):
    vals=[]
    for i,t in enumerate(tokens):
        if i:
            p=tokens[max(0,i-10):i]
            vals.append(int(any(t!=x and lev1(t,x) for x in p)))
    return statistics.mean(vals) if vals else 0.0

def summarize(unit_tokens):
    lens=[len(t) for t in unit_tokens]; types=set(unit_tokens)
    flat=[u for t in unit_tokens for u in t]
    kt=sum(u in {'k','t'} for u in flat); k=sum(u=='k' for u in flat)
    return {
      'n_tokens':len(unit_tokens),'n_types':len(types),
      'ttr':len(types)/len(unit_tokens) if unit_tokens else 0.0,
      'mean_len':statistics.mean(lens) if lens else 0.0,
      'sd_len':statistics.pstdev(lens) if len(lens)>1 else 0.0,
      'median_len':statistics.median(lens) if lens else 0.0,
      'unit_inventory':len(set(flat)), 'unit_entropy':entropy(flat),
      'first_entropy':entropy([t[0] for t in unit_tokens if t]),
      'last_entropy':entropy([t[-1] for t in unit_tokens if t]),
      'edit1_fraction':edit1_fraction(types),
      'local_prev10':near_prev10(unit_tokens),
      'kt_mass':kt/len(flat) if flat else 0.0,
      'k_share_within_kt':k/kt if kt else 0.0,
    }

def mi_pairs(pairs):
    c=Counter(pairs);n=sum(c.values());a=Counter(x for x,y in pairs);b=Counter(y for x,y in pairs)
    return sum((v/n)*math.log2((v/n)/((a[x]/n)*(b[y]/n))) for (x,y),v in c.items()) if n else 0.0

def parse(src):
    headers={}; lines=[]; page_line_counter=Counter(); para_counter=Counter(); para_line_counter=Counter()
    for raw in Path(src).read_text(errors='replace').splitlines():
        h=HPAT.match(raw)
        if h:
            headers[h.group('page')]=dict(re.findall(r'\$(\w)=([^\s>]+)',h.group('meta')))
            continue
        m=VPAT.match(raw)
        if not m or 'P' not in m.group('code'): continue
        page=re.match(r'f\d+[rv]\d*',m.group('loc')).group()
        toks=[coll(t) for t in clean(m.group('body'))]
        if len(toks)<=1: continue
        start='<%>' in m.group('body')
        if start or para_counter[page]==0:
            para_counter[page]+=1; para_line_counter[(page,para_counter[page])]=0
        p=para_counter[page]
        pli=para_line_counter[(page,p)];para_line_counter[(page,p)]+=1
        li=page_line_counter[page];page_line_counter[page]+=1
        leaf=int(re.match(r'f(\d+)',page).group(1));side='r' if re.match(r'f\d+r',page) else 'v'
        md=headers.get(page,{})
        lines.append({
          'page_side':page,'physical_leaf':leaf,'side':side,'section':md.get('I','?'),
          'currier':md.get('L','?'),'hand':md.get('H','?'),'quire':md.get('Q','?'),
          'paragraph_id':p,'paragraph_start':int(start),'paragraph_line_index':pli,
          'page_line_index':li,'locator':m.group('loc'),'code':m.group('code'),
          'all':toks,'body':toks[1:]
        })
    return headers,lines

def aggregate(lines,keys):
    groups=defaultdict(list)
    for r in lines:groups[tuple(r[k] for k in keys)].append(r)
    out=[]
    for key,rr in groups.items():
        toks=[t for r in rr for t in r['body']]
        d={k:v for k,v in zip(keys,key)};d.update(summarize(toks));d['n_lines']=len(rr)
        pairs=[]
        for r in rr:
            a=r['all']
            for i,t in enumerate(a):
                pos='first' if i==0 else 'last' if i==len(a)-1 else 'middle'
                sig=(t[0] if t else '',t[-1] if t else '',min(len(t),7))
                pairs.append((pos,sig))
        d['linepos_mi']=mi_pairs(pairs)
        out.append(d)
    return out

def write_csv(path,rows):
    if not rows:return
    cols=[]
    for r in rows:
        for k in r:
            if k not in cols:cols.append(k)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('transcription');ap.add_argument('--out',default='phase56_state')
    a=ap.parse_args();headers,lines=parse(a.transcription)
    page=aggregate(lines,['page_side','physical_leaf','side','section','currier','hand','quire'])
    para=aggregate(lines,['page_side','physical_leaf','side','section','currier','hand','quire','paragraph_id'])
    line=[]
    for r in lines:
        d={k:r[k] for k in ['page_side','physical_leaf','side','section','currier','hand','quire','paragraph_id','paragraph_start','paragraph_line_index','page_line_index','locator','code']}
        d.update(summarize(r['body']));line.append(d)
    write_csv(a.out+'_page.csv',page);write_csv(a.out+'_paragraph.csv',para);write_csv(a.out+'_line.csv',line)
    summary={
      'schema_version':'56A-v1','source':str(a.transcription),
      'n_headers':len(headers),'n_source_lines':len(lines),'n_page_sides':len(page),'n_physical_leaves':len(set(r['physical_leaf'] for r in page)),
      'n_paragraph_groups':len(para),'n_line_rows':len(line),
      'page_sections':dict(Counter(r['section'] for r in page)),
      'page_currier':dict(Counter(r['currier'] for r in page)),
      'page_hands':dict(Counter(r['hand'] for r in page)),
      'missing_metadata_pages':sum(1 for r in page if '?' in (r['section'],r['currier'],r['hand'])),
      'recto_verso_counts':dict(Counter(r['side'] for r in page)),
      'paragraph_start_lines':sum(r['paragraph_start'] for r in lines),
    }
    Path(a.out+'_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
