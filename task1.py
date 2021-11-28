import requests, pprint, os, json
from bs4 import BeautifulSoup

# task6
def analyse_movies_language(movie_list):
    counts={"Hindi":0, "English":0, "Tamil":0, "Malayalam":0}
    for details in movie_list:
        for lang in details["language"]:
            if lang in counts:
                counts[lang]+=1
    return counts
            
# task5
def get_movie_list_details():
    top_movies = scrape_top_list()
    movies = []
    for details in top_movies:
        movieLink = details["url"]
        moreDetails = scrape_movie_details(movieLink)
        movies.append(moreDetails)
    return movies


# task 4
def scrape_movie_details(movie_url):
    movie_id = ""
    for _id in movie_url[27:37]:
        movie_id+=_id
    fileName = movie_id+".json"
    if not os.path.exists(fileName):
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


        runtimediv = title_runtime_div.find("div", class_="TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr").ul
        runtime= runtimediv.find_all("li")[2].text ## here is the runtime
        
        genre_summary = soup.find("div", class_="GenresAndPlot__ContentParent-cum89p-8 bFvaWW Hero__GenresAndPlotContainer-kvkd64-11 twqaW")
        genreDiv = genre_summary.find("div", class_="ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL")
        for genre in genreDiv:
            genres.append(genre.find("span").text)
        ## genres added here

        summary = soup.find("div", class_="ipc-html-content ipc-html-content--base").div.text # summary is here


        country_lang = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base")
        country = country_lang.find_all("li", class_="ipc-inline-list__item")[1].a.text # country is here
        lang = country_lang.find_all("li", class_="ipc-inline-list__item")[2] # language is here
        for language in lang:
            languages.append(language.text)
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
        with open(fileName, "w") as f:
            json.dump(dic, f, indent=4)
    else:
        with open(fileName, 'r') as f:
            dic = json.load(f)
    return dic


# task3
def group_by_decade(movies):
    grouped_by_year = group_by_year(movies)
    decades = [x for x in range(1950, 2022) if x%10 == 0]
    decade_wise = []
    for decs in decades:
        decDict = {decs:[]}
        for details in grouped_by_year:
            # pprint.pprint(details)
            for year, movie in details.items():
                # print(year)
                if year not in decDict:
                    if year>=decs and year<decs+10:
                        decDict[decs].extend(movie)
        
        decade_wise.append(decDict)
    return decade_wise


# task2
def group_by_year(movies):
    years = []
    for movie in movies:
        years.append(movie['year'])
    sorted_years = sorted(list(set(years)))
    yearWisedMovies=[]
    for year in sorted_years:
        yearDict = {year:[]}
        for movieNames in movies:
            if movieNames["year"] == year:
                yearDict[year].append(movieNames)
        yearWisedMovies.append(yearDict)
    return yearWisedMovies

# task1
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
for i in range(10):
    scrape_movie_details(scrape_top_list()[i]['url'])

# movies = []
# for i in range(10):
#     obj = scrape_movie_details(scrape_top_list()[i]['url'])
#     movies.append(obj)
#     with open('details_list.json', 'w') as f:
#         json.dump(movies, f, indent=4)
# with open("details_list.json", 'r') as f:
#     content = json.load(f)

# print(analyse_movies_language(content))

    
