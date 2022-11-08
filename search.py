#!/usr/bin/python3

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
    print(f"\nUsage: python {sys.argv[0]} [OPTIONS]")
    print("\nOPTIONS:")
    print("   -symp  (str)  : Search Symptom")
    print("   -med   (str)  : Search Medicine")
    print("   -s     (bool) : Save result to file")
    print("   -v     (bool) : Enable/Disable Verbose Mode (default: disabled)")
    print("   -h     (bool) : Print this help and exit")
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
search_symp  = None
search_med   = None

try:
    search_symp = parse_arguments(sys.argv,'symp')
except Exception as e:
    pass

try:
    search_med = parse_arguments(sys.argv,'med')
except Exception as e:
    pass

if search_symp is None and search_med is None:
    usage(1)

try:
    if parse_arguments(sys.argv, 'v', True):
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

if search_symp:
    for med in data:
        if "symptoms" in data[med]:
            symp = data[med]['symptoms']
            res = {}
            for k,v in symp.items():
                if v.lower().find(search_symp) != -1:
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
        save_file_name = f"{search_symp}_{str(uuid.uuid4())[:6]}.txt"
        with open(save_file_name,'w') as f:
            f.write(to_be_printed)
        print(f"\n\n File saved to {save_file_name}.")


if search_med:
    for med in data:
        if med.find(search_med.upper()) >=0 or data[med]['long_name'].find(search_med.upper()) >=0:
            long_name = data[med]['long_name']
            short_name = data[med]['short_name']
            to_print = f" {long_name} ({short_name}) "
            print("~"*len(to_print))
            print(to_print)
            print("~"*len(to_print))
            print()
            print("-"*len(" Description "))
            print(" Description ")
            print("-"*len(" Description "))
            print(data[med]['description'])
            print()
            print("-"*len(" Symptoms "))
            print(" Symptoms ")
            print("-"*len(" Symptoms "))
            if "symptoms" in data[med]:
                for sym_cat,val in data[med]['symptoms'].items():
                    print(f"|{sym_cat.upper()}| : {val}")
                    print()
            print("-"*len(" Dose "))
            print(" Dose ")
            print("-"*len(" Dose "))
            if "dose" in data[med]:
                print(f"{data[med]['dose']}")
            print()
            
