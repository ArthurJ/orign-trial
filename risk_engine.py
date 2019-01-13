from datetime import datetime

# Elegibility Rules
def auto_elegibility(user_profile) -> bool:
    '''
        >>> auto_elegibility({'vehicles':[]})
        False
        >>> auto_elegibility({'vehicles':[ {"key": 1, "year": 2018} ]})
        True
    '''
    vehicles = user_profile['vehicles']
    return len(vehicles) > 0

def disability_elegibility(user_profile) -> bool:
    '''
        >>> disability_elegibility({'income':0})
        False
        >>> disability_elegibility({'income':500})
        True
    '''
    income = user_profile['income']
    return income > 0

def home_elegibility(user_profile) -> bool:
    '''
        >>> home_elegibility({'houses':[]})
        False
        >>> home_elegibility({'houses': \
                                [{"key": 1, "ownership_status": "owned"}]})
        True
        >>> home_elegibility({'houses': \
                                [{"key": 1, "ownership_status": "mortgaged"}]})
        True
    '''
    houses = user_profile['houses']
    return len(houses) > 0

def life_elegibility(user_profile) -> bool:
    '''
        >>> life_elegibility({'age':70})
        False
        >>> life_elegibility({'age':60})
        False
        >>> life_elegibility({'age':59})
        True
        >>> life_elegibility({'age':40})
        True
    '''
    age = user_profile['age']
    return age < 60


# General Rules
def rule_3(user_profile) -> int:
    '''
    >>> rule_3({'age':29})
    -2
    >>> rule_3({'age':39})
    -1
    >>> rule_3({'age':40})
    0
    '''
    if user_profile['age'] < 30:
        return - 2
    elif user_profile['age'] < 40:
        return - 1
    else: return 0

def rule_4(user_profile) -> int:
    '''
    >>> rule_4({'income': 0})
    0
    >>> rule_4({'income': 100000})
    0
    >>> rule_4({'income': 200000})
    0
    >>> rule_4({'income': 200001})
    -1
    '''
    return -1 if user_profile['income'] > 200000 else 0


