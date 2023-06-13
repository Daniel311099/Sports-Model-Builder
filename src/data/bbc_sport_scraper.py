import requests

def fetch(page_num: int):
    url = "https://push.api.bbci.co.uk/batch"
    querystring = {"t":f"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F62619652/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/serviceName/news/version/1.5.6?timeout=5"}
    headers = {"Path": f"/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F62619652%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F{page_num}%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response.text

# url = "https://push.api.bbci.co.uk/batch"

# querystring = {"t":"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F62619652/isUk/true/limit/20/nitroKey/lx-nitro/pageNumber/7/serviceName/news/version/1.5.6?timeout=5"}

# headers = {"Path": "/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F62619652%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F7%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)