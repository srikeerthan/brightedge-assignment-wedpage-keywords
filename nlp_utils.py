import re


def parse_text_data(text):
    """
    This method returns the text by converting it to lower and limiting the characters to alphanumeric and one space
    between the words
    :param text: text which has to be converted
    :type text: str
    :return: returns lower case, alphanumeric string
    :rtype: str
    """
    text = text.lower()
    text = re.sub(r'([^\s\w]|_|\n|\t|\r)+', ' ', text)
    text = re.sub(' +', ' ', text)
    return text


def get_word_count_tuples_list(content):
    """
    This method creates a list of tuples. where each tuple contains the word and its corresponding frequency in the given
      content. The return list format is like below
    [('words1',1),('words2',2),('words3',3)]
    :param content: content/text whose word count needs to be calculated
    :type content: str
    :return: returns list of word count tuples
    :rtype: list
    """
    words_count_dict = {}
    words = content.split(" ")
    for word in words:
        if word in words_count_dict:
            words_count_dict[word] += 1
        else:
            words_count_dict[word] = 1

    word_count_tuples = []
    for c in words_count_dict:
        word_count_tuples.append((c, words_count_dict[c]))
    return word_count_tuples


# output array of stopwords ["a","b","c","d",...]
def get_stop_words():
    """
    This method returns list of stop words which are constructed from a stop words text file
    :return: list of stop words
    :rtype: list
    """
    stop_words = []
    with open("stop_words.txt") as f:
        for line in f.readlines():
            stop_words.append(line.strip('\n'))
    return stop_words


def remove_stop_words(word_frequency_tuples):
    """
    This method removes the stop words from the given list of words.
    :param word_frequency_tuples: tuples with words and its frequencies
    :type word_frequency_tuples: list
    :return: returns word frequency tuples without stop words
    :rtype: list
    """
    stop_words = get_stop_words()
    new_word_frequency_tuples = []
    for word_tuple in word_frequency_tuples:
        if word_tuple[0] not in stop_words:
            new_word_frequency_tuples.append(word_tuple)
    return new_word_frequency_tuples


def sort_list_of_tuples(tuples, index):
    """
    This method returns a sorted list of tuples based on the index of tuple in ascending order.
    :param tuples: tuples which needs to sorted
    :type tuples: list
    :param index: tuple index, which is used for sorting the tuples
    :type index: int
    :return: tuples which are sorted based on given tuple index
    :rtype: list
    """
    tuples = sorted(tuples, key=lambda t: t[index])
    return tuples


def merge_list_of_tuples_with_weights(word_frequency_tuples1, word_frequency_tuples2, word_frequency_tuples3,
                                      weight1=1, weight2=1):
    """
    This method merges two lists of tuples by giving more weightage to the first list of tuples
    :param word_frequency_tuples1: first list of word frequency tuples
    :type word_frequency_tuples1: list
    :param word_frequency_tuples2: second list of word frequency tuples
    :type word_frequency_tuples2: list
    :param word_frequency_tuples3: third list of word frequency tuples
    :type word_frequency_tuples3: list
    :param weight1: amount of weightage needs to be given to the first list words frequencies
    :type weight1: int
    :param weight2: amount of weightage need to added to the second word frequency tuples
    :type weight2: int
    :return: returns merged list of word frequency tuples
    :rtype: list
    """
    words_frequency_dict = {}
    for word_tuple in word_frequency_tuples1:
        words_frequency_dict[word_tuple[0]] = word_tuple[1] * weight1
    for word_tuple in word_frequency_tuples2:
        if word_tuple[0] in words_frequency_dict:
            words_frequency_dict[word_tuple[0]] += (word_tuple[1] * weight2)
        else:
            words_frequency_dict[word_tuple[0]] = (word_tuple[1] * weight2)
    for word_tuple in word_frequency_tuples3:
        if word_tuple[0] in words_frequency_dict:
            words_frequency_dict[word_tuple[0]] += word_tuple[1]
        else:
            words_frequency_dict[word_tuple[0]] = word_tuple[1]
    words_frequency_tuples_list = []
    for word in words_frequency_dict:
        words_frequency_tuples_list.append((word, words_frequency_dict[word]))
    return words_frequency_tuples_list
