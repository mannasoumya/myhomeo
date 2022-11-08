## Quick Start

```console
$ python search.py

Usage: python search.py [OPTIONS]

OPTIONS:
   -symp  (str)  : Search Symptom
   -med   (str)  : Search Medicine
   -s     (bool) : Save result to file
   -v     (bool) : Enable/Disable Verbose Mode (default: disabled)
   -h     (bool) : Print this help and exit

$ python search.py -symp fever
$ python search.py -med nux
```
## Interactive Mode in Browser

```console 
$ pip install -r requirements.txt
$ streamlit run search_int.py
```
![alt text](image.png "Screenshot")