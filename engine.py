from datetime import datetime

# Elegibility riles
def auto_elegibility(vehicles) -> bool:
    '''
        >>> auto_elegibility([])
        False
        >>> auto_elegibility([ {"key": 1, "year": 2018} ])
        True
    '''
    return len(vehicles) > 0

def disability_elegibility(income) -> bool:
    '''
        >>> disability_elegibility(0)
        False
        >>> disability_elegibility(500)
        True
    '''
    return income > 0

def home_elegibility(houses) -> bool:
    '''
        >>> home_elegibility([])
        False
        >>> home_elegibility([ {"key": 1, "ownership_status": "owned"} ])
        True
        >>> home_elegibility([ {"key": 1, "ownership_status": "mortgaged"} ])
        True
    '''
    return len(houses) > 0

def life_elegibility(age) -> bool:
    '''
        >>> life_elegibility(70)
        False
        >>> life_elegibility(60)
        False
        >>> life_elegibility(59)
        True
        >>> life_elegibility(40)
        True
    '''
    return age < 60


# General Rules
def rule_3(risk, user_profile) -> int:
    '''
    >>> rule_3(0, {'age':29})
    -2
    >>> rule_3(0, {'age':39})
    -1
    >>> rule_3(0, {'age':40})
    0
    '''
    if user_profile['age'] < 30:
        return risk - 2
    elif user_profile['age'] < 40:
        return risk - 1
    else: return risk

def rule_4(risk, user_profile) -> int:
    '''
    >>> rule_4(0, {'income': 0})
    0
    >>> rule_4(0, {'income': 100000})
    0
    >>> rule_4(0, {'income': 200000})
    0
    >>> rule_4(0, {'income': 200001})
    -1
    '''
    return -1 if user_profile['income'] > 200000 else 0


# Risk-specific Rules
def rule_5(user_profile) -> dict:
    '''
        >>> rule_5({"houses": [ {"key": 1, "ownership_status": "owned"}, \
                                {"key": 2, "ownership_status": "mortgaged"}]})
        {'houses': 1, 'disability': 1}
        >>> rule_5({"houses": [ {"key": 1, "ownership_status": "owned"}]})
        {}
        >>> rule_5({"houses": [ {"key": 1, "ownership_status": "mortgaged"}, \
                                {"key": 2, "ownership_status": "mortgaged"}]})
        {'houses': 2, 'disability': 1}
    '''
    analysis = {}
    for house in user_profile['houses']:
        if house['ownership_status'] == 'mortgaged':
            analysis['houses'] = analysis.get('houses',0) + 1
            analysis['disability'] = 1
    return analysis
    
def rule_6(user_profile) -> dict:
    '''
        >>> rule_6({"dependents": 2})
        {'disability': 1, 'life': 1}
        >>> rule_6({"dependents": 1})
        {'disability': 1, 'life': 1}
        >>> rule_6({"dependents": 0})
        {}
    '''
    if user_profile['dependents'] > 0:
        return {'disability': 1, 'life':1}
    return {}

def rule_7(user_profile) -> dict:
    '''
        >>> rule_7({"marital_status": "married"})
        {'life': 1, 'disability': -1}
        >>> rule_7({"marital_status": "single"})
        {}
    '''
    if user_profile['marital_status'] == 'married':
        return {'life': 1, 'disability': -1}
    return {}

def rule_8(user_profile) -> dict:
    '''
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2018} ] })
        {'auto': 1}
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2010} ] })
        {}
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2018}, \
                                  {"key": 2, "year": 2010}] })
        {'auto': 1}
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2018}, \
                                  {"key": 2, "year": 2017}, \
                                  {"key": 2, "year": 2016}, \
                                  {"key": 2, "year": 2010}] })
        {'auto': 3}
    '''
    analysis = {}
    for vehicle in user_profile['vehicles']:
        if datetime.now().year - vehicle['year'] < 5:
            analysis['auto'] = analysis.get('auto', 0) +1
    return analysis
        
def rule_9_auto(user_profile) -> dict:
    '''
        >>> rule_9_auto({'vehicles': [{"key": 1, "year": 2018}]})
        {'auto': 1}
        >>> rule_9_auto({'vehicles': [{"key": 1, "year": 2018}, \
                                 {"key": 2, "year": 2017}]})
        {}
    '''
    if len(user_profile['vehicles']) == 1:
        return {'auto': 1}
    return {}

def rule_9_home(user_profile) -> dict:
    '''
        >>> rule_9_home({"houses": [ {"key": 1, "ownership_status": "owned"}, \
                            {"key": 2, "ownership_status": "mortgaged"} ]})
        {}
        >>> rule_9_home({"houses": [ {"key": 1, "ownership_status": "owned"}]})
        {'home': 1}
    '''
    if len(user_profile['houses']) == 1:
        return {'home': 1}
    return {}



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    example =  {
                "age": 35,
                "dependents": 2,
                "houses": [ {"key": 1, "ownership_status": "owned"},
                            {"key": 2, "ownership_status": "mortgaged"} ],
                "income": 0,
                "marital_status": "married",
                "risk_questions": [0, 1, 0],
                "vehicles": [ {"key": 1, "year": 2018} ] 
                }
    
