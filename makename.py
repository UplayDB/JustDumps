import json
import yaml

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
prodToListJson = json.load(open("prodToList.json","r",encoding='utf8'))
for prod in prodToListJson:
    pid = prod["pid"]
    if pid in id_name:
        name = id_name[pid]
        prod["name"] = name
    skipids.append(pid)
    if prod["name"] == "None":
        noneIds.append(int(pid))

for iname in id_name:
    if str(iname) not in skipids:
        prodToListJson.append({"pid": iname, "name": id_name[iname]})
        if id_name[iname] == "None":
            noneIds.append(iname)

ptl = open("prodToList.json","w",encoding='utf8')
ptl.write(json.dumps(prodToListJson, indent=4))
ptl.close()

nnid = open("noneIds.json","w",encoding='utf8')
nnid.write(json.dumps(noneIds, indent=4))
nnid.close()

prodToListJson = json.load(open("prodToList.json","r",encoding='utf8'))
for prod in prodToListJson:
    with open('prodname/' + str(prod["pid"]) + '.txt', 'w',encoding='utf8') as _prodname:
        _prodname.write(prod["name"])
        _prodname.close()

