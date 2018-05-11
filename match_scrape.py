"""
Takes data from 'match_url.csv', scrapes each url and gets the match players, map and winner.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import sys
import unicodedata
import time


async def get_stats_html(url):
    """
    Parses the given url with BeautifulSoup.
    Waits for asynchronous function 'get(url)'.
    :param url: Url for the match.
    Calls 'write_from_soup(soup, date)' to scrape and write each line to csv.
    """
    base = 'https://www.hltv.org'
    stats_url = base + url[0]
    date = url[1]
    stats_page = await get(stats_url)
    soup = BeautifulSoup(stats_page, 'html.parser')
    write_from_soup(soup, date)


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


def get_map(soup):
    """
    Scrapes the map name.
    :param soup: Soup of the match
    :return: Map name or None if no map found in soup.
    """
    map = soup.find('div', attrs={'class': "match-info-box"})
    if map:
        map = map.get_text().split('\n')[2].strip()

        return map
    else:
        return None


def get_winner(soup):
    """
    Scrapes the winner of the match.
    :param soup: Soup of the match.
    :return: returns winner as "team-left", "team-right" or "tie".
    """
    winner = soup.find('div', attrs={'class': "bold won"})
    if winner:
        winner = winner.parent["class"][0]
    else:
        winner = "tie"

    return winner


def get_players(soup):
    """
    Scrapes the players of the match.
    :param soup: Soup of the match.
    :return: Player list.
    """
    player_soup = soup.find_all('td', attrs={'class': "st-player"})
    players = [player.get_text() for player in player_soup]

    return players


def fix_ascii(row):
    """
    Checks and fixes non-ascii characters to ascii equivalents or similar.
    :param string: String of characters.
    :return: Fixed string.
    """
    for i, item in enumerate(row):
        if not all(ord(char) < 128 for char in item):
            row[i] = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore').decode('utf-8')

    return row


def write_from_soup(soup, match_date):
    """
    Scrapes the needed data and writes to csv file.
    :param soup: Soup of the match.
    :param match_date: Match date.
    """
    map = get_map(soup)
    if not map:
        return

    winner = get_winner(soup)

    players = get_players(soup)
    if len(players) != 10:
        return

    with open('matches.csv', 'a', newline='') as csv_write:
        writer = csv.writer(csv_write, delimiter=',')
        row = players + [map] + [winner] + [match_date]
        row = fix_ascii(row)
        print(row)
        writer.writerow(row)


def main():
    with open('matches.csv', 'w') as _:
        """ Clears the csv file """
        pass

    url_list = []
    with open('match_url.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        for row in reader:
            url_list.append([row[0], row[1]])

    global sema
    sema = asyncio.BoundedSemaphore(5)
    loop = asyncio.get_event_loop()
    f = asyncio.wait([get_stats_html(url) for url in url_list])
    loop.run_until_complete(f)


if __name__ == '__main__':
    main()























