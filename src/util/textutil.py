"""
Text util for chobomemo
"""
import re

def getEnterPos(text):
    enter_list = text.split('\n')
    hoplist = []

    pos = 0
    hoplist.append(pos)
    for line in enter_list:
        if len(line) < 80:
            pos = pos + len(line) + 1
            hoplist.append(pos)
        else:
            pos = pos + 80 + 1
            hoplist.append(pos)
            for _ in range(80, len(line)):
                pos = pos + 80 + 1
                hoplist.append(pos)

    return hoplist

def searchKeyword(text, keywordList):
    searchResult = []

    if len(text) == 0:
        return []
 
    textLower = text.lower()
    
    searchKeywordList = _removeSpace(keywordList)
    if len(searchKeywordList) == 0:
        return []

    searchKeyword = '|'.join(searchKeywordList)
    processed_search_keyword = searchKeyword.replace('[', '\[')
    pattern = re.compile(processed_search_keyword)
    findPositionList = pattern.finditer(textLower)
    for match in findPositionList:
        searchResult.append(match.span())
    return searchResult

def _removeSpace(keywordList):
    if len(keywordList) == 0:
        return []

    keywords = []
    for k in keywordList:
        word = k.lower().strip()
        if len(word) > 0:
            keywords.append(word)
 
    return keywords

def test():
    assert _removeSpace("") == []
    assert _removeSpace(['a', '', 'b']) == ['a', 'b']
    assert searchKeyword("", "") == []
    assert searchKeyword("abc", "") == []
    assert searchKeyword("abc", ['a', '', 'b']) == [(0,1), (1,2)]
    assert searchKeyword("abc", ['ac', '', 'ce']) == []
    assert searchKeyword("abc", ['bc', '', 'ac']) == [(1,3)]