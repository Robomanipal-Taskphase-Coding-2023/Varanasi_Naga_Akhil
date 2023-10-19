import itertools

def splitwords(input_string):
    words = input_string.split()
    return words

def generatecombinations(words):
    combinations = []
    for r in range(1, len(words) + 1):
        combinations.extend(itertools.permutations(words, r))
    return combinations

def construct_sentences(word_combinations):
    sentences = []
    for combination in word_combinations:
        sentence = ' '.join(combination)
        sentences.append(sentence)
    return sentences

input_string = input("Enter a string: ")

words = splitwords(input_string)

word_combinations = generatecombinations(words)

sentences = construct_sentences(word_combinations)

for sentence in sentences:
    print(sentence)
