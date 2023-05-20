

def demographic_profile(param):
    keyword = param['keyword']
    search_intent = param['search_intent']
    prompt = f"""
        We need to create the target consumer demographic profile for people who are searching for \'{keyword}\' with search intent of \'{search_intent}\'. We need to know everything and anything about the person. We need to dive deep and uncover as much information for their profile. 
    """
    return prompt

