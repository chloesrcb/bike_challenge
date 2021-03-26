


def create_dict_counter(counters, df_list):
    dict_counters = {}
    i = 0
    for elt in counters:
        dict_counters[elt] = df_list[i]
        i = i + 1
    return dict_counters

