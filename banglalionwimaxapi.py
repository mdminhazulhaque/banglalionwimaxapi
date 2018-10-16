#!/usr/bin/env python3

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

"""
Copyright (c) 2018 Md. Minhazul Haque

This file is part of mdminhazulhaque/banglalionwimaxapi
(see {https://github.com/mdminhazulhaque/banglalionwimaxapi).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import json
import requests
import xml.etree.ElementTree as ET
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def html_to_json(content, indent=None):
    soup = BeautifulSoup(content, "lxml")
    rows = soup.find_all("tr")
    
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = thead.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            for index in headers:
                items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        data.append(items)
    return data

def banglalion_wimax_api(username, password):
    BASEURL = 'http://care.banglalionwimax.com/alepowsrc/'

    r = requests.get(BASEURL, allow_redirects=False)
    redir_url = r.headers["Location"]
    cookies = r.cookies
    r = requests.get(redir_url, cookies=cookies)
    
    lines = r.text.split("\n")

    ajax_line = [line for line in lines if 'Wicket.Ajax.ajax({"f":"id3"' in line][0]
    form_line = [line for line in lines if '<form id="id3"' in line][0]

    # JS Part
    script = json.loads(ajax_line.replace("Wicket.Ajax.ajax(", "").replace(");;", ""))
    ajax_url = script['u'].replace("../../../", "")

    # XML Part
    xmlheader = '<?xml version="1.0"?>'
    form_xml = xmlheader + form_line + "</form>"
    form = ET.fromstring(form_xml)
    form_url = form.attrib['action'].replace("../../../", "")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Wicket-Ajax': 'true',
        'Wicket-Ajax-BaseURL': form_url
    }

    data = 'id15_hf_0=&signInForm.username=' + username\
            + '&signInForm.password=' + password\
            + '&signInContainer%3Asubmit=1'

    r = requests.post(BASEURL + ajax_url, headers=headers, cookies=cookies, data=data)

    if "Invalid Username or Password" in r.text:
        raise Exception("Login failed")
    else:
        r = requests.post(BASEURL + "?2", headers=headers, cookies=cookies, data=data)
        
        parsed_html = BeautifulSoup(r.text, 'html.parser')

        accounttable = parsed_html.body.find('table', attrs={'class':'table_column2'})
        internettable = parsed_html.body.find('table', attrs={'class':'dataTable'})

        a = html_to_json(str(accounttable))
        i = html_to_json(str(internettable))

        accountinfo = {
            "user_name": a[0][1],
            "user_id": a[1][1],
            "account_status": a[1][3],
            "total_balance": a[2][1],
            "expiration_date": a[3][1],
            "databank": i[1][1],
            "databank_till": i[1][2],
            "walletbank": i[2][1],
            "walletbank_till": i[2][2],
        }

        return json.dumps(accountinfo, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Banglalion WiMAX API", add_help=False)
    parser.add_argument('-u', dest='user', action="store", required=True, type=str)
    parser.add_argument('-p', dest='pswd', action="store", required=True, type=str)
    args = parser.parse_args()

    try:
        d = banglalion_wimax_api(args.user, args.pswd)
        print(d)
    except:
        print("Invalid Username or Password. Check and retry.")
        
