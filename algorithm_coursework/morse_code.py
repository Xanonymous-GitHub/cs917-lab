from morse_decision_tree import MorseDecisionTree

# All the morse codes, including alphanumeric characters and numbers.
__word_to_morse_codes: dict[str, str] = dict((
    ('a', '.-'),
    ('b', '-...'),
    ('c', '-.-.'),
    ('d', '-..'),
    ('e', '.'),
    ('f', '..-.'),
    ('g', '--.'),
    ('h', '....'),
    ('i', '..'),
    ('j', '.---'),
    ('k', '-.-'),
    ('l', '.-..'),
    ('m', '--'),
    ('n', '-.'),
    ('o', '---'),
    ('p', '.--.'),
    ('q', '--.-'),
    ('r', '.-.'),
    ('s', '...'),
    ('t', '-'),
    ('u', '..-'),
    ('v', '...-'),
    ('w', '.--'),
    ('x', '-..-'),
    ('y', '-.--'),
    ('z', '--..'),
    ('0', '-----'),
    ('1', '.----'),
    ('2', '..---'),
    ('3', '...--'),
    ('4', '....-'),
    ('5', '.....'),
    ('6', '-....'),
    ('7', '--...'),
    ('8', '---..'),
    ('9', '----.'),
))


def __create_mose_code_hash_dict() -> dict[str, str]:
    morse_code_hash_dict: dict[str, str] = dict()

    for key, value in __word_to_morse_codes.items():
        morse_code_hash_dict[value] = key

    return morse_code_hash_dict


def __create_inverse_morse_decision_tree() -> MorseDecisionTree:
    tree_ = MorseDecisionTree()

    for word, morse_code in __word_to_morse_codes.items():
        tree_.insert(morse_signs=morse_code[::-1], answer=word)

    return tree_


mose_code_to_words: dict[str, str] = __create_mose_code_hash_dict()
mose_code_tree = __create_inverse_morse_decision_tree()
