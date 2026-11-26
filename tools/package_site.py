"""将已构建站点打包用于Windows解压阅读；不涉及任何远程仓库。"""
import json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    audit=json.loads((ROOT/'reports/site-audit.json').read_text(encoding='utf-8'))
    if audit['errors']: raise RuntimeError('站点审计未通过，拒绝打包。')
    output=ROOT/'output'; output.mkdir(exist_ok=True)
    target=output/'hot100-website.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((ROOT/'site').rglob('*')):
            if path.is_file(): archive.write(path,path.relative_to(ROOT/'site').as_posix())
    print(f'{target.name}: {target.stat().st_size:,} bytes')
if __name__=='__main__': main()
