import requests  # Used to send HTTP requests to web servers
from bs4 import BeautifulSoup  # For parsing HTML and extracting links
from urllib.parse import urljoin, urlparse  # For combining and parsing URLs


def crawl_website(base_url):  # Base URL is the starting point of the website to crawl
    visited = set()  # To avoid re-visiting the same URL
    urls_to_visit = [base_url]  # List of URLs pending to be visited
    broken_links = []  # Stores URLs with 404 errors and other similar errors
    insecure_links = []  # Stores URLs that use HTTP instead of HTTPS

    print(f"Crawling: {base_url}")  # Prints base URL at the start of the crawling process

    while urls_to_visit:  # Loops until there are no more URLs to crawl
        url = urls_to_visit.pop(0)  # Retrieves and pops the first URL from the list
        if url not in visited:  # Ensures the URL hasn't been crawled
            try:
                response = requests.get(url)  # Sends an HTTP GET request to the URL
                status_code = response.status_code
                visited.add(url)  # Adds the URL to the visited set

                # Check if the URL uses HTTPS
                parsed_url = urlparse(url)
                if parsed_url.scheme != 'https':
                    print(f"Insecure link found: {url} (not using HTTPS)")
                    insecure_links.append(url)

                if status_code == 404:
                    print(f"Broken link found: {url} (404)")
                    broken_links.append(url)
                    continue  # Skips further processing of this URL
                elif status_code != 200:
                    print(f"Non-successful status code {status_code} for URL: {url}")
                    continue

                # Parse HTML and find links
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):  # Finds all <a> tags with an href attribute (links)
                    absolute_url = urljoin(url, link['href'])  # Converts relative links to absolute URLs
                    if base_url in absolute_url and absolute_url not in visited:  # Ensures the link belongs to the same domain
                        urls_to_visit.append(absolute_url)  # Adds the URL to the to-visit list

                print(f"Visited: {url}")  # Prints the URL after successful crawl
            except requests.RequestException as e:  # Handles errors like timeout or invalid response
                print(f"Failed to access {url}: {e}")
                broken_links.append(url)

    return visited, broken_links, insecure_links  # Returns all crawled URLs, broken links, and insecure links


# Main script
if __name__ == "__main__":
    base_url = input("Enter the base URL of the website to scan: ")  # Prompts user to add the base URL
    crawled_urls, broken_links, insecure_links = crawl_website(base_url)  # Calls the crawl_website function

    # Save crawled URLs to a file
    with open("crawled_urls.txt", "w") as crawled_file:
        crawled_file.write("\n".join(crawled_urls))
    print("\nCrawled URLs saved to 'crawled_urls.txt'")

    # Save broken links to a file
    with open("broken_links.txt", "w") as broken_file:
        broken_file.write("\n".join(broken_links))
    print("Broken links saved to 'broken_links.txt'")

    # Save insecure links to a file
    if insecure_links:
        with open("insecure_links.txt", "w") as file:
            file.write("Insecure Links (HTTP instead of HTTPS):\n")
            for url in insecure_links:
                file.write(url + "\n")
        print("\nInsecure links saved to 'insecure_links.txt'")
    else:
        print("\nNo insecure links found")
