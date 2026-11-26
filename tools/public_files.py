"""明确发布白名单；不把项目父目录、临时文件或新增的无关文件自动公开。"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROOT_FILES={
    '.gitignore','.gitattributes','mkdocs.yml','requirements-deploy.txt',
    'requirements-site.txt','requirements-site-lock.txt','README.md',
    'Hot100-Java-完整学习手册.md','Java基础知识附录.md','算法知识附录.md',
    '初学者推荐刷题顺序.md','手机与电脑阅读说明.md',
    '完整性检查报告.md','网站构建与验证报告.md','THIRD_PARTY_NOTICES.md',
}
REPORTS={'audit.json','integrity.json','test-results.json','site-audit.json','browser-check.json','pdf-check.json'}
def public_files():
    paths=[ROOT/n for n in sorted(ROOT_FILES) if (ROOT/n).is_file()]
    for folder,suffixes in [('chapters',{'.md'}),('solutions',{'.java'}),('tests',{'.java'}),
                            ('web',{'.css','.js','.html','.svg','.json','.txt'})]:
        paths += [p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in suffixes]
    paths += [p for p in (ROOT/'tools').glob('*.py') if p.is_file()]
    paths += [ROOT/'sources'/n for n in ['problems.json','manifest.json']]
    paths += [ROOT/'reports'/n for n in sorted(REPORTS) if (ROOT/'reports'/n).exists()]
    paths += [ROOT/'.github/workflows/pages.yml',ROOT/'output/pdf/Hot100-Java-完整学习手册.pdf']
    paths=sorted(set(paths))
    for path in paths:
        if not path.is_file() or not path.resolve().is_relative_to(ROOT.resolve()):
            raise RuntimeError(f'发布文件异常：{path.name}')
    return paths

def markdown_files():
    return [p for p in public_files() if p.suffix=='.md']
