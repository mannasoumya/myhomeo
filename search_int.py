import streamlit as st
import json
import pandas as pd

st.header("Search Homeopathic Medicine")

search_query = st.text_input("Symptom")
search_query = search_query.strip().lower()
data = {}

with open("medicines4.json") as f:
    data = json.load(f)

results = []

if st.button("Search"):

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
        