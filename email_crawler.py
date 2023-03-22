import os
import time
import fetcher

links_to_crawl: list = []
url_finished: list = []
email_addresses: list = []
new_email_addresses: list = []


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main():
    clear()
    target: str = str(input("Target: "))
    if target == "":
        exit("Target cannot be empty.")

    crawler = fetcher.Webcrawler(target)

    while True:

        # * Scan the target to broaden the search.
        if len(links_to_crawl) == 0:
            crawler.start()
            url_list, email_list = crawler.join()
            for url in url_list:
                if url in links_to_crawl:
                    continue
                else:
                    if len(email_list) > 0:
                        for email in email_list:
                            if email in new_email_addresses:
                                continue
                            else:
                                new_email_addresses.append(email)
                    links_to_crawl.append(url)
                    url_finished.append(url)
        # * If there are links to crawl, then crawl them.
        else:
            if len(new_email_addresses) > 0:
                for email_address in new_email_addresses:
                    if email_address in email_addresses:
                        continue
                    else:
                        email_addresses.append(email_address)
                    # print("Email Address Found : " + email_address)

            for link in links_to_crawl:
                crawler = fetcher.Webcrawler(link)
                crawler.start()
                list_web_uri, email_list = crawler.join()
                if len(email_list) > 0:
                    for email in email_list:
                        if email in new_email_addresses:
                            continue
                        else:
                            print("Email Address Found : " + email)
                            new_email_addresses.append(email)
                for url in list_web_uri:
                    if url in links_to_crawl:
                        continue
                    else:
                        links_to_crawl.append(url)


if __name__ == "__main__":
    main()
