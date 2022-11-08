import streamlit as st
import json
import pandas as pd

st.header("Search Homeopathic Medicine")

search_symp = st.text_input("Symptom")
search_symp = search_symp.strip().lower()
data = {}

with open("medicines4.json") as f:
    data = json.load(f)

results = []

if st.button("Search Symptom") and search_symp!="":

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

    # banner = " MEDICINE NAME | DOSE | SYMPTOM "
    # st.write("-"*len(banner))
    # st.write(banner)
    # st.write("-"*len(banner))

    # to_be_printed = ""
    # to_be_printed = to_be_printed + "-"*len(banner) + "\n" + banner + "\n" + "-"*len(banner) + "\n"
    
    st.write(f"#### {len(results)} results found...")
    st.write(pd.DataFrame(results))
    
    # for med in results:
    #     r = f'{med["long_name"]}({med["short_name"]}) | {med["dose"] if "dose" in med else None} | {med["symptom"]}'
    #     st.write(r)
    #     to_be_printed = to_be_printed + r + "\n" + "-"*len(r) + "\n"
    #     st.write("-"*len(r))

search_med = st.text_input("Medicine")
search_med = search_med.strip()

if st.button("Search Medicine") and search_med!="":
    for med in data:
        if med.find(search_med.upper()) >=0 or data[med]['long_name'].find(search_med.upper()) >=0:
            long_name = data[med]['long_name']
            short_name = data[med]['short_name']
            to_print = f"## {long_name} ({short_name}) "
            st.write(to_print)
            st.write("#### Description ")
            st.write(data[med]['description'])
            st.write("#### Symptoms ")
            if "symptoms" in data[med]:
                for sym_cat,val in data[med]['symptoms'].items():
                    st.write(f"**{sym_cat.upper()}** : {val}")
            st.write("#### Dose ")
            if "dose" in data[med]:
                st.write(f"{data[med]['dose']}")

            st.write()    
