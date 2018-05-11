"""
Takes data from 'matches.csv', replaces each player's name with their statistics.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import sys
import unicodedata


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


async def get_stats_html(date):
    """
    Gets the three month interval depending on match date.
    Forms a url link from that date interval.
    Waits for asynchronous function 'get(url)'.
    Parses the given url with BeautifulSoup.
    :param url: Url for the match.
    Calls 'write_from_soup_date(soup, date)' to scrape and write each line to csv.
    """
    start, end = get_start_end_dates(date)
    stats_url = "https://www.hltv.org/stats/players?startDate={start}&endDate={end}&minMapCount=1"\
                .format(start=start, end=end)
    stats_page = await get(stats_url)
    soup = BeautifulSoup(stats_page, 'html.parser')

    write_from_soup_date(soup, date)


def get_start_end_dates(date):
    """
    Forms the start and end dates for the filter.
    :param date: Match date
    :return: Start and end dates.
    """
    datetime_object_end = datetime.strptime(date, '%d/%m/%y')
    three_months = timedelta(days=90)
    datetime_object_start = datetime_object_end - three_months
    start = datetime_object_start.strftime('%Y-%m-%d')
    end = datetime_object_end.strftime('%Y-%m-%d')

    return start, end


def write_from_soup_date(soup, soup_date):
    """
    Parses through the existing 'matches.csv' file and replaces each players nickname with their statistic,
    which is scraped from the soup with the corresponding date as the match.
    :param soup: Soup of the players statistics from that date.
    :param soup_date: Soup date used to compare to the match date from csv file rows.
    After replacing the row contents each row is written to a new csv file "merged.csv".
    """
    with open('matches.csv', 'r') as matches_csv:
        reader = csv.reader(matches_csv, delimiter=',')

        for row in reader:
            if len(row) == 13:
                nicknames = row[:10]
                date = row[12]

                if date == soup_date:
                    player_table = soup.find_all('tr')[1:]
                    for player in player_table:

                        stat = player.get_text().strip()
                        stat_split = stat.split('\n')
                        del stat_split[1]
                        stat_split[2] = stat_split[2].replace("+", '')
                        if not all(ord(char) < 128 for char in stat_split[0]):
                            stat_split[0] = unicodedata.normalize('NFKD', stat_split[0])\
                                .encode('ascii', 'ignore').decode('utf-8')

                        for nick in nicknames:
                            if stat_split[0] == nick:
                                for i, item in enumerate(row):
                                    if item == nick:
                                        row[i:i + 1] = stat_split[1:]
                                        break

                    with open('merged.csv', 'a', newline='') as merged_csv:
                        writer = csv.writer(merged_csv, delimiter=',')
                        print(row)
                        writer.writerow(row)


def main():
    """
    Forms a unique set of dates which are used to scrape from.
    This is done to minimize the quantity of scraping (to not scrape the same date multiple times).
    The dates are then compared with each match date and multiple player statistics can be pulled from one date,
    since there are multiple matches played on the same day.
    """
    dates = set()
    with open('matches.csv', 'r') as matches_csv:
        reader = csv.reader(matches_csv, delimiter=',')
        for row in reader:
            if len(row) == 13:
                dates.add(row[12])
    dates = list(dates)

    with open('merged.csv', 'w', newline='') as _:
        """ Clears the csv file """
        pass

    global sema
    sema = asyncio.BoundedSemaphore(value=5)
    loop = asyncio.get_event_loop()
    f = asyncio.wait([get_stats_html(date) for date in dates])
    loop.run_until_complete(f)


if __name__ == '__main__':
    main()






















