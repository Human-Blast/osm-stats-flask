from dataclasses import dataclass, astuple, asdict, field
import pyrebase
import pandas as pd
from DataProcess import *


class FirebaseAuthentication:

    def __init__(self):
        self.firebaseConfig = {
        "apiKey": "AIzaSyBTzzXFHncci7RanGMjNfduJ8_471RkYoU",
        "authDomain": "open-street-map-research.firebaseapp.com",
        "databaseURL": "https://open-street-map-research-default-rtdb.firebaseio.com",
        "storageBucket": "open-street-map-research.appspot.com",
        "serviceAccount": "open-street-map-research-firebase-adminsdk-4kv8q-3f47cae2b0.json"
        }
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)

    def run_db(self):
        return self.firebase.database()

    def run_store(self):
        return self.firebase.storage()



@dataclass(order=True)
class DataAccess:
    """Class for validations of requests and Data Access"""

    db: pyrebase.pyrebase.Database 
    country: str
    category: str
    countriesInDB: list
    categoriesInDB: list
    allYears:list = field(init=False, default_factory = list)
    

    def ValidateRequestAllYears(self):
        """Validates given request"""
        if(self.country.lower() in self.countriesInDB and self.category.lower() in self.categoriesInDB):
            return True
        
        return False

    def ValidateRequestOneYear(self, year):
        """Validates given request for given one year"""
        
        if(self.country.lower() in self.countriesInDB and self.category.lower() in self.categoriesInDB and year in self.allYears):
            return True
        
        return False

    def GetallYears(self):
        return self.allYears
       
    def GetTop5_JSON_DataOfAllYears(self):
        """Returns JSON Data having Top 5 category details for all years of a country"""
        
        if self.ValidateRequestAllYears():
            category_index = self.categoriesInDB.index(self.category)
            category_data = self.db.child('/osm_data/analyzed/' + self.country + '/top_5/data/' + str(category_index) + '/' + self.category).get()
            self.allYears = self.db.child('/osm_data/dates/'+self.country).get().val()
            
            return category_data.val() #return json dictionary data
            
        return None


    def GetTop10_DataFrame_DataOfOneYear(self):
        """Returns pd.DataFrame Data having Top 10 category details of one year of a country"""

        self.allYears = self.db.child('/osm_data/dates/'+self.country).get().val()

        if len(self.allYears) == 1:
            year = str(self.allYears[0])
            if self.ValidateRequestOneYear(year):
                category_index = self.categoriesInDB.index(self.category)
                json_dict = self.db.child('/osm_data/analyzed/' + self.country + '/top_10/data/' + str(category_index) + '/' + self.category + '/' + year).get().val()
                df = pd.DataFrame(json_dict,index=[year for i in range(len(json_dict['frequency']))])
                
                return df #return dataframe
                
        return pd.DataFrame() #return empty dataframe


    def GetTop5_DataFrame_DataOfAllYears(self):
        """Returns pandas.DataFrame Data having Top 5 category details for all years of a country"""

        json_data = self.GetTop5_JSON_DataOfAllYears()

        if json_data != None:
            if len(self.allYears) > 1:
                dfs_created = []

                for year in self.allYears:
                    df_name = self.category +'_'+ str(year)
                    globals()[df_name] = pd.DataFrame(json_data[str(year)],index=[str(year) for i in range(len(json_data[str(year)]['frequency'])) ])
                    dfs_created.append(globals()[df_name])
                
                if len(dfs_created) > 0:
                    return pd.concat(dfs_created) # return dataframe
                
                return pd.DataFrame()

            elif len(self.allYears) == 1:
                year = str(self.allYears[0])
                return pd.DataFrame(json_data[year], index=[year for i in range(len(json_data[year]['frequency']))]) # return dataframe
            
            return pd.DataFrame()
        return pd.DataFrame()


    def GenerateAndSendDataTo_DataProcess(self, plot_kind):
        """Gets data and sends it to DataProcess for Graph generation"""

        try:
            df = self.GetTop5_DataFrame_DataOfAllYears()
            print (df)

            if df.empty:
                return None 
            
            x = Data_Manipulation(data = df, years = self.allYears,  country = self.country, category = self.category)
            return x.RefineData_and_GenerateGraph(plot_kind)

        except Exception:
            return Exception


      

                    
                    
            


        
    
