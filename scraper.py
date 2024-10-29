import re
from urllib.parse import urljoin, urlparse, urlunparse
from lxml import html
#from Collections import Counter

stop_words = set(["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between",
                  "both", "but", "by", "can't", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
                  "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "herself", "his", "how", "how's", "i", "i'd",
                  "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
                  "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", 
                  "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", 
                  "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", 
                  "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"

])

'''
#possibly/potential way to track unique pages, all subdomains, and word counts of pages
storage = {
    "unique": set(),
    "subdomains": Counter(),
    "page_word_count":  Counter(),

}
'''


# def letter_or_digit(char):
#     return ('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('0' <= char <= '9')

# def tokenize(path_file: str):
#     try:
#         with open(path_file, 'r', encoding='utf-8') as file:
#             current_token = []
#             while True:
#                 # Read one line at a time
#                 line = file.readline()  
#                 if not line:
#                     # Exit if end of file is reached
#                     break  

#                 for char in line:
#                     # Check if the character is an English letter or digit manually
#                     if letter_or_digit(char):
#                         # Add character to current token
#                         current_token.append(char)  
#                     else:
#                         # If a token has been formed yield it and reset for next
#                         if current_token:
#                             # Convert to lowercase before yielding
#                             yield ''.join(current_token).lower()  
#                             # Reset token for next
#                             current_token = []  

#             # Yield the last token if any
#             if current_token:
#                 yield ''.join(current_token).lower()

#     # Error handling
#     except FileNotFoundError:
#         print(f"Error! The file {path_file} not found.")
#         raise
#     except IOError as error:
#         print(f"Error reading file {path_file}: {error}")
#         raise


# def computeWordFrequencies(tokens: list[str]) -> dict[str,int]:
#     # initialize empty dictionary to store word frequency
#     frequencies = {}

#     for token in tokens:
#         if token in frequencies:
#             # Increment the count
#             frequencies[token] += 1
#         else:
#             frequencies[token] = 1
    
#     return frequencies


# def findCommonTokens(file1: str, file2: str):
#     try:
#         # Create a set for each file
#         tokens_file1 = set(tokenize(file1))
#         tokens_file2 = set(tokenize(file2))

#         # Find the common tokens
#         common = tokens_file1.intersection(tokens_file2)
        
#         print(f"The number of common tokens: {len(common)}")

#     # Error handling
#     except (FileNotFoundError) as error:
#         print(f"Error: {error}")
#         sys.exit(1)
#     except IOError as error:
#         print(f"Error reading the file: {error}")
#         sys.exit(1)

def scraper(url, resp):

    #Theory to see if this actually checks whether "content" is empty or small
    '''
    if len(resp.raw_response.content) < 100:
        return []
    '''
    
    links = extract_next_links(url, resp)

    """
    #stores unique pages, disregarding fragements. 
    #can just be put under extract_next_links i believe before appending ? 

    non_defrag_links = urlparse(url)._replace(fragemnts='').geturl()
    storage["unique"].add(non_defrag_links)
    """

    '''
    #calls helper function which tracks word freq and longest page
    helper(url, resp.raw_response.content)
    '''


    '''
    # gets all subdomain potentially 
    
    if ".uci.edu" in url:
        parsed_url = urlparse(url)
        #from urlib: .netloc: contains network location which is domain and any subdomain if is there 
        #.hostname works i believe, and probably might be better honestly.i read about netloc first 
        sub = parsed_url.netloc


        #possible adds subdomain link 
        storage["subdomains"][sub] += 1

    '''

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
        # jacqueline -- trying smth out (with lxml)
        if resp.status != 200:
            return []
        #       --> nothing retrieved, so empty list
        #
        content = html.fromstring(resp.raw_response.content) 
        #       --> converts html to string
        #
        words = re.findall(r'\b\w+\b', content)
        if len(words) < 100:
            return []
        
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
    #urljoin: combines urls to create absolute url 
    # absolute url:  full url (http://uci.edu/stuff)
    # relative url: url that only has path (/stuff)

    #<anchor tag <a> defines hyperlink (used to link from one page to another)
    #href attribute indicates the link's destination (url)
    #<a> tag is not a hyperlink without href attribute
    

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    try:
        parsed = urlparse(url)

        #list of provided domains that are valid
        domains = [".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/", ".stat.uci.edu/", "today.uci.edu/department/information_computer_sciences/"]

        #checks if domains that are valid in url - returns false if url doesn't have them
        if all(domain not in url for domain in domains):
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
        print ("TypeError for ", parsed)
        raise

"""
def helper(url, content):
    #from lxml documentation: .text_content(): Returns the text content of the element, including the text content of its children, with no markup.

    text = html.fromstring(content).text_content()
    words = re.findall(r"\b\w+\b", text.lower())
    filtered = [word for word in words if word not in stop_words]
    count = len(filtered)


    #should probably count per page and track the longest 
    storage["page_word_count"][url] = count



"""