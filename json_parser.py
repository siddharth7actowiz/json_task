import json
from datetime import *
import re
structured_data = dict()
#raw json file path
raw_json = "input_zomato_data.json"

#filename for structured_json
f_name="ZOMATO"
today=datetime.today()
todays_date=datetime.strftime(today,"%Y_%m_%d")
file_name=f"{f_name}_{todays_date}.json"


#function to read json and return raw_json dict
def read_json(raw_json):
    with open(raw_json, "r") as file:
        python_obj = json.load(file)
        print(type(python_obj))
        raw_json_dict = dict(python_obj)
        return raw_json_dict    
    
#function to parse raw__dict and return structured dict
def json_parser(raw_dict):
        
        #Restro
        base_index=raw_dict.get("page_info")
        structured_data["restaurant_id"]=base_index.get("resId")
        structured_data["restaurant_name"]=base_index.get("ogTitle")
        
        common_index=raw_dict.get("page_data").get("sections").get("SECTION_RES_CONTACT")
        structured_data["restaurant_contact"] = [common_index.get("phoneDetails").get("phoneStr")]  
        #for fssai_licence_number only
        fassi_num=raw_dict.get("page_data").get("order").get("menuList").get("fssaiInfo").get("text")
        match=re.search("\d+",fassi_num)
        structured_data["fssai_licence_number"]=match.group()
       
       
       
        structured_data["address_info"]={
             "full_address":common_index.get("address"),
             "region":common_index.get("locality_verbose"),
             
             "city":common_index.get("city_name"),
             "pincode":common_index.get("zipcode"),

             "state":"Gujrat"
             }
        #region 
        old_reg=structured_data["address_info"]["region"]
        structured_data["address_info"]["region"]=old_reg.replace(old_reg,"Ambali").strip()



        structured_data["cuisines"]=[
             {"name":i.get("name"),
                "url":i.get("url")
             }
             for i in raw_dict.get("page_data").get("sections").get("SECTION_RES_HEADER_DETAILS").get("CUISINES")
        ]

        #Restro openning and Closing timing
        common_path2=raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"]
        days=["monday","tuesdy","wednsday","thursday","friday","saturday","sunday"]
        open_time=common_path2.split()[0]
        if open_time in ["12noon","noon","Noon","12Noon"]:
             open_time="12pm"


        close_time=common_path2.split()[-1]
        
       
        
        structured_data["timings"]={
            
            day:{"open":open_time,"close":close_time}
            for day in days
                      
        }
             
        
        store=[]
        for i in raw_dict["page_data"]["order"]["menuList"]["menus"]:
            
            for j in i["menu"]["categories"]:
                temp_dict=dict()
                #if category name is not avilable we have fallback to menu name
                temp_dict["category_name"] = (j.get("category", {}).get("name") or i.get("menu", {}).get("name"))
                temp_dict['items'] = [
                {
                    
                    "item_id": item["item"]["id"], 
                    "item_name": item["item"]["name"],
                    "item_slugs": item["item"]["tag_slugs"],
                    "item_description":item["item"]["desc"],
                    "is_veg":  item["item"]["dietary_slugs"][0] == "veg" 
                } 
                for item in j["category"]["items"] 
                ]
                store.append(temp_dict)
        
        structured_data["menu_categories"] = store
        print(structured_data)
        return structured_data



#function for structured_json
def export_structured_data_func(res):
    with open(file_name,"w") as file:
         file.write(json.dumps(res))
    

# Function call to load jsion 
raw_dict = read_json(raw_json)


#Function Call to Parse Json
res=json_parser(raw_dict)


# #Function call to create json file
export_structured_data_func(res)
