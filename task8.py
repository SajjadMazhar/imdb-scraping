from typing_extensions import runtime
import requests, json, os
from bs4 import BeautifulSoup

def scrape_movie_details(movie_url):
    movie_id = ""
    for _id in movie_url[27:]:
        if _id != '/':
            movie_id+=_id
        else:
            break
    fileName = movie_id+".json"
    if os.path.exists(f"data/{fileName}"):
        with open(f"data/{fileName}", 'r') as f:
            dic = json.load(f)
    else:        
        directors = []
        genres =[]
        languages=[]
        page = requests.get(movie_url)
        soup = BeautifulSoup(page.text, "html.parser")
        title_runtime_div = soup.find("div", class_="TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt")
        title = title_runtime_div.h1.text ## here is the titile

        director_ul = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt")
        director = director_ul.find_all("li")[0].find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")
        for direc in director.find_all("li"):
            directors.append(direc.text)
        ## directors stored here

        titleBlock = soup.find("div", class_="TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt")
        runtimeBlock = titleBlock.find("div", class_="TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr").ul
        runtimeString =runtimeBlock.find_all("li")[-1].text
        hour = ""
        mint = ""
        for h in runtimeString:
            if h != 'h':
                hour+=h
            else:
                break
        for m in range(-2, -len(runtimeString), -1):
            if runtimeString[m]!=' ':
                mint = runtimeString[m]+mint
            else:
                break
        runtime = int(hour)*60 + int(mint)
        print(runtime)

            

            
        # runtimediv = title_runtime_div.find("div", class_="TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr").ul
        # runtime= runtimediv.find_all("li")[-1].text ## here is the runtime
        
        genre_summary = soup.find("div", class_="GenresAndPlot__OffsetContentParent-cum89p-9 dUAPpa Hero__GenresAndPlotContainer-kvkd64-11 twqaW")
        if not genre_summary:
            genre_summary = soup.find("div", class_="GenresAndPlot__ContentParent-cum89p-8 bFvaWW Hero__GenresAndPlotContainer-kvkd64-11 twqaW")
        genreDiv = genre_summary.find("div").find_all("a")
        for genre in genreDiv:
            genres.append(genre.find("span").text)
        ## genres added here

        summary = soup.find("div", class_="ipc-html-content ipc-html-content--base").div.text # summary is here


        country_lang = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base")
        if not country_lang:
            country_lang = soup.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")

        detail_section = soup.find("section", attrs={'data-testid':'Details', 'class':'ipc-page-section ipc-page-section--base celwidget'})
        detail_ul = detail_section.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base")
        country= detail_ul.find_all("li")[2].a.text # country is here
        lang_li = detail_ul.find("li", attrs={'data-testid':'title-details-languages'}).find("ul")
        lang = lang_li.find_all("li", class_="ipc-inline-list__item")
        for language in lang:
            languages.append(language.find("a").text)
        #languages done

        img_url = soup.find("a", class_="ipc-lockup-overlay ipc-focusable")['href'] # poster url is here
        dic = {
            "name":title,
            "director":directors,
            "country":country,
            "language":languages,
            "poster_image_url":img_url,
            "bio":summary,
            "runtime":runtime,
            "genre":genres
        }
        with open(f"data/{fileName}", "w") as f:
            json.dump(dic, f, indent=4)
    
    return dic


def scrape_top_list():
    if not os.path.exists("topList.json"):

        url = "https://www.imdb.com/india/top-rated-indian-movies/"
        page = requests.get(url)
        print(page)
        soup = BeautifulSoup(page.text, "html.parser")
        mainBody = soup.find("tbody", class_="lister-list")
        trs = mainBody.find_all("tr")
        movie_names = []
        releasing_years= []
        ratings = []
        links = []
        all_contents=[]
        for tr in trs:
            ## fetching movie names
            trData=tr.find("td", class_="titleColumn")
            movie_name = trData.a.text
            movie_names.append(movie_name)

            ## fetching movie release year
            movie_year = trData.span.text
            stripped = ""
            for char in movie_year:
                if char not in ['(',')']:
                    stripped+=char
            releasing_years.append(int(stripped))

            ## fetching movie ratings
            rate = tr.find("td", class_ = "ratingColumn imdbRating").strong.text
            ratings.append(float(rate))

            ## fetching links
            link = trData.a['href']
            mainLink = f"https://www.imdb.com{link}?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=VFN45A13PEBDT8J55TYC&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_1"
            links.append(mainLink)
        for i in range(len(movie_names)):
            contents = {}
            contents["name"]=movie_names[i]
            contents["year"]= releasing_years[i]
            contents["position"] = i+1
            contents["rating"] = ratings[i]
            contents["url"] = links[i]
            all_contents.append(contents)
    else:
        with open("topList.json", 'r') as f:
            all_contents = json.load(f)
        print("cache")
    return all_contents

movies= scrape_top_list()
for i in range(len(movies)):

    scrape_movie_details(movies[i]['url'])
    print("done", i)
# scrape_movie_details(movies[12]['url'])