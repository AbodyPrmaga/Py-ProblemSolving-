def count_vowels(text:str):

    return sum(ch in {'a', 'e', 'i', 'o', 'u'} for ch in text.lower()) 

result = count_vowels("hello")
print(result)