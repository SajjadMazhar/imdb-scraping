def scrape_movie_details(movie_url):
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

    return {
        "name":title,
        "director":directors,
        "country":country,
        "language":languages,
        "poster_image_url":img_url,
        "bio":summary,
        "runtime":runtime,
        "genre":genres
    }
