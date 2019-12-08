'''
Text util for chobomemo
'''
import re

def searchKeyword(text, keywordList):
    searchResult = []

    if len(text) == 0:
        return []
 
    textLower = text.lower()
    
    searchKeywordList = _removeSpace(keywordList)
    if len(searchKeywordList) == 0:
        return []

    searchKeyword = '|'.join(searchKeywordList)
    pattern = re.compile(searchKeyword)
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