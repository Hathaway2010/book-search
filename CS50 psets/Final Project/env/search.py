import sqlite3

def ordered_query(string):
    results = []
    term_dict_exact = {"term": string}
    term_dict_fuzzier = {"term": f"%{string}%"}
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    exact = c.execute("SELECT title, author, price FROM inv WHERE title LIKE :term OR author_first LIKE :term OR author_last LIKE :term or author2_last LIKE :term",
                  term_dict_exact)
    for row in exact:
        results.append(row)
    if len(string) > 4:
        fuzzier = c.execute("SELECT title, author, price FROM inv WHERE title LIKE :term OR author_first LIKE :term OR author_last LIKE :term or author2_last LIKE :term",
                         term_dict_fuzzier)
        for row in fuzzier:
            if row not in results:
                results.append(row)
    return results

def search(search_list):
    if search_list:
        results_full = [];
        search_length = len(search_list)
        while search_length > 0:
            end_idx = search_length
            while end_idx <= len(search_list):
                sublist = search_list[end_idx - search_length: end_idx]
                for row in ordered_query(" ".join(sublist)):
                    if row not in results_full:
                        results_full.append(row)
                end_idx = end_idx + 1
            search_length = search_length - 1
        return results_full


    else:
        return []