# Risk-specific Rules
def rule_5(user_profile) -> dict:
    '''
        >>> rule_5({"houses": [ {"key": 1, "ownership_status": "owned"}, \
                                {"key": 2, "ownership_status": "mortgaged"}]})
        {'home': {2: 1}, 'disability': 1}
        >>> rule_5({"houses": [ {"key": 1, "ownership_status": "owned"}]})
        {}
        >>> rule_5({"houses": [ {"key": 1, "ownership_status": "mortgaged"}, \
                                {"key": 2, "ownership_status": "mortgaged"}]})
        {'home': {1: 1, 2: 1}, 'disability': 1}
    '''
    analysis = {}
    for house in user_profile['houses']:
        if house['ownership_status'] == 'mortgaged':
            analysis_houses = analysis.get('home',{})
            analysis_houses.update({house['key']: 1})
            analysis['home'] = analysis_houses
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
        {'auto': {1: 1}}
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2010} ] })
        {}
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2018}, \
                                  {"key": 2, "year": 2010}] })
        {'auto': {1: 1}}
        >>> rule_8({"vehicles": [ {"key": 1, "year": 2018}, \
                                  {"key": 2, "year": 2017}, \
                                  {"key": 3, "year": 2016}, \
                                  {"key": 4, "year": 2010}] })
        {'auto': {1: 1, 2: 1, 3: 1}}
    '''
    analysis = {}
    for vehicle in user_profile['vehicles']:
        if datetime.now().year - vehicle['year'] < 5:
            analysis_auto = analysis.get('auto', {})
            analysis_auto.update({vehicle['key']: 1})
            analysis['auto'] = analysis_auto
    return analysis
        
def rule_9_auto(user_profile) -> dict:
    '''
        >>> rule_9_auto({'vehicles': [{"key": 1, "year": 2018}]})
        {'auto': {1: 1}}
        >>> rule_9_auto({'vehicles': [{"key": 1, "year": 2018}, \
                                 {"key": 2, "year": 2017}]})
        {}
    '''
    if len(user_profile['vehicles']) == 1:
        return {'auto': {1:1}}
    return {}

def rule_9_home(user_profile) -> dict:
    '''
        >>> rule_9_home({"houses": [ {"key": 1, "ownership_status": "owned"}, \
                            {"key": 2, "ownership_status": "mortgaged"} ]})
        {}
        >>> rule_9_home({"houses": [ {"key": 1, "ownership_status": "owned"}]})
        {'home': {1: 1}}
    '''
    if len(user_profile['houses']) == 1:
        return {'home': {1: 1}}
    return {}


def calc_base_risk(user_profile, rules) -> int:
    '''
        >>> calc_base_risk({"risk_questions": [0, 1, 0]}, [])
        1
        >>> calc_base_risk({"risk_questions": [1, 1, 0]}, [lambda x: 1])
        3
    '''
    base_risk = sum(user_profile['risk_questions'])
    for rule in rules:
        base_risk += rule(user_profile)
    return base_risk


# Rules organized for each step
eligibility = {'auto': auto_elegibility, 'disability':disability_elegibility,
               'home': home_elegibility, 'life':life_elegibility}

general_rules = [rule_3, rule_4]

risk_specific_rules = [rule_5, rule_6, rule_7, rule_8, rule_9_auto, rule_9_home]

# Last step methods
def score_mapping(user_risk):
    '''
        >>> score_mapping({'auto':'ineligible', 'home':[{'value':1},{'value':3}], 'life':0 })
        {'auto': 'ineligible', 'home': [{'value': 'regular'}, {'value': 'responsible'}], 'life': 'economic'}
    '''
    def mapping(v):
        if v <= 0: return 'economic'
        elif 0 < v <=2: return 'regular'
        else: return 'responsible'

    for paper, value in user_risk.items():
        if value == 'ineligible':
            continue
        elif isinstance(value, list):
            for item in value:
                item['value'] = mapping(item['value'])
        else:
            user_risk[paper] = mapping(value)

    return user_risk

def umbrella_score(user_risk):
    '''
        >>> umbrella_score({'auto': 'ineligible', \
                            'home': [{'value': 'economic'}, \
                                     {'value': 'regular'}], \
                                     'life': 'responsible'})
        {'auto': 'ineligible', 'home': [{'value': 'economic'}, {'value': 'regular'}], 'life': 'responsible', 'umbrella': 'regular'}
    '''
    # TODO, não há uma regra clara para definir o score da  umbrella, necessário perguntar  
    for _, value in user_risk.copy().items():
        if value == 'ineligible':
            continue
        elif value == 'economic':
            user_risk['umbrella'] = 'regular'
            break
        elif isinstance(value, list):
            for item in value:
                if item['value'] == 'economic':
                    user_risk['umbrella'] = 'regular'
                    break
            else:
                continue
            break

    else:
        user_risk['umbrella'] = 'ineligible'

    return user_risk

risk_modifiers = [score_mapping, umbrella_score]

# Process helper functions
def user_risk_special(user_risk, user_profile, special_cases):
    '''
        >>> user_risk_special({'auto': 127}, \
                                {'vehicles':[{"key": 51, "year": 2018}] }, \
                                {'auto':'vehicles'})
        {'auto': [{'key': 51, 'value': 127}]}
    '''
    for paper, obj in special_cases.items():
        paper_risk = user_risk[paper]
        user_risk[paper] = []
        for item in user_profile[obj]:
            item = {'key':item['key'], 'value':paper_risk}
            risk_paper = user_risk[paper]
            risk_paper.append(item)
            user_risk[paper] = risk_paper
    return user_risk

def user_risk_initial(risk, 
                        user_profile, 
                        eligibility_rules,
                        special_cases = {'auto':'vehicles', 'home':'houses'}):
    '''
        >>> user_risk_initial(37, {'income': 10, 'vehicles': [] }, \
                                    {'disability': lambda x: True, \
                                    'auto': lambda x: False}, {})
        {'disability': 37, 'auto': 'ineligible'}
    '''
    user_risk = {key:eligible(user_profile) 
                    for key, eligible in eligibility_rules.items()}

    for key, value in user_risk.items():
        if value:
            user_risk[key] = risk
        else:
            user_risk[key] = 'ineligible'
    
    user_risk = user_risk_special(user_risk, user_profile, special_cases)

    return user_risk


def process(user_profile, step1_rules, step2_rules, step3_rules, finalization_mathods):
    base_risk = calc_base_risk(user_profile, step1_rules)
    user_risk = user_risk_initial(base_risk, user_profile, step2_rules)
    
    to_apply = (rule(user_profile) for rule in step3_rules)

    for modifiers in to_apply:
        for key, modifier in modifiers.items():
            if user_risk[key] == 'ineligible':
                continue
            elif isinstance(modifier, dict):
                for sub_key, value in modifier.items():
                    # The subkey MUST match the index on the list
                    new_value = user_risk[key][sub_key-1]['value'] + value
                    user_risk[key][sub_key-1] = {'key':sub_key, 'value':new_value} 
            else:
                user_risk[key] += modifier
    
    for method in finalization_mathods:
        user_risk = method(user_risk)

    return user_risk


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

    assert \
        process(example, general_rules, eligibility, risk_specific_rules, risk_modifiers) == \
        {'auto': [{'key':1, 'value':'regular'}], 
        'disability': 'ineligible', 
        'home':[{'key':1, 'value':'economic'}, {'key':2, 'value':'regular'}], 
        'life':'regular', 'umbrella':'regular'}

    print(process(example, general_rules, eligibility, risk_specific_rules, risk_modifiers))