import requests #used to send http request to web server and retrive response
from bs4 import BeautifulSoup # a bs4 library for parsing html and extracting links
from urllib.parse import urljoin #combines relative urls with base url to form a full, absolute url

def crawl_website(base_url): #base_url is starting point of the website to crawl
    visited = set()  # To avoid re-visiting the same URL
    urls_to_visit = [base_url] #list of url pending to be visited
    broken_links = [] #stores url with 404 errors and other similar errors

    print(f"Crawling: {base_url}") #prints base url at starting of crawling process

    while urls_to_visit: #loops until there are no more url to crawl
        url = urls_to_visit.pop(0) #retrives and pops the first url from list 
        if url not in visited: #ensures thhat the url hasnt been crawled
            try: 
                response = requests.get(url) #sends http GET request to url
                status_code = response.status_code
                visited.add(url) #adds the url to visited set

                if status_code == 404:
                    print(f"broken link found: {url} (404)")
                    broken_links.append(url)
                    continue # skips further processing of this url
                elif status_code != 200:
                    print(f"non sucessful status code {status_code} for url: {url}")
                    continue 


                # Parse HTML and find links
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True): #finds all <a> tags with an href attributs(links) 
                    absolute_url = urljoin(url, link['href']) #urljoin(url, link['href']): Converts a relative link (e.g., /about) into an absolute URL (e.g., https://example.com/about).
                    if base_url in absolute_url and absolute_url not in visited: #enures absolute_url belomgs to same domain as base_url
                        urls_to_visit.append(absolute_url) #url is not a;ready visited
                
                print(f"Visited: {url}") #prints the url after sucess crawl
            except requests.RequestException as e: #handles errors like timeout or invalid response and faliback message
                print(f"Failed to access {url}: {e}")
                broken_links.append(url)

    return visited, broken_links #returns set of all crawled website


#main script
if __name__ == "__main__":
    base_url = input("Enter the base URL of the website to scan: ") #prompts user to add base url
    crawled_urls, broken_links = crawl_website(base_url) # calls crawl_website function
    
    with open("crawled_urls.txt", "w") as crawled_file:
        crawled_file.write("\n".join(crawled_urls))
    print("\n crawled urls saved to 'crawled_urls.txt")

    with open("broken_links.txt", "w") as broken_files:
        broken_files.write("\n".join(broken_links))
    print("broken links saved to 'broken_links.txt'")
