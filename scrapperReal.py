import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape the data
def scrape():

    url = "https://www.moneycontrol.com/stocks/marketstats/index.php"
    response = requests.get(url)
    page_content = response.content
    soup = BeautifulSoup(page_content, 'html.parser')

    table_1 = soup.find('table', {"class": "breakout_tbl"})
    div = soup.find('div', {"id": "onlybuy_bse"})
    table_2 = div.find('table', {"class": "breakout_tbl"}) if div else None
   
    # Process table_2 if it exists
    if table_2 is not None:
        table_2_rows = []
        for tr in table_2.find_all("tr"):
            cells = tr.find_all("td")
            if not cells:
                cells = tr.find_all("th")
            row = [cell.text.strip() for cell in cells]
            if row:
                table_2_rows.append(row)
        
        if table_2_rows:
            table_2_headers = table_2_rows[0]
            table_2_data = table_2_rows[1:]
            df_2 = pd.DataFrame(table_2_data, columns=table_2_headers)
            df_2.to_csv("onlybuy_bse_moneycontrol.csv", index=False)
            print("Data from 'onlybuy_bse' table saved to onlybuy_bse_moneycontrol.csv")
        else:
            print("No data found in 'onlybuy_bse' table")
    else:
        print("'onlybuy_bse' table not found")

    # Process table_1 if it exists
    if table_1 is not None:
        table_1_rows = []
        for tr in table_1.find_all("tr"):
            cells = tr.find_all("td")
            if not cells:
                cells = tr.find_all("th")  # Handle header row
            row = [cell.text.strip() for cell in cells]
            if row:  # Only add non-empty rows
                table_1_rows.append(row)

        if table_1_rows:
            # The first row is the header
            table_1_headers = table_1_rows[0]
            table_1_data = table_1_rows[1:]

            # Print headers and rows for debugging
            print("Headers:", table_1_headers)
            print("Rows:", table_1_data)

            # Creating a DataFrame and saving it to a CSV file
            df = pd.DataFrame(table_1_data, columns=table_1_headers)
            df.to_csv('top_gainers.csv', index=False)
            print("Data from 'breakout_tbl' table saved to top_gainers.csv")
        else:
            print("No data found in 'breakout_tbl' table")
    else:
        print("'breakout_tbl' table not found")

# Calling the scrape function
scrape()
