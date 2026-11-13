import glob, json, re, warnings, sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings("ignore")
import eng_to_ipa as ipa
OV={'café':'kæˈfeɪ','takeaway':'ˈteɪkəˌweɪ','API':'ˌeɪ pi ˈaɪ','frontend':'ˈfrʌntˌɛnd','refactor':'riˈfæktər','hoodie':'ˈhʊdi','memorise':'ˈmɛməˌraɪz','unmute':'ʌnˈmjut','CV':'ˌsi ˈvi','self-motivated':'ˌsɛlf ˈmoʊtəˌveɪtɪd','goal-oriented':'ˈgoʊl ˌɔriɛntɪd','roadmap':'ˈroʊdˌmæp','MVP':'ˌɛm vi ˈpi','prioritise':'praɪˈɔrəˌtaɪz','workaround':'ˈwɝkəˌraʊnd','smartphone':'ˈsmɑrtˌfoʊn','screenshot':'ˈskrinˌʃɑt','user-friendly':'ˌjuzər ˈfrɛndli','skillful':'ˈskɪlfəl'}
rows=[]; seen=set(); topics=[]; dups=[]; bad=[]
for f in sorted(glob.glob(os.path.join(ROOT,'data','*.txt'))):
    lvl=topic=None
    for ln in open(f, encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln.strip(): continue
        if ln.startswith('@'):
            lvl,topic=ln[1:].split('|',1)
            if topic not in topics: topics.append(topic)
            continue
        p=ln.split('|')
        if len(p)!=6: bad.append((f,ln)); continue
        w=p[0].strip(); key=(w.lower(),p[1].strip().lower())
        if key in seen: dups.append(w); continue
        seen.add(key)
        t=OV.get(w) or ipa.convert(w)
        t='' if '*' in t else '/'+t.strip('/')+'/'
        rows.append([w,t,p[1],p[2],p[3],p[4],p[5],topics.index(topic),lvl])
print('total',len(rows),'dups',len(dups),'bad',len(bad), 'topics',len(topics))
print('no ipa',sum(1 for r in rows if not r[1]))
for b in bad: print('BAD',b)
print('DUPS',dups)
out=os.path.join(ROOT,'words.js')
with open(out,'w',encoding='utf-8') as o:
    o.write('// SpeakUp 3D — словарь. Формат: [слово, транскрипция, перевод, описание, где применяется, пример, перевод примера, индекс темы, уровень]\n')
    o.write('window.TOPICS='+json.dumps(topics,ensure_ascii=False)+';\n')
    o.write('window.WORDS=[\n'+',\n'.join(json.dumps(r,ensure_ascii=False) for r in rows)+'\n];\n')
