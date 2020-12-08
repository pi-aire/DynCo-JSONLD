from pyld import jsonld
import json

URL_CONTEXT = "./context.json"
URL_RAWJSON = "../data/issues.json"

with open(URL_CONTEXT) as contextR, open(URL_RAWJSON) as rawR:
    raw = json.load(rawR)
    ctx = json.load(contextR)
    doc = jsonld.expand(raw,{'expandContext': ctx})
    compacted = jsonld.compact(doc, ctx)
    expanded = jsonld.expand(compacted)
    frame = jsonld.frame(compacted,{})
    normalized = jsonld.normalize(expanded, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    with open("result.json","w", encoding='utf8', errors="ignore") as result:
        result.write(json.dumps(expanded, indent=2))
    with open("result.nq","w", encoding='utf8', errors="ignore") as result:
        result.write(normalized)
    
    
