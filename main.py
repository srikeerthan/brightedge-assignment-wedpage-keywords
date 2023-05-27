import requests as requests
import validators
from validators import ValidationFailure

from html_parser import HTMLParser
from nlp_utils import get_word_count_tuples_list, remove_stop_words, sort_list_of_tuples, \
    merge_two_list_of_tuples_with_weight


def is_valid_url(url_str):
    """
    This method validates whether given string is a valid URL or not
    :param url_str: input url in string format
    :type url_str: String
    :return: return true if given string is valid otherwise false
    :rtype: Boolean
    """
    result = validators.url(url_str)
    return not isinstance(result, ValidationFailure)


def get_page_content(url):
    """
    This method returns response received after calling the given url
    :param url: input web page url
    :type url: string
    :return: returns given url page content
    :rtype: string
    """
    headers = {
        'Accept-Charset': 'utf-8',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
    }
    try:
        page_content = requests.get(url, headers=headers, timeout=10).text
    except Exception as exc:
        raise ValueError("Unable to get the content from the url: {}".format(url))
    return page_content


def find_web_page_relevant_topics(url):
    # Validates whether the given input is a valid url or not
    if not is_valid_url(url):
        print("Entered URL is not valid")
        return

    # Downloads the web page using the url
    try:
        page_content = get_page_content(url)
    except ValueError as exc:
        print(exc)
        return

        # constructs html parser object from the downloaded content of url
    try:
        html_obj = HTMLParser(page_content)
    except ValueError as exc:
        print(exc)
        return

    # collects the page title, keywords and header from the parsed html data
    page_title = html_obj.get_page_title()
    page_key_words = html_obj.get_page_key_words()
    page_headers = html_obj.get_page_headers()

    # forms the highest frequency words from the page content
    parsed_body = html_obj.get_page_content()
    body_word_count_tuples = get_word_count_tuples_list(parsed_body)
    body_word_count_tuples = remove_stop_words(body_word_count_tuples)
    body_word_count_tuples = sort_list_of_tuples(body_word_count_tuples, index=1)
    body_word_count_tuples = body_word_count_tuples[-10:]

    # Forms highest frequency words from the page title, keywords and headers
    title_keyword_headers_text = page_title + " " + page_key_words
    for header in page_headers:
        title_keyword_headers_text += " " + header
    keywords_count_tuples = get_word_count_tuples_list(title_keyword_headers_text)
    keywords_count_tuples = remove_stop_words(keywords_count_tuples)
    keywords_count_tuples = sort_list_of_tuples(keywords_count_tuples, index=1)
    keywords_count_tuples = keywords_count_tuples[-10:]

    # Merges both of the above highest frequency words by giving more weightage to the title, keywords and headers
    # than the content.
    final_word_count_tuples = merge_two_list_of_tuples_with_weight(keywords_count_tuples, body_word_count_tuples, 3)
    final_word_count_tuples = sort_list_of_tuples(final_word_count_tuples, index=1)
    final_word_count_tuples = final_word_count_tuples[-5:]
    final_word_count_tuples.reverse()

    print("Related topics/keywords of given web page")
    for word in final_word_count_tuples:
        print(word[0])


if __name__ == '__main__':
    print("Please enter the web page URL to get relevant topics")
    input_url = input()
    find_web_page_relevant_topics(input_url)

