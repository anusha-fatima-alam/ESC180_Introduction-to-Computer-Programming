'''Semantic Similarity:

Author: Michael Guerzhoy and Anusha Fatima Alam.
Last modified: December 6th, 2022.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
       described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity as a float between the sparse vectors
       defined by vec1 and vec2. The sparse vectors vec1 and vec2 are stored as
       dictionaries.'''

    # Compute the euclidean norm of the sparse vectors: vec1 and vec2
    mag_vec1 = norm(vec1)
    mag_vec2 = norm(vec2)
    mag_product = mag_vec1*mag_vec2

    scalar_product = 0.0

    # Compute the scalar product of the sparse vectors vec1 and vec2
    for keys in vec1:
        if keys in vec2:
            scalar_product += vec1[keys] * vec2[keys]

    return scalar_product/mag_product

def build_semantic_descriptors(sentences):
    '''Return a dictionary d whose key is a word in sentences and value is a
    dictionary of the number of times a word appears with other phrases in all
    sentences (which are stored as a list of list of strings)'''

    d = {}

    for i in range(len(sentences)):
        terms_in_sentence = []
        for term in sentences[i]:
            if term not in terms_in_sentence:
                terms_in_sentence.append(term)
        for phrase in terms_in_sentence:
            if phrase not in d:
                d[phrase] = {}
            for word in terms_in_sentence:
                if word != phrase:
                    if word not in d[phrase]:
                        d[phrase][word] = 0
                    d[phrase][word] += 1

    return d

def build_semantic_descriptors_from_files(filenames):
    '''Return a dictionary containing the semantic descriptors of all the words
    in the file (in filenames). Assume that only punctuation that separate a
    sentence are ".", "!" and "?". Assume that other punctuation present in the
    text are [",", "-", "--", ":", ";"]. Treat the files in filenames as a
    single text. Assume that filenames is a list of files.'''

    compiled_text = ""
    sentences = []

    # Compile all files (in filenames) in one file to treat it as a single text
    for m in range(len(filenames)):
        compiled_text += str(open(filenames[m], "r", encoding="latin1").read())

    # Modify the compiled_text to all lower case and replace the punctuations
    # that do not separate the sentences with a single space.
    compiled_text = compiled_text.lower()
    compiled_text = compiled_text.replace("-", " ")
    compiled_text = compiled_text.replace("--", " ")
    compiled_text = compiled_text.replace(",", " ")
    compiled_text = compiled_text.replace(":", " ")
    compiled_text = compiled_text.replace(";", " ")
    compiled_text = compiled_text.replace("\n", " ")

    # Split the text based on punctuation that does separate the sentences
    compiled_text = compiled_text.replace("!", ".")
    compiled_text = compiled_text.replace("?", ".")
    compiled_text = compiled_text.split(".")

    # Modify the contents of the list of sentences with sentences in the text
    for k in range(len(compiled_text)):
        res = compiled_text[k].split()
        sentences.append(res)

    return build_semantic_descriptors(sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''Return the string in the list of choices that is the most similar to
    the word word according the similarity computed by the similarity function.
    Assume the semantic_descriptors is a dictionary computed from
    build_semantic_descriptors(sentences)'''

    similarity = []

    # If the semantic similarity between the words cannot be computed return -1
    if word not in semantic_descriptors:
        return -1

    for i in range(len(choices)):
        if choices[i] not in semantic_descriptors:
            similarity.append(-1)
            continue
        # Compute the similarity using the similarity function
        similarity.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]]))

    # Correct choice the one of whose similarity is maximum
    correct_choice = choices[similarity.index(max(similarity))]

    return correct_choice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''Return a float between 0.0 and 100.0 for the percentage of the correct
    number of guesses using the semantic descriptors stored in semantic
    descriptors and the similarity function'''

    right = 0

    text = open(filename, encoding="latin1").read()
    text = text.split("\n")

    for i in range(len(text)):
        text[i] = text[i].split()
        # If the list of text[i] is empty, delete the list item and continue to the next iteration
        if len(text[i]) == 0:
            del text[i]
            i -= 1
            continue
        # Check if the word in text[1] is the right guess using the most_similar_word function
        if text[i][1] == most_similar_word(text[i][0], text[i][2:], semantic_descriptors, similarity_fn):
            right += 1

    length = len(text)

    # Compute the percentage of the number of correct guesses
    percentage = right/length * 100
    return percentage


if __name__ == "__main__":
    vec1 = {"a": 1, "b": 2, "c": 3}
    vec2 = {"b": 4, "c": 5, "d": 6}
    print(cosine_similarity(vec1, vec2))

    filenames = ["war_and_peace.txt", "swanns_way.txt"]

    print(build_semantic_descriptors([["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]],
))

    import time
    start = time.time()
    print(run_similarity_test("test.txt", build_semantic_descriptors_from_files(filenames), cosine_similarity))
    end = time.time()
    print(end - start)