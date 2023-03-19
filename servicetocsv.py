import json

productservice = json.load(open("productservice.json", 'r',encoding='utf8'))

csv = ""

i = 1

for ps in productservice:
    v = (str(i))
    csv=csv+v+','+str(ps["ProductId"])+',"'+ps["SpaceId"]+'","'+ps["AppId"]+'"\n'    
    i=i+1

csvw = open("app_to_ids.csv", 'w',encoding='utf8')
csvw.write(csv)
csvw.close()
print("Done!")
