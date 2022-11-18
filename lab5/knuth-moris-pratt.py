


def knuth_morris_pratt( text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)
    text_index = 0 
    pattern_index = 0

    lps = compute_lps(pattern)

    while text_index <= text_length - pattern_length:
        if pattern[pattern_index] == text[text_index]:
            text_index += 1
            pattern_index += 1

        if pattern_index == pattern_length:
            return text_index - pattern_index       # store position here if you need to find multiple
            pattern_index = lps[pattern_index-1]

        elif text_index < text_length and pattern[pattern_index] != text[text_index]:
            if pattern_index != 0:
                pattern_index = lps[pattern_index-1]
            else:
                text_index += 1
    
    return -1
    

def compute_lps(pattern):
    pattern_length = len(pattern)
    
    prefix_index = 0 
    suffix_index = 1

    lps = [0]*pattern_length

    while suffix_index < pattern_length:
        if pattern[suffix_index] == pattern[prefix_index]:
            prefix_index += 1
            lps[suffix_index] = prefix_index
            suffix_index += 1
        else:
            if prefix_index != 0:
                prefix_index = lps[prefix_index-1]
            else:
                lps[suffix_index] = 0
                suffix_index += 1
    
    return lps

if __name__ == '__main__':
    print(knuth_morris_pratt("CACACФФAACAACACACA!", "AACAC"))