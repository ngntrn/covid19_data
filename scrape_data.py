from bs4 import BeautifulSoup
import requests
import pandas as pd

def World_Spider(url):

    # GET request HTML from specified url
    html_content = requests.get(url).text

    # use beautifulsoup to parse HTML content
    soup = BeautifulSoup(html_content, "lxml")

    # specify table id we want to scrape
    world_table = soup.find("table", attrs={"id": "main_table_countries_today"})
    # header row (tr) are the column names
    header = world_table.thead.find_all("tr")
    headings = []
    for th in header[0].find_all("th"):
        # remove newlines in column names
        headings.append(th.text.replace("\n", "").strip())

    # find all rows (tr) on table body
    body = world_table.tbody.find_all("tr")
    # empty list to hold table rows data
    data = []
    for r in range(1, len(body)):
        # row holds data for a single row
        row = []
        for tr in body[r].find_all("td"):
            row.append(tr.text.replace("\n", "").strip())
        data.append(row)

    # create dataframe for the table, using headings as columns
    df = pd.DataFrame(data, columns=headings)

    # filter the dataframe for only country rows (those with # value)
    # reset the index once those rows are removed
    data = df[df["#"] != ""].reset_index(drop=True)

    # drop columns that aren't needed
    cols = ['#',
            'Tot\xa0Cases/1M pop',
            'Deaths/1M pop',
            'Tests/1M pop',
            '1 Caseevery X ppl',
            '1 Deathevery X ppl',
            '1 Testevery X ppl']
    countries_data = data.drop(cols, axis=1)

    return countries_data

# repeat same process for US data table
def US_Spider(url):
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")

    us_table = soup.find("table", attrs={"id": "usa_table_countries_today"})
    header = us_table.thead.find_all("tr")
    headings = []
    for th in header[0].find_all("th"):
        headings.append(th.text.replace("\n", "").strip())
    body = us_table.tbody.find_all("tr")

    us_data = []
    for r in range(1, len(body)):
        row = []
        for tr in body[r].find_all("td"):
            row.append(tr.text.replace("\n", "").strip())
        us_data.append(row)

    df = pd.DataFrame(us_data, columns=headings)
    us_data = df[df["#"] != ""].reset_index(drop=True)

    cols = ['#',
            'Tot\xa0Cases/1M pop',
            'Deaths/1M pop',
            'Tests/1M pop',
            'Source',
            'Projections']
    us_data_final = us_data.drop(cols, axis=1)

    return us_data_final
