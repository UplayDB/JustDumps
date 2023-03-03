import json

prodToListJson = json.load(open("prodToList.json","r",encoding='utf8'))

for prod in prodToListJson:
    with open('prodname/' + str(prod["pid"]) + '.txt', 'w',encoding='utf8') as _prodname:
        _prodname.write(prod["name"])
        _prodname.close()

