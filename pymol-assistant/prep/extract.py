import requests
import pandas as pd
from bs4 import BeautifulSoup


# Step 1: Fetch the webpage
url = "https://pymol.org/pymol-command-ref.html#api"
response = requests.get(url)

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Identify the HTML structure that contains the commands and their documentation
# For this, you would inspect the webpage in your browser and 
# find out which HTML tags hold the command details

cmd_dfs = []

commands = soup.find_all('pre')  # Modify this if the command is within a different tag

# Step 4: Extract the sections based on the <b> tags
for i, command in enumerate(commands):
    command_text = command.get_text(separator='\n')
    
    # Initialize section variables
    sections = {}
    current_section = None
    
    # Loop through the tags to identify sections
    for tag in command:
        if tag.name == 'b':
            # Start a new section
            current_section = tag.get_text(strip=True)
            sections[current_section] = ""
        elif current_section:
            # Add text to the current section
            sections[current_section] += tag.get_text(separator='\n', strip=True) + "\n"
    
    if "DESCRIPTION" in sections and "ARGUMENTS" in sections and 'EXAMPLE' in sections and  "PYMOL API" in sections:
        
        see_also = sections['SEE ALSO'].strip() if "SEE ALSO" in sections else ""
        notes = sections['NOTES'].strip() if "NOTES" in sections else ""

        cmd_dfs.append({
            "name": sections['DESCRIPTION'].split('\n')[0],
            "description": sections['DESCRIPTION'] + see_also + notes,
            "arguments": sections['ARGUMENTS'],
            "example": sections['EXAMPLE'] if "EXAMPLE" in sections else "",
            "usage": sections['PYMOL API'],
        })

        #print("="*50)

# Step 5: Convert the extracted data into a DataFrame
df = pd.DataFrame(cmd_dfs)
df.to_csv("data/pymol_commands_api.csv", index=False)


# Step 1: Fetch the webpage
url = "https://pymolwiki.org/index.php/Category:Commands"
url = "https://pymolwiki.org/index.php?title=Category:Commands&pagefrom=View%0AView#mw-pages"
response = requests.get(url)

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Identify the HTML structure that contains the commands and their documentation
content = soup.find_all('div', {'class': 'mw-category-group'})

view_found = False

base_url = "https://pymolwiki.org/index.php/"

skip_list = [
    'Abort', 
    'Alias',
    'Cealign', # not properly updated, there's no cmd.cealign defined in the docs (but exists in PyMOL)
    'Cls'
    ]

sections_to_extract = [
    'jump to search',
    'usage',
    'arguments',
    'examples',
    'pymol api',
    'notes'
]

results = []

for item in content:
    if "<li>" in str(item):
        elements = item.get_text().split("\n")

        if "View Module" in elements:
            view_found = True
            continue
        
        if view_found:
            #print(elements)
            elements_to_use = [x for x in elements[1:] if x not in skip_list]
            #print(elements_to_use)
            for element in elements_to_use:
                url = base_url + element
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                content = soup.find('div', {'class': 'vector-body'})

                all_text = content.get_text().split("\n")
                # extract the sections
                sections = {}
                current_section = None
                for text in all_text:

                    if text.lower() in sections_to_extract:
                        current_section = text.lower() if text.lower() != 'jump to search' else 'name'
                        sections[current_section] = ""
                    elif current_section:
                        sections[current_section] += text + "\n"

                results.append(
                    {
                        "name": element,
                        "description": sections['name'] + sections.get('notes', ""),
                        "arguments": sections.get('arguments', ""),
                        "example": sections.get('examples', ""),
                        "usage": sections.get('pymol api', "") + sections.get('usage', "")
                    }
                )

# Step 5: Convert the extracted data into a DataFrame
df2 = pd.DataFrame(results)

# save the dataframes to csv
#df2.to_csv("data/pymol_commands_wiki_1.csv", index=False)
df2.to_csv("data/pymol_commands_wiki_2.csv", index=False)


