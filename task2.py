def group_by_year(movies):
    years = []
    for movie in movies:
        years.append(movie['year'])
    sorted_years = sorted(list(set(years)))
    yearWisedMovies=[]
    for year in sorted_years:
        yearDict = {year:[]}
        print(year)
        for movieNames in movies:
            if movieNames["year"] == year:
                yearDict[year].append(movieNames)
        yearWisedMovies.append(yearDict)
    return yearWisedMovies