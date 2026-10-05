"""Build an offline, standalone HTML dashboard from the verified Excel workbook."""
import json,zipfile,xml.etree.ElementTree as ET,unicodedata,shutil,hashlib
from pathlib import Path
ROOT=Path(__file__).parent
WORKSPACE=ROOT.parent.parent
INPUT=WORKSPACE/'outputs/tse-acre-55456/antonio_pedro_55456_acre.xlsx'
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def normalize(s):return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()
with zipfile.ZipFile(INPUT) as z:
    shared=ET.fromstring(z.read('xl/sharedStrings.xml'))
    strings=[''.join(e.itertext()) for e in shared]
    tree=ET.fromstring(z.read('xl/worksheets/sheet3.xml'))
    rows=[]
    for row in tree.findall('.//m:sheetData/m:row',NS):
        if int(row.attrib['r'])<7:continue
        cells={}
        for c in row.findall('m:c',NS):
            v=c.find('m:v',NS);t=c.attrib.get('t')
            if v is None:value=''
            elif t=='s':value=strings[int(v.text)]
            else:value=v.text or ''
            col=''.join(x for x in c.attrib['r'] if x.isalpha());cells[col]=value
        rows.append(dict(municipio=cells['A'],codigo=cells['B'],zona=cells['C'],secao=cells['D'],agregadas=cells.get('E',''),local=cells['F'],votos=int(cells['G']),situacao=cells['H'],arquivo=cells['I'],url=cells['J']))
assert len(rows)==2270 and sum(r['votos'] for r in rows)==5118
assert len({(r['codigo'],r['zona'],r['secao']) for r in rows})==2270
assert sum(r['votos']>0 for r in rows)==1332
ibge=json.loads((WORKSPACE/'output/tse-acre-55456/municipios-ibge.json').read_text(encoding='utf-8-sig'))
geography=json.loads((WORKSPACE/'output/tse-acre-55456/acre-municipios.geojson').read_text(encoding='utf-8-sig'))
names={str(m['id']):m['nome'] for m in ibge}
tse={normalize(r['municipio']):r['codigo'] for r in rows}
for feature in geography['features']:
    code=str(feature['properties']['codarea']);name=names[code]
    feature['properties']={'ibge':code,'nome':name,'codigo':tse[normalize(name)]}
assert len(geography['features'])==22
assert {f['properties']['codigo'] for f in geography['features']}=={r['codigo'] for r in rows}
data={'meta':{'candidato':'Antônio Pedro','numero':'55456','cargo':'Deputado estadual','uf':'AC','eleicao':'6259','dataEleicao':'2026-10-04','dataColeta':'2026-10-05','totalOficial':5118,'totalSecoes':2270,'xlsxSha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'fonteTSE':'https://resultados.tse.jus.br/oficial/ele2026/6259/dados/ac/ac-c0007-e006259-u.json','fonteMapa':'https://servicodados.ibge.gov.br/api/v3/malhas/estados/12?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio'},'rows':rows,'geography':geography}
text=(ROOT/'src/index.html').read_text(encoding='utf-8')
text=text.replace('/* INLINE_CSS */',(ROOT/'src/styles.css').read_text(encoding='utf-8'))
text=text.replace('/* INLINE_DATA */',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/'))
text=text.replace('/* INLINE_APP */',(ROOT/'src/app.js').read_text(encoding='utf-8'))
(ROOT/'index.html').write_text(text,encoding='utf-8')
(ROOT/'downloads').mkdir(exist_ok=True)
shutil.copy2(INPUT,ROOT/'downloads/antonio_pedro_55456_acre.xlsx')
(ROOT/'.nojekyll').touch()
print(f'HTML gerado: {len(rows)} seções, {sum(r["votos"] for r in rows)} votos, 22 municípios, {len(text.encode())} bytes')
