import re

from bs4 import BeautifulSoup

from nlp_utils import parse_text_data


class HTMLParser:
    _ratio = 0.75

    def __init__(self, page_content):
        """
        In this class initialization method we are parsing the html page content using a BeautifulSoup library
        :param page_content:
        :type page_content: String
        """
        try:
            soup_data = BeautifulSoup(page_content, "lxml")
            soup_data.encode("utf-8")
            for script in soup_data("script"):
                script.replaceWith(" ")
            for link in soup_data("link"):
                link.replaceWith(" ")
            for style in soup_data("style"):
                style.replaceWith(" ")
        except Exception as exc:
            raise ValueError("Unable to Parse the downloaded content from the url")

        invalid_tags = ['b', 'i', 'u', 'strong', 'a']
        for tag in invalid_tags:
            for match in soup_data.findAll(tag):
                match.replaceWithChildren()
        self.soup_obj = soup_data

    def parse_tag_data(self, tag_data):
        return parse_text_data(tag_data.get_text())

    def get_page_title(self):
        """
        This method returns the web page title from the html title tag
        :return: returns the title of the web page
        :rtype: str
        """
        if self.soup_obj.title is None:
            return ""
        else:
            title = self.parse_tag_data(self.soup_obj.find('title'))
            return re.sub(r'\W+', ' ', title)

    def get_page_key_words(self):
        """
        This method returns the keywords of the web page using meta and keywords html tags
        :return: web page keywords text
        :rtype: str
        """
        key_words_tag = self.soup_obj.find("meta", {"name": "keywords"})
        if key_words_tag is None:
            return ""
        else:
            return parse_text_data(key_words_tag['content'])

    def get_page_headers(self):
        """
        This method returns list of h1, h2, h3 and h4 headers of the web page
        :return: returns different headers of a webpage
        :rtype: list
        """
        headers = []

        h1_tag = self.soup_obj.find("h1")
        if h1_tag is not None:
            headers.append(self.parse_tag_data(h1_tag))

        h2_tag = self.soup_obj.find("h2")
        if h2_tag is not None:
            headers.append(self.parse_tag_data(h2_tag))

        h3_tag = self.soup_obj.find("h3")
        if h3_tag is not None:
            headers.append(self.parse_tag_data(h3_tag))

        h4_tag = self.soup_obj.find("h4")
        if h4_tag is not None:
            headers.append(self.parse_tag_data(h4_tag))

        return headers

    def get_page_meta_description(self):
        """
        This method return the meta description of a web page
        :return: returns meta description text
        :rtype: str
        """
        meta_description_tag = self.soup_obj.find("meta", {"name": "description"})
        if meta_description_tag is None:
            return ""
        else:
            return parse_text_data(meta_description_tag['content'])

    def get_page_abstract_content(self):
        """
        This method returns the abstract content of the web page
        :return: abstract description text
        :rtype: str
        """
        abstract_tag = self.soup_obj.find("meta", {"name": "abstract"})
        if abstract_tag is None:
            return ""
        else:
            return parse_text_data(abstract_tag["content"])

    def get_content_data(self, html_tag_node, words_list):
        """
        This method constructs the page content text by recursively going through the
        html subtree. If the word density is greater than the tag then we add this word to the
        result page content.
        :param html_tag_node: html subtree tag node
        :type html_tag_node: object
        :param words_list: page contents list with words 
        :type words_list: list
        """
        if html_tag_node is None:
            html_tag_node = self.soup_obj

        if len(str(html_tag_node)) == 0:
            return
        ratio = len(html_tag_node.get_text()) / float(len(str(html_tag_node)))
        if ratio > self._ratio:
            # print "\n\n\n\n\n\n\n--"
            # print self.parseNode(node)+" "
            # print ratio
            # print "\n\n\n\n\n\n\n--"
            words_list.append(self.parse_tag_data(html_tag_node) + " ")
        else:
            for i in range(len(html_tag_node.findChildren(recursive=False))):
                self.get_content_data(html_tag_node.findChildren(recursive=False)[i], words_list)

    def get_page_content(self):
        """
        This method returns the actual content of the web page by going through the html subtree
        :return: returns page content
        :rtype:str
        """
        words_list = []
        text_data = ""
        self.get_content_data(None, words_list)
        for words in words_list:
            text_data += words + " "
        return parse_text_data(text_data)
