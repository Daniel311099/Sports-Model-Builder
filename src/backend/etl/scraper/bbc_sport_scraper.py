import requests, json
from bs4 import BeautifulSoup

def fetch_matchday_page_comments(page_num: int, id_: int=62619652):
    url = "https://push.api.bbci.co.uk/batch"
    # id_ = 62619652
    # id_ = 65448666
    querystring = {"t":f"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F{id_}/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/serviceName/news/version/1.5.6?timeout=5"}
    # querystring = {"t":f"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F{id_}/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/serviceName/news/version/1.5.6?timeout=5"}
    # headers = {"Path": f"/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F62619652%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F{page_num}%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}
    # headers = {"Path": f"/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F65448666%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F{page_num}%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}
    response = requests.request("GET", url, params=querystring)
    print(response.text)
    return response.text

def get_num_pages(id_: int):
    class_name = "qa-pagination-total-page-number"
    url = f"https://www.bbc.co.uk/sport/live/football/{id_}"
    response = requests.request("GET", url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    num_pages = soup.find(class_=class_name).text
    return int(num_pages)

def fetch_page_comment_likes(page_num: int, id_: int):
    url = "https://push.api.bbci.co.uk/batch"
    # https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-lx-stream-reaction-counts-data%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F65448666%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F28%2Fversion%2F2.0.17?timeout=5
    querystring = {"t":f"/data/bbc-morph-lx-stream-reaction-counts-data/assetUri/%2Fsport%2Flive%2Ffootball%2F{id_}/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/version/2.0.17?timeout=5"}
    response = requests.request("GET", url, params=querystring)
    print(response.text)
    return response.text

def fetch_match_comments(id_, pages):
    comments = []
    for page in range(1, pages+1):
        page_comments = fetch_matchday_page_comments(page, id_)
        page_comments = json.loads(page_comments)['payload'][0]['body']['results'] 
        if not page_comments:
            comments.append([])
            continue
        sorted_comments = sorted(page_comments, key=lambda x: x['assetId'])
        comments.append(sorted_comments)
    return comments

def fetch_match_likes(id_, pages):
    ratings = []
    for page in range(1, pages+1):
        page_ratings = fetch_page_comment_likes(page, id_)
        page_ratings = json.loads(page_ratings)['payload'][0]['body']['postReactions']
        if not page_ratings:
            ratings.append([])
            continue
        sorted_ratings = sorted(page_ratings.items(), key=lambda x: x[0])
        ratings.append(sorted_ratings)
    return ratings

def fetch_match_comments_likes(id_) -> list[tuple[dict, dict]]:
    pages = get_num_pages(id_)
    comments = fetch_match_comments(id_, pages)
    ratings = fetch_match_likes(id_, pages)
    comment_ratings = []
    for page_comments, page_ratings in zip(comments, ratings):
        if len(page_comments) != len(page_ratings):
            # comment_ratings.append(())
            continue
        for c, r in zip(page_comments, page_ratings):
            comment_ratings.append((c, r))
    return comment_ratings

# url = "https://push.api.bbci.co.uk/batch"

# querystring = {"t":"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F62619652/isUk/true/limit/20/nitroKey/lx-nitro/pageNumber/7/serviceName/news/version/1.5.6?timeout=5"}

# headers = {"Path": "/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F62619652%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F7%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)