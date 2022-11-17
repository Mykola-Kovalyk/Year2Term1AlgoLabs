

def preprocess(pattern_string):
    pattern = {}

    for index, char in enumerate(pattern_string):
        pattern[char] = len(pattern_string) - index - 1

    pattern[pattern_string[-1]] = len(pattern_string)

    return pattern

def bad_character(string, pattern_string, pattern, position):

    if position + len(pattern_string) > len(string):
        return -1
    
    shift_value = 0
    for index, char in  reversed(list(enumerate(pattern_string))):
        inverse_index = len(pattern_string) - 1 - index
        string_char = string[position + index]

        if string_char != char:
            if string_char in pattern:
                shift_value = max(1, pattern[string_char] - inverse_index)
            else:
                shift_value = len(pattern_string) - inverse_index
            break
    
    return shift_value


def boyer_moore(string, pattern_string):
    pattern = preprocess(pattern_string)

    current_position = 0

    while (shift := bad_character(string, pattern_string, pattern, current_position)) > 0 and current_position < len(string):
        current_position += shift
    
    current_position = -1 if shift < 0 else current_position 

    
    return current_position



if __name__ == "__main__":
    print(boyer_moore("CACACФФAACAACACACA!", "AACAC"))