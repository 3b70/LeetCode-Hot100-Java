"""本地/CI共用：检查并构建现有题解，不重写题解、Java或PDF，不发布。"""
import hashlib,os,subprocess,sys
from pathlib import Path
from public_files import ROOT

def content_fingerprint():
    protected=list((ROOT/'chapters').glob('*.md'))+list((ROOT/'solutions').rglob('*.java'))
    protected += [ROOT/'Hot100-Java-完整学习手册.md',ROOT/'output/pdf/Hot100-Java-完整学习手册.pdf']
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}

def main():
    before=content_fingerprint()
    for command in [['tools/deploy_preflight.py'],['tools/site_build.py'],['-m','mkdocs','build','--clean','--strict'],['tools/site_audit.py']]:
        subprocess.run([sys.executable,*command],cwd=ROOT,check=True)
    if before!=content_fingerprint(): raise RuntimeError('部署构建改动了受保护题解、Java或PDF，已停止。')
    print('PASS: deployment build left all 100 solutions, 17 chapters, full manual and PDF unchanged.')
if __name__=='__main__': main()
