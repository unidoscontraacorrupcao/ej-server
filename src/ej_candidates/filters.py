
def filter_by_name(querySet, filter):
    if(querySet):
        filteredCandidates = querySet.filter(name__contains=filter.upper())
        if(filteredCandidates):
            return filteredCandidates
        return []

def filter_by_party(querySet, filter):
    if(querySet):
        filteredCandidates = querySet.filter(party=filter)
        if(filteredCandidates):
            return filteredCandidates
        return []

def filter_by_candidacy(querySet, filter):
    if(querySet):
        filteredCandidates = querySet.filter(candidacy=filter.upper())
        if(filteredCandidates):
            return filteredCandidates
        return []

def filter_by_uf(querySet, filter):
    if(querySet):
        filteredCandidates = querySet.filter(uf=filter.upper())
        if(filteredCandidates):
            return filteredCandidates
        return []

def filter_by_adhered(querySet, filter):
    if(querySet):
        filteredCandidates = querySet.filter(adhered_to_the_measures__contains=filter)
        if(filteredCandidates):
            return filteredCandidates
        return []

def filter_by_clean_pass(querySet, filter):
    if(querySet):
        filteredCandidates = querySet.filter(has_clean_pass__contains=filter)
        if(filteredCandidates):
            return filteredCandidates
        return []

def filter_candidates(querySet, filters):
    if(filters["filter_by_uf"]):
        querySet = filter_by_uf(querySet, filters["filter_by_uf"])
    if(filters["filter_by_name"]):
        querySet = filter_by_name(querySet, filters["filter_by_name"])
    if(filters["filter_by_party"]):
        querySet = filter_by_party(querySet, filters["filter_by_party"])
    if(filters["filter_by_candidacy"]):
        querySet = filter_by_candidacy(querySet, filters["filter_by_candidacy"])
    if(filters["filter_by_adhered"]):
        querySet = filter_by_adhered(querySet, filters["filter_by_adhered"])
    if(filters["filter_by_clean_pass"]):
        querySet = filter_by_clean_pass(querySet, filters["filter_by_clean_pass"])
    return querySet

def get_filters(request):
    filters = {}
    filters["filter_by_name"] = request.get('filter_by_name')
    filters["filter_by_uf"] = request.get('filter_by_uf')
    filters["filter_by_party"] = request.get('filter_by_party')
    filters["filter_by_candidacy"] = request.get('filter_by_candidacy')
    filters["filter_by_adhered"] = request.get('filter_by_adhered')
    filters["filter_by_clean_pass"] = request.get('filter_by_clean_pass')
    return filters

def valid_filters(filters):
    return filters["filter_by_name"] or filters["filter_by_uf"] or\
        filters["filter_by_party"] or filters["filter_by_candidacy"] or\
        filters["filter_by_adhered"] or filters["filter_by_clean_pass"]

def get_query_limit(request):
    try:
        return int(request.GET.get("limit"))
    except:
        return 10
