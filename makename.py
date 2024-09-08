import json
import yaml
import os.path
from collections import OrderedDict

prodconf = json.load(open("productconfig.json","r",encoding='utf8'))

id_name = {}

for conf in prodconf:
    prodId = int(conf["ProductId"])
    yml = yaml.safe_load(conf["Configuration"])
    def_loc = None
    if "localizations" in yml:
        loc = yml["localizations"]
        if "default" in loc:
            def_loc = loc["default"]
    prodname = "None"
    root = yml['root']
    if "name" in root:
        if def_loc != None and root["name"] in def_loc:
            prodname = def_loc[root["name"]]
        else:
            if root["name"] != '':
                prodname = root["name"]
    else:
        prodname = "None"
    if type(prodname) == type(None):
        prodname = "None"
    id_name.update({prodId: prodname})

noneIds = []
skipids = []
prodToListJson = []
if (os.path.exists("prodToList.json")):
    prodToListJson = json.load(open("prodToList.json","r",encoding='utf8'))
for prod in prodToListJson:
    pid = prod["pid"]
    if pid in id_name:
        name = id_name[pid]
        prod["name"] = name
    skipids.append(pid)

for iname in id_name:
    if str(iname) not in skipids:
        if not prodToListJson.__contains__({"pid": iname, "name": id_name[iname]}):
            prodToListJson.append({"pid": iname, "name": id_name[iname]})
        if id_name[iname] == "None":
            noneIds.append(iname)


L = json.loads(json.dumps(prodToListJson, indent=4, ensure_ascii=False), object_pairs_hook=OrderedDict)
seen = OrderedDict()
for d in L:
    oid = d["pid"]
    if oid not in seen:
        seen[oid] = d

outp = []
for seenv in seen.values():
    outp.append({"pid": seenv['pid'], "name": seenv['name']})

ptl = open("prodToList.json","w",encoding='utf8')
ptl.write(json.dumps(outp, indent=4, ensure_ascii=True))
ptl.close()

nnid = open("noneIds.json","w",encoding='utf8')
nnid.write(json.dumps(noneIds, indent=4))
nnid.close()

prodToListJson = json.load(open("prodToList.json","r",encoding='utf8'))
for prod in prodToListJson:
    with open('prodname/' + str(prod["pid"]) + '.txt', 'w',encoding='utf8') as _prodname:
        _prodname.write(prod["name"])
        _prodname.close()

