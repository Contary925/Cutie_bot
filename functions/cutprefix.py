def cutprefix(text, prefix) :
    cut = text[len(prefix):]
    while cut.startswith(" "):
        cut = cut[1:]
    return cut