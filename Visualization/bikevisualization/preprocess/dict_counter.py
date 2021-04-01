

def create_dict_counter(counters, df_list):
    """
        create a dictionnary with all the counters and there dataframe
    """
    dict_counters = {}
    i = 0
    for elt in counters:
        dict_counters[elt] = df_list[i]
        i = i + 1
    return dict_counters

