import requests, pprint
from bs4 import BeautifulSoup

def scrape_top_list():
    url = "https://www.imdb.com/india/top-rated-indian-movies/"
    page = requests.get(url)
    print(page)
    soup = BeautifulSoup(page.text, "html.parser")
    print(type(soup))
#     mainBody = soup.find("tbody", class_="lister-list")
#     trs = mainBody.find_all("tr")
#     movie_names = []
#     releasing_years= []
#     ratings = []
#     links = []
#     all_contents=[]
#     for tr in trs:
#         ## fetching movie names
#         trData=tr.find("td", class_="titleColumn")
#         movie_name = trData.a.text
#         movie_names.append(movie_name)

#         ## fetching movie release year
#         movie_year = trData.span.text
#         stripped = ""
#         for char in movie_year:
#             if char not in ['(',')']:
#                 stripped+=char
#         releasing_years.append(stripped)

#         ## fetching movie ratings
#         rate = tr.find("td", class_ = "ratingColumn imdbRating").strong.text
#         ratings.append(float(rate))

#         ## fetching links
#         link = trData.a['href']
#         mainLink = f"https://www.imdb.com{link}?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=VFN45A13PEBDT8J55TYC&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_1"
#         links.append(mainLink)
#     for i in range(len(movie_names)):
#         contents = {}
#         contents["name"]=movie_names[i]
#         contents["year"]= releasing_years[i]
#         contents["position"] = i+1
#         contents["rating"] = ratings[i]
#         contents["url"] = links[i]
#         all_contents.append(contents)

#     return all_contents

    
pprint.pprint(scrape_top_list())
