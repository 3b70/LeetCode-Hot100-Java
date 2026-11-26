"""从已获取的官方HTML快照重提取；不依赖外网，不把快照日期冒充实时日期。"""
import json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    html=(ROOT/'sources/official-page.html').read_text(encoding='utf-8')
    data=json.loads(re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',html).group(1))
    plan=data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['studyPlanV2Detail']
    out=[]
    for i,g in enumerate(plan['planSubGroups'],1):
        for q in g['questions']:
            out.append(dict(id=int(q['questionFrontendId']),name=q['translatedTitle'],
                difficulty={'EASY':'简单','MEDIUM':'中等','HARD':'困难'}[q['difficulty']],category=g['name'],
                chapter=i,slug=q['titleSlug'],url='https://leetcode.cn/problems/'+q['titleSlug']+'/'))
    assert len(out)==len({q['id'] for q in out})==100
    (ROOT/'sources/official-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'sources/problems.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Extracted 100 unique questions from saved official snapshot; this is not a live refresh.')
if __name__=='__main__': main()
