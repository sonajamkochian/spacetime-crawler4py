import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from lxml import html

def scraper(url, resp):
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

   



    

    # jacqueline -- just trying smth out (with BeautifulSoup)
    # if resp.status != 200:
    #   return []
    #       --> nothing retrieved, so empty list
    #
    # soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    #       --> initializes a BeautifulSoup obj with the page contents
    #       --> 'html.parser' for parsing contents
    #
    # links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]
    #       --> for loop finds <a> tags with 'href'attb(s) in content + takes that value
    #       --> urljoin converts links to URLs again
    #       --> originally used a written out for loop, but changed it to list comprehension idk
    #
    # return links
    #       --> returns list of hyperlinks


    # jacqueline -- trying smth out (with lxml)
    # if resp.status != 200:
    #   return []
    #       --> nothing retrieved, so empty list
    #
    # content = html.fromstring(resp.raw_response.content) 
    #       --> converts html to string
    #
    # links = content.xpath('//a/@href') 
    #       --> gets hyperlinks in the raw content
    #
    # return [urljoin(url, link) for link in links]
    #       --> returns list of hyperlinks


    # urlparse: parses url 
    #urljoin: combines urls to create absolute url 
    # absolute url:  full url (http://uci.edu/stuff)
    # relative url: url that only has path (/stuff)


    #parses html content into links - acts as stucture of page
    links = html.fromstring(resp.raw_resposne.content)
    



    #<anchor tag <a> defines hyperlink (used to link from one page to another)
    #href attribute indicates the link's destination (url)
    #<a> tag is not a hyperlink without href attribute

    #//a[@href] selects all <a> elements with href attribute
    anchors = links.xpath('//a[@href]')

    #processes each anchor element in order to extract url (<a href = "http:example.com">)
    for element in anchors:

        #gets value of href attribute from anchor element <a> in <a href>
        #href can either be relative or absolute url
        href = element.get('href')

        #creates absolute url from base url of current page with href 
        #makes relative url into absolute urls for crawler
        absolute  = urljoin(url, href)  







    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        #list of provided domains that are valid
        domains = [".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/", ".stat.uci.edu/"]

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
