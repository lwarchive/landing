from string import Template
from bs4 import BeautifulSoup

import requests
import datetime
import sys

resp = requests.get(f"https://api.github.com/orgs/{sys.argv[1]}/repos")
output = []

print(f"Polling repositories for {sys.argv[1]}")

for i in resp.json():
    if (i["homepage"] is not None):
        if (i['name'] not in sys.argv[2]):
            output.append(f"\t\t<tr><td><a href=\"{i["homepage"]}\">{i["name"]}</a></td><td><a href=\"{i["html_url"]}\">Source</a></td></tr>")

print(f"Created {len(output)} link(s) for discovered projects.")

with open('template.html', 'r') as f:
    templateText = Template(f.read())

with open('output/index.html', 'w') as fw:
    soup = BeautifulSoup(templateText.substitute(body='\n'.join(output), footer=f'<i>Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for {sys.argv[1]}</i>'), "html.parser")
    fw.writelines(soup.prettify())
    
print("Done!")