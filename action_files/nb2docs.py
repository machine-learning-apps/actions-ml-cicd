import re
from pathlib import Path
from typing import Tuple, Set
from nbdev import export2html
from nbdev.export2html import Config, _re_digits

# Check for leading dashses or numbers
_re_numdash = re.compile(r'(^[-\d]+)')
warnings = set()

def rename_for_jekyll(nb_path: Path, warnings: Set[Tuple[str, str]]=None) -> str:
    """
    Name converted HTML to a .md extension and replace spaces with dashes.
    """
    assert nb_path.exists(), f'{nb_path} could not be found.'
    nm = nb_path.with_suffix('.md').name.replace(' ', '-')
    warnings.add((nb_path, nm))
    return nm


# Modify the naming process such that destination files get named properly for Jekyll _posts
def _nb2htmlfname(nb_path, dest=None): 
    fname = rename_for_jekyll(nb_path, warnings=warnings)
    if dest is None: dest = Config().doc_path
    return Path(dest)/fname
    
## apply monkey patch
export2html._nb2htmlfname = _nb2htmlfname
export2html.notebook2html(fname='notebooks/*.ipynb', dest='docs/docs/reports/', template_file='action_files/template.tpl')