

def rabin_carp(string, pattern_string):
    char_legnth =  2 ^ 8
    hash_prime = 797

    string_hash = 0 
    for i, x in enumerate(string[0:len(pattern_string)]):
        string_hash = (string_hash + ord(x) * pow(char_legnth, len(pattern_string) - i - 1)) % hash_prime

    pattern_hash = 0 
    for i, x in enumerate(pattern_string):
        pattern_hash = (pattern_hash + ord(x) * pow(char_legnth, len(pattern_string) - i - 1)) % hash_prime

    position = 0
    while True:
        if string_hash == pattern_hash:
            if string[position:position+len(pattern_string)] == pattern_string:
                break 
        

        if position >= len(string) - len(pattern_string):
            return -1

        string_hash = string_hash * char_legnth - ord(string[position]) * pow(char_legnth, len(pattern_string))
        string_hash = (string_hash + ord(string[position + len(pattern_string)])) % hash_prime

        position += 1
    
    return position

if __name__ == '__main__':
    print(rabin_carp("CACACФФAACAACACACA!", "AACAC"))