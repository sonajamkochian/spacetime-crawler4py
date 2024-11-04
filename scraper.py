import re
from urllib.parse import urljoin, urlparse, urlunparse
from lxml import html
from collections import Counter

stop_words = set(["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between",
                  "both", "but", "by", "can't", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
                  "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "herself", "his", "how", "how's", "i", "i'd",
                  "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
                  "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
                  "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
                  "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
                  "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"

                  ])

unqique_pages  = set()
longest_page_in_words = {"url": "", "word_count": 0}

word_counter = Counter()
number_of_subdomains = Counter()

def save_data_file():
    pass

def scraper(url, resp):

    if resp.status != 200 or resp.raw_response is None or resp.raw_response.content is None:
        return []

    try:
        # Decode content safely and check if it's non-empty
        content = resp.raw_response.content.decode('utf-8', errors='ignore')
        if not content.strip():
            return []

        # Parse the HTML content to text
        text = html.fromstring(content).text_content()

        # Find words and filter out pages with fewer than 500 words
        words = re.findall(r'\b\w+\b', text)
        if len(words) < 500:
            return []

        # gets unique urls
        defrag_url = urlparse(url)._replace(fragment="").geturl()
        unqique_pages.add(defrag_url)

        # updates if new longest page is found
        if len(words) > longest_page_in_words["word_count"]:
            longest_page_in_words["url"] = url
            longest_page_in_words["word_count"] = len(words)
        
        #should get word frequency excluding stop_words
        filter = [word.lower() for word in words if word.lower() not in stop_words]
        word_counter.update(filter)

        # updates subdomain count 
        parsed_url = urlparse(url)
        if ".uci.edu" in parsed_url.netloc:
            number_of_subdomains[parsed_url.netloc] += 1

    except Exception as e:
        print(f"Error parsing content at {url}: {e}")
        return []

    links = extract_next_links(url, resp)

    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    try:

        if resp.status != 200 or resp.raw_response is None or resp.raw_response.content is None:
            return []

        # jacqueline -- trying smth out (with lxml)

        #       --> nothing retrieved, so empty list
        #
        content = html.fromstring(resp.raw_response.content)
        #       --> converts html to string
        #
        #
        links = content.xpath('//a/@href')
        #       --> gets hyperlinks in the raw content
        #
        res = []
        for link in links:
            purl = urlparse(urljoin(url, link))
            purl = purl._replace(fragment="")
            res.append(urlunparse(purl))

        return res
        #       --> returns list of hyperlinks
    except:
        return []

    # urlparse: parses url
    # urljoin: combines urls to create absolute url
    # absolute url:  full url (http://uci.edu/stuff)
    # relative url: url that only has path (/stuff)

    # <anchor tag <a> defines hyperlink (used to link from one page to another)
    # href attribute indicates the link's destination (url)
    # <a> tag is not a hyperlink without href attribute

def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    try:
        parsed = urlparse(url)

        # list of provided domains that are valid
        domains = [".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/",
                   ".stat.uci.edu/", "today.uci.edu/department/information_computer_sciences/"]

        # Filters
        filters = ["https://isg.ics.uci.edu/events/", ".war", "?ical=", ".php", "https://www.ics.uci.edu/~eppstein/pix/",
                   "?outlook-ical=", "?share=", "http://flamingo.ics.uci.edu/release", "cloudberry",
                   "timeline?", "?format=", "precision=second", "https://wics.ics.uci.edu/events/", "wics.uci.edu/events", "login",
                   ".txt", ".zip", ".pdf", ".ps", ".m", ".tex", ".sql"]

        # Filter out links with date-only patterns
        date_pattern = r'(\b\d{4}[-/]\d{2}[-/]\d{2}\b|\b\d{2}[-/]\d{2}[-/]\d{4}\b)'
        if re.search(date_pattern, url):
            return False

        # checks if domains that are valid in url - returns false if url doesn't have them
        if all(domain not in url for domain in domains):
            return False

        if any(filter in url for filter in filters):
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise