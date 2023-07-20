import requests
import json
import config

# Notion secret key
NOTION_SECRET = config.NOTION_SECRET # this is received after making an integration in notion
DATABASE_ID = config.DATABASE_ID
POST_DATABASE_ID = config.POST_DATABASE_ID #created separate db to test Post and Patch

# Headers
headers = {
    "Authorization": "Bearer " + NOTION_SECRET,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

"""
# GET DATA :: WORKS
"""
def get_pages(num_pages= None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query" #allows you to query any table with any filters as needed (similar to sql)

    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    # Comment this out to dump all data to a file
    # import json
    #with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)
    
    #with open('db_TEST_POST_PATH_DELETE.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    return results

pages = get_pages()

for page in pages:
    page_id = page["id"]
    props = page["properties"]
    Month = props["Month"]["title"][0]["text"]["content"]
    foodbeverage = props["food-beverage"]["rich_text"][0]["text"]["content"] #do the same for the other columns
    restaurantcafe = props["Restaurants-cafes"]["rich_text"][0]["text"]["content"]
    rentpricegrowth = props["Rental-price-Growth"]["rich_text"][0]["text"]["content"]
    electricenergyprice = props["Energy-prices-electricity"]["rich_text"][0]["text"]["content"]
    gasenergyprice = props["Energy-prices-Gas"]["rich_text"][0]["text"]["content"]

    print(Month,'\t', foodbeverage, '\t', restaurantcafe, '\t',rentpricegrowth, '\t',electricenergyprice, '\t',gasenergyprice)

"""
# POST stuff (or in notion create a new page)   :: WORKS
"""
def create_page(data: dict):        
    create_url = f"https://api.notion.com/v1/pages"

    payload = {"parent":{"database_id": POST_DATABASE_ID}, "properties": data}

    res = requests.post(create_url, json=payload, headers=headers)
    print(res.status_code)
    return res
    

Month = "Jul-23"
foodbeverage = "1"
restaurantcafe = "0.9"
rentpricegrowth = "3.4"
electricenergyprice = "50.3"
gasenergyprice = "76.1"

# check the Json file and see if below is correct, will not work otherwise
data = {
    "Month": {"title": [{"text": {"content": Month}}]},
    "food-beverage": {"rich_text": [{"text": {"content": foodbeverage}}]},
    "Restaurants-cafes": {"rich_text": [{"text": {"content": restaurantcafe}}]},
    "Rental-price-Growth": {"rich_text": [{"text": {"content": rentpricegrowth}}]},
    "Energy-prices-electricity": {"rich_text": [{"text": {"content": electricenergyprice}}]},
    "Energy-prices-Gas": {"rich_text": [{"text": {"content": gasenergyprice}}]}
}

create_page(data)

"""
# PATCH stuff.  
This is to update values in db
"""

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id1}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    print(res.status_code)
    return res

#make sure page_id is updated otherwise you get a 400 error
page_id1 = config.pageid_access_token1 #get this from db.json under results, below page

new_val1 = "updated val 1"
new_val2 = "updated val 2"
new_val3 = "updated val 3"

update_data = {
    "food-beverage": {"rich_text": [{"text": {"content": new_val1}}]},
    "food-beverage": {"rich_text": [{"text": {"content": new_val2}}]},
    "Restaurants-cafes": {"rich_text": [{"text": {"content": new_val3}}]},
}

update_page(page_id, update_data)


"""
# DELETE stuff.  
This is to delete values in db
"""
def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id2}"

    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)
    print(res.status_code)
    return res

#make sure page_id is updated otherwise you get a 400 error
page_id2 = config.pageid_access_token2 # same page id as in PATCH

delete_page(page_id)
