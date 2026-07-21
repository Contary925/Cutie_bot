def cutword(text, word) : #cuts the word off the beginning of the text, if text really starts with the word.
#cuts space(s) after the word off as well.
    if text.startswith(word):
        cut = text[len(word):]
        while cut.startswith(" "):
            cut = cut[1:]
        return cut
    raise Exception("Cannot cut as there is no target word in the beginning of the given text")