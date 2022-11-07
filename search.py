import json
import sys
import uuid

def parse_arguments(arr, argument, bool=False, verbose=False):
    for i, val in enumerate(arr):
        if val.replace("-", "") == argument:
            if bool:
                if verbose:
                    print(f"{argument} : True")
                return True
            if i+1 == len(arr):
                if verbose:
                    print(f":ERROR: No Value Passed for Argument: `{argument}`")
                raise Exception("NoValueForArgument")
            if verbose:
                print(f"{argument} : {arr[i+1]}")
            return arr[i+1]
    if verbose:
        print(f"ERROR: Argument '{argument}' not found")
    raise Exception("ArgumentNotFound")

def usage(exit_code):
    print(f"\nUsage: python {sys.argv[0]} 'symptom' [OPTIONS]")
    print("\nOPTIONS:")
    print("   -s  (bool) : Save result to file")
    print("   -v  (bool) : Enable/Disable Verbose Mode (default: disabled)")
    print("   -h  (bool) : Print this help and exit")
    print()
    if exit_code != None:
        sys.exit(exit_code)

try:
    if parse_arguments(sys.argv, 'h', True):
        usage(0)
except Exception as e:
    pass

if len(sys.argv) < 2:
    usage(1)
    
verbose_mode = False
save_to_file = False
search_query = sys.argv[1]


try:
    if parse_arguments(sys.argv[2:], 'v', True):
        verbose_mode = True
except Exception as e:
    pass

try:
    if parse_arguments(sys.argv[2:], 's', True):
        save_to_file = True
except Exception as e:
    pass

data = {}

with open("medicines4.json") as f:
    data = json.load(f)

results = []

for med in data:
    if "symptoms" in data[med]:
        symp = data[med]['symptoms']
        res = {}
        for k,v in symp.items():
            if v.lower().find(search_query) != -1:
                res = {
                    "short_name": data[med]["short_name"],
                    "long_name": data[med]["long_name"],
                    "symptom" : v,
                }
                if "keypoints" in data[med]:
                    res.update({
                        "keypoints": data[med]["keypoints"],
                    })
                
                if "dose" in data[med]:
                    res.update({
                        "dose": data[med]["dose"],
                    })
        if res != {}:
            results.append(res)

if verbose_mode:
    banner = " MEDICINE NAME | DOSE | SYMPTOM "
    print("-"*len(banner))
    print(banner)
    print("-"*len(banner))
else:
    banner = " MEDICINE NAME | DOSE "
    print("-"*len(banner))
    print(banner)
    print("-"*len(banner))

to_be_printed = ""
to_be_printed = to_be_printed + "-"*len(banner) + "\n" + banner + "\n" + "-"*len(banner) + "\n"

for med in results:
    if verbose_mode:
        r = f'{med["long_name"]}({med["short_name"]}) | {med["dose"] if "dose" in med else None} | {med["symptom"]}'
        print(r)
        to_be_printed = to_be_printed + r + "\n" + "-"*len(r) + "\n"
        print("-"*len(r))
    else:        
        r = f'{med["long_name"]}({med["short_name"]}) | {med["dose"] if "dose" in med else None}'
        print(r)
        to_be_printed = to_be_printed + r + "\n" + "-"*len(r) + "\n"
        print("-"*len(r))

if save_to_file:
    save_file_name = f"{search_query}_{str(uuid.uuid4())[:6]}.txt"
    with open(save_file_name,'w') as f:
        f.write(to_be_printed)
    print(f"\n\n File saved to {save_file_name}.")