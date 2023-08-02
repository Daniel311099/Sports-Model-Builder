import requests, json
from bs4 import BeautifulSoup

from typing import Any, TypedDict

from backend.etl.scraper.types_ import ScrapedData, ScrapeResult, ScrapeTask

class BBCSportRating(TypedDict):
    comment_id: int
    likes: int
    dislikes: int

class BBCSportComment(TypedDict):
    id_: int
    text: str

class BBCSPortCommentRating(TypedDict):
    comment: BBCSportComment
    rating: BBCSportRating

def find_comment_text(comment: dict[str, Any]):
    try:
        return str(comment['text'])
    except KeyError:
        for key, value in comment.items(): # type: ignore
            if isinstance(value, str):
                continue
            elif type(value) == dict[str, Any]:
                child = find_comment_text(value) # type: ignore
                if isinstance(child, str):
                    return child
        else:
            return None

def fetch_matchday_page_comments(page_num: int, id_: int) -> list[BBCSportComment]:
    url = "https://push.api.bbci.co.uk/batch"
    # id_ = 62619652
    # id_ = 65448666
    querystring = {"t":f"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F{id_}/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/serviceName/news/version/1.5.6?timeout=5"}
    # querystring = {"t":f"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F{id_}/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/serviceName/news/version/1.5.6?timeout=5"}
    # headers = {"Path": f"/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F62619652%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F{page_num}%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}
    # headers = {"Path": f"/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F65448666%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F{page_num}%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}
    response = requests.request("GET", url, params=querystring)
    print(response.text)
    page_comments: list[dict[str, Any]] = json.loads(response.text)['payload'][0]['body']['results'] 
    
    return [
        BBCSportComment(
            id_=comment['assetId'],
            text=find_comment_text(comment) or "",
        )
        for comment in page_comments
    ]

def get_num_pages(id_: int):
    class_name = "qa-pagination-total-page-number"
    url = f"https://www.bbc.co.uk/sport/live/football/{id_}"
    response = requests.request("GET", url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    num_pages = soup.find(class_=class_name)
    if num_pages is None:
        return 0
    return int(num_pages.text)

def fetch_page_comment_likes(page_num: int, id_: int):
    url = "https://push.api.bbci.co.uk/batch"
    # https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-lx-stream-reaction-counts-data%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F65448666%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F28%2Fversion%2F2.0.17?timeout=5
    querystring = {"t":f"/data/bbc-morph-lx-stream-reaction-counts-data/assetUri/%2Fsport%2Flive%2Ffootball%2F{id_}/isUk/true/nitroKey/lx-nitro/pageNumber/{page_num}/version/2.0.17?timeout=5"}
    response = requests.request("GET", url, params=querystring)
    page_ratings = json.loads(response.text)['payload'][0]['body']['postReactions']
    return [
        BBCSportRating(
            comment_id=rating[0],
            likes=rating['likes'],
            dislikes=rating['dislikes'],
        )
        for rating in page_ratings
    ]

def fetch_match_comments(id_: int, pages: int):
    comments: list[list[BBCSportComment]] = []
    for page in range(1, pages+1):
        page_comments = fetch_matchday_page_comments(page, id_)
        if not page_comments:
            comments.append([])
            continue
        sorted_comments = sorted(page_comments, key=lambda x: x['id_'])
        comments.append(sorted_comments)
    return comments

def fetch_match_likes(id_: int, pages: int):
    ratings: list[list[BBCSportRating]] = []
    for page in range(1, pages+1):
        page_ratings = fetch_page_comment_likes(page, id_)
        if not page_ratings:
            ratings.append([])
            continue
        sorted_ratings = sorted(page_ratings, key=lambda x: x['comment_id'])
        ratings.append(sorted_ratings)
    return ratings

def fetch_match_comments_likes(task: ScrapeTask) -> ScrapeResult[BBCSPortCommentRating]:
    id_ = task['id_']
    pages = get_num_pages(id_)
    comments = fetch_match_comments(id_, pages)
    ratings = fetch_match_likes(id_, pages)
    comment_ratings = ScrapeResult[BBCSPortCommentRating](data=[])
    for page_comments, page_ratings in zip(comments, ratings):
        if len(page_comments) != len(page_ratings):
            # comment_ratings.append(())
            continue
        for c, r in zip(page_comments, page_ratings):
            comment_ratings.data.append(ScrapedData[BBCSPortCommentRating](
                id_ = c['id_'],
                data= BBCSPortCommentRating(
                    comment = c,
                    rating = r,
                ))
            )
    return comment_ratings

# url = "https://push.api.bbci.co.uk/batch"

# querystring = {"t":"/data/bbc-morph-lx-commentary-data-paged/assetUri/%2Fsport%2Flive%2Ffootball%2F62619652/isUk/true/limit/20/nitroKey/lx-nitro/pageNumber/7/serviceName/news/version/1.5.6?timeout=5"}

# headers = {"Path": "/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fsport%252Flive%252Ffootball%252F62619652%2FisUk%2Ftrue%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F7%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5"}

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)