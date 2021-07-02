def dictToPrettyString(dick, string, tabs):
    if isinstance(dick, (dict, list, tuple)):
        for i in dick:
            if isinstance(dick[i], (int, float)):
                string += addTab(tabs)
                string += i + f" : {dick[i]}\n"
            elif isinstance(dick[i], str):
                string += addTab(tabs)
                string += i + f" : '{dick[i]}'\n"
            else:
                string += addTab(tabs)
                string += i + " :\n"
                dictToPrettyString(dick[i], string, tabs + 3)
        return string


def addTab(tabQuantity):
    string = ""
    for i in range(0, tabQuantity):
        string += " "
    return string


# if __name__ == '__main__':
#     dick = {'key': "hello", 'key 2': 0, "key 3": {'key 4': "world", 'key 5': 1}}
#     text = dictToPrettyString(dick, "", 0)
#     print(text)
