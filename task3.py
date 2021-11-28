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