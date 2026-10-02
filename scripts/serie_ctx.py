# Gemeinsamer Einstieg aller Skripte: wählt die Serie (Umgebungsvariable SERIE, Standard 4blocks),
# wechselt in ihr Verzeichnis serien/<slug>/ und lädt serie.py. Relative Pfade (osm/, raw/, out/)
# beziehen sich danach immer auf diese Serie.
import os,sys,importlib.util
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def ctx():
    slug=os.environ.get('SERIE') or '4blocks'
    d=os.path.join(ROOT,'serien',slug)
    if not os.path.isfile(os.path.join(d,'serie.py')): sys.exit(f'Serie "{slug}" nicht gefunden: {d}/serie.py fehlt')
    os.chdir(d)
    for sub in ('osm','raw','raw/photos'): os.makedirs(sub,exist_ok=True)
    if not os.path.exists('out'): os.makedirs('out')
    os.makedirs('out/fotos',exist_ok=True)
    spec=importlib.util.spec_from_file_location('serie',os.path.join(d,'serie.py'))
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return slug,d,m
