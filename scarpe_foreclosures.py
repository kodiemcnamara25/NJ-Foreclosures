from bs4 import BeautifulSoup
import requests
import re
import string
import pandas as pd

base_url = "https://salesweb.civilview.com"
relative_url_to_table = "/Sales/SalesSearch?countyId=8"

page = requests.get(base_url+relative_url_to_table)
soup = BeautifulSoup(page.content, 'html.parser')

fc_html_table = soup.find("table", class_='table table-striped')

column_headers = [hdr.text if hdr.text!='' else "Link to Details" for hdr in fc_html_table.find("thead").find_all("th")]


fc_dict = {}
for col in column_headers:
    fc_dict[col] = []

row_obj = fc_html_table.find_all("tr")[1]
for row_obj in fc_html_table.find_all("tr")[1:]:
    cols = row_obj.find_all("td")
    
    fc_dict["Link to Details"].append(
        base_url + cols[0].find_all("a")[0].get('href')
        )

    for i in range(1,len(cols)):
        fc_dict[list(fc_dict.keys())[i]].append(cols[i].text)


# Parse out street addresses, town, and zip code
fc_dict["Street Address"] = []
fc_dict["Town"] = []
fc_dict["Zip Code"] = []

street_names = [
    "Court",
    "Street",
    "Avenue",
    "Concourse",
    "Place",
    "Drive",
    "Road",
    "Lane",
    "Run",
    "Circle",
    "Parkway",
    "Boulevard",
    "Terrace"
]

for address in fc_dict['Address']:
    rev_split_address = list(reversed(address.split(" ")))

    fc_dict["Zip Code"].append(rev_split_address[0])
    town_name = rev_split_address[2]

    for i in range(3,len(rev_split_address)):
        word = rev_split_address[i]
        if re.match(pattern=f'{"|".join(street_names)}|[0-9]',string=word,flags=re.IGNORECASE):
            street_address = " ".join(list(reversed(rev_split_address[i:])))
            break
        
        town_name = word + " " + town_name

    fc_dict["Town"].append(town_name)
    fc_dict["Street Address"].append(street_address)

fc_summary_table = pd.DataFrame(fc_dict)


# link = fc_dict['Link to Details'][0]
# for link in fc_dict['Link to Details']:

#     page = requests.get(link)
#     soup = BeautifulSoup(page.content, 'html.parser')

#     fc_html_table = soup.find("table", class_='table table-striped')

#     column_headers = [hdr.text if hdr.text!='' else "Link to Details" for hdr in fc_html_table.find("thead").find_all("th")]


#     fc_dict = {}
#     for col in column_headers:
#         fc_dict[col] = []

#     row_obj = fc_html_table.find_all("tr")[1]
#     for row_obj in fc_html_table.find_all("tr")[1:]:
#         cols = row_obj.find_all("td")
        
#         fc_dict["Link to Details"].append(
#             base_url + cols[0].find_all("a")[0].get('href')
#             )

#         for i in range(1,len(cols)):
#             fc_dict[list(fc_dict.keys())[i]].append(cols[i].text)