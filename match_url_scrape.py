"""
Scrapes the url list of matches for some date interval.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import sys


async def get_stats_html(url):
    """
    Parses the given url with BeautifulSoup.
    Waits for asynchronous function 'get(url)'.
    :param url: Url for the match.
    :return: A soup of the match.
    """
    stats_page = await get(url)
    soup = BeautifulSoup(stats_page, 'html.parser')

    return soup


async def get(url):
    """
    Asynchronous function to retrieve the url content.
    Uses semaphores to throttle the connections to a fixed value.
    Prints semaphore status to visualize progress.
    :param url: Url for the match.
    :return: html text.
    """
    async with aiohttp.ClientSession() as session:
        async with sema, session.get(url) as response:
            print(sema)
            return await response.text()


def generate_url_list(start_date, end_date):
    """

    :param start_date: start date for the filter ('%Y-%m-%d')
    :param end_date: end date for the filter ('%Y-%m-%d')
    :return: list of url links for whole page
    """
    url_list = []
    offset = 0
    while offset < 35000:
        stats_url = "https://www.hltv.org/stats/matches?startDate={start}&endDate={end}&offset={offset}" \
            .format(start=start_date, end=end_date, offset=offset)
        url_list.append(stats_url)
        offset += 50

    return url_list


def main():
    url_list = generate_url_list('2015-01-19', '2018-04-19')

    global sema
    sema = asyncio.Semaphore(value=5)
    loop = asyncio.get_event_loop()
    f = asyncio.wait([get_stats_html(url) for url in url_list]) #generates a list of tasks for asyncio
    done, pending = loop.run_until_complete(f)

    soup_list = []
    for future in done:
        """ Retrieves the results from future object """
        soup_list.append(future.result())

    with open('match_url.csv', 'w') as _:
        """ Clears the csv file """
        pass

    for soup in soup_list:
        dates_links = soup.find_all('td', attrs={'class': "date-col"})[1:] #scrapes the rows with dates and url links
        if dates_links is None:
            """ If the page is empty (no more matches), break main loop """
            break
        for i in dates_links:
            date = i.get_text().strip()
            url = i.find('a')['href']
            with open('match_url.csv', 'a', newline='') as csv_file:
                """ Writes results to csv file"""
                writer = csv.writer(csv_file, delimiter=',')
                print([url, date])
                writer.writerow([url, date])


if __name__ == '__main__':
    main()



















