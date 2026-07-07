def compress(text:str):
    if not text:return ""
    
    curr_char = text[0] 
    count = 1
    result = ''

    for ch in text[1:]: 
        if curr_char == ch: 
            count += 1
        else:
            result += curr_char+str(count)
            curr_char = ch 
            count = 1
    result += curr_char+str(count)
    return result

app = compress("aaabbccccdd")
print(app)