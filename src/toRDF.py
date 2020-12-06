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
    normalized = jsonld.normalize(frame, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    print(json.dumps(frame, indent=2))
    with open("result.json","w") as result:
        result.write(json.dumps(expanded, indent=2))
    
    
