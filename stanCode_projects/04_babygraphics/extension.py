"""
File: extension.py
Name: 林柏廷 Kyle
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10890537
Female Number: 7939153
---------------------------
2000s
Male Number: 12975692
Female Number: 9207577
---------------------------
1990s
Male Number: 14145431
Female Number: 10644002
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        ##################
        #                #
        #      TODO:     #
        #                #
        ##################
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')     # create BeautifulSoup object
        items = soup.tbody.find_all('tr')                               # items stores all 'tr' tag element in 'tbody'
        male = 0        # variable for summation
        female = 0      # variable for summation

        for item in items[:-1]:        # the last item is source information, need to be excluded
            new_item = item.find_all('td')      # split every 'td' element tag into a list
            # print(new_item)     # [<td>1</td>, <td>Noah</td>, <td>182,993</td>, <td>Emma</td>, <td>194,755</td>]
            # print(new_item[2].text)   # type == 'string'

            # summation for male and female
            male += int(''.join(new_item[2].text.split(',')))       # remove ',' and convert 'string' to 'int'
            female += int(''.join(new_item[4].text.split(',')))     # remove ',' and convert 'string' to 'int'

        # print the calculated results
        print(f'Male Number: {male}')
        print(f'Female Number: {female}')


if __name__ == '__main__':
    main()
