from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
from pandas import DataFrame


teams = ['BOS/boston-bruins', 'BUF/buffalo-sabres', 'DET/detroit-red-wings', 'FLA/florida-panthers', 'MON/montreal-canadiens', 'OTT/ottawa-senators', 
          'TB/tampa-bay-lightning', 'TOR/toronto-maple-leafs', 'CAR/carolina-hurricanes', 'CLB/columbus-blue-jackets', 'NYI/new-york-islanders', 'NYR/new-york-rangers', 
              'NJ/new-jersey-devils', 'PHI/philadelphia-flyers', 'PIT/pittsburgh-penguins', 'WAS/washington-capitals', 'ARI/arizona-coyotes', 'CHI/chicago-blackhawks', 
                  'COL/colorado-avalanche', 'DAL/dallas-stars', 'MIN/minnesota-wild', 'NSH/nashville-predators', 'STL/st-louis-blues', 'WPG/winnipeg-jets', 
                      'ANA/anaheim-ducks', 'CGY/calgary-flames', 'EDM/edmonton-oilers', 'LA/los-angeles-kings', 'SJ/san-jose-sharks', 'SEA/seattle-kraken',
                          'VAN/vancouver-canucks', 'LV/vegas-golden-knights']

players = []
players_df = pd.DataFrame(players)
tables_list = [0,1,2,3]

for x in teams:

    response = requests.get(f'https://www.cbssports.com/nhl/teams/{x}/roster/')
    soup = Soup(response.text, 'lxml')
    tables = soup.find_all('table')

    for y in tables_list:

        data = tables[y]
        rows = data.find_all('tr')

        def parse_row(row):
            return [str(x.string) for x in row.find_all('a')]

        list_of_parsed_rows = [parse_row(row) for row in rows]
        data_df = DataFrame(list_of_parsed_rows)

        players_df = pd.concat([players_df, data_df])

        players_df = players_df.drop(0, axis=1)


players_df = players_df.dropna()
players_df.rename(columns = {1:'name'}, inplace=True)
players_df = players_df['name'].str.lower()
players_df = players_df.str.replace('[^\w\s]','')
players_df = players_df.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
players_df = players_df.sort_values()

players_df.to_csv('nhl_list.csv', index=False)
