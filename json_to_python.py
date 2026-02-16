import json
# import jmespath
structured_data = dict()

#function to read json and return raw_json dict
def read_load_json(raw_json):
    with open(raw_json, "r") as file:
        python_obj = json.load(file)
        raw_json_dict = dict(python_obj)
        return raw_json_dict    
    
#function to parse raw__dict and return structured dict
def json_parser(raw_dict):
        
        structured_data["restaurant_id"]=raw_dict.get("page_info").get("resId")
        structured_data["restaurant_name"]=raw_dict.get("page_info").get("ogTitle")
        

        structured_data["restaurant_contact"] = [raw_dict.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("phoneDetails").get("phoneStr")]  
        structured_data["fssai_licence_number"]=raw_dict.get("page_data").get("order").get("menuList").get("fssaiInfo").get("text")
        structured_data["address_info"]={
             "full_address":raw_dict.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("address"),
             "region":raw_dict.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("country_name"),
             "city":raw_dict.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("city_name"),
             "pincode":raw_dict.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("zipcode"),

             "state":"Gujrat"
             }
        


       

        structured_data["cuisines"]=[
             {"name":i.get("name"),
                "url":i.get("url")
             }
             for i in raw_dict.get("page_data").get("sections").get("SECTION_RES_HEADER_DETAILS").get("CUISINES")
        ]

        
        structured_data["timings"]={
             
            "monday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},
            "tuesday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},
            "wednssday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},
            "thursday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},
            "fridayday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},
            "saturdayday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},
            "sunday":{"open":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":raw_dict["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[-1]},

            
        }
             
    
       
       


        store=[]
        for i in raw_dict["page_data"]["order"]["menuList"]["menus"]:
            
            for j in i["menu"]["categories"]:
                temp_dict=dict()
                temp_dict['category_name'] = j["category"]["name"]
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
def structured_data_func(res):
    with open("ZOMATO_16_02_2025.json","w") as file:
         file.write(json.dumps(res))
    


raw_json = "D:\\Siddharth\\JSON\\zomato_data.json"

raw_dict = read_load_json(raw_json)
res=json_parser(raw_dict)
structured_data_func(res)
