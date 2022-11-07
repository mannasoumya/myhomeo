import json
import pprint
import copy

pp = pprint.PrettyPrinter(indent=2)
data = {}
with open("medicines3.json") as f:
    data = json.load(f)


for med in data:
    if "dose" in data[med]:
        x = data[med]['dose']
        index = x.find("<")
        if index > -1:
            data[med]['dose'] = x[0:index].strip().strip("\t")

# pp.pprint(data)
# for med in data:
#     print(med)
#     data[med]['keypoints'] = []
#     if "symptoms" in data[med]:
#         sym = data[med]['symptoms']
#         for k,v in sym.items():
#             s = copy.deepcopy(v)
#             if s.find("<font color=\"#0000ff\"><i>") >= 0:
#                 aa = s.split('<font color=\"#0000ff\"><i>')
#                 print(aa)
#                 for i in range(1,len(aa)):
#                     print(data[med]['keypoints'])
#                     data[med]['keypoints'].append((aa[i].split("</i></font>"))[0])
#                 data[med]['symptoms'][k] = v.replace('<font color=\"#0000ff\"><i>','').replace("</i></font>","")

with open("medicines4.json",'w') as f:
    json.dump(data,f)

