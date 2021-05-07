from dataclasses import dataclass, astuple, asdict
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
from itertools import count, islice
import numpy as np
from matplotlib import cm
import pandas as pd
# from pprint import pprint
# import inspect
from ImageProcess import *

@dataclass(frozen=True, order=True)
class Data_Manipulation:
    """A class for Data manipulation and Graph generation"""

    data: pd.DataFrame
    years: list
    category: str
    country: str

    def convertImage(self, fig):
        """Converts image to Base64 string"""
        file_name = 'test.svg'
        plt.savefig(file_name, dpi=100) 

        _img_ = ImageProcess(fig)
        return _img_.ImageToBase64()

    def get_factors(self, n): #get factors of a number in pairs
        for i in range(1, int(pow(n, 1 / 2))+1):
            if n % i == 0:
                res =  [i,int(n / i)]
        return res
    
    def is_prime(self, n): #check if a number is prime
        return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))

    # graph generation begins here
    def GenerateBarGraph_in_subplots(self, dfs_created_in_RefineData):
        """Generate bar plot from matplotlib for all years"""
        if len(self.years) > 5 and self.is_prime(len(self.years)): #if plots needed are more than 5 and is prime
            row_col = self.get_factors(len(self.years)+1) #add a number and make it even, then get factors
        else:
            row_col = self.get_factors(len(self.years)) #get factors as it is

        ct=0
        
    
        if row_col[0] > 1:
            fig, ax = plt.subplots(row_col[0], row_col[1], figsize=(30, 25)) #init figure with desired subplots

            if len(self.years) > 5 and self.is_prime(len(self.years)): #delete redundant subplot
                fig.delaxes(ax[row_col[0]-1,row_col[1]-1])

            for row in ax:
                for col in row:
                    if ct >= len(dfs_created_in_RefineData):
                        break

                    df_individual = dfs_created_in_RefineData[ct] #extract individual df
                    
                    my_colors = [(x/10.0, x/15.0, 0.75) for x in range(len(df_individual))]
                    # my_colors = cm.inferno_r(np.linspace(.4, .8, 20))
                    col.bar(globals()[df_individual]['tag_name'], globals()[df_individual]['frequency'],alpha=0.75,color=my_colors) #plot bar graph
                    col.set_title(str(self.years[ct]),fontdict={'fontsize': 20})
                    col.set_xticklabels(globals()[df_individual]['tag_name'],rotation=90,fontdict={'fontsize': 19})
                    col.grid(axis='y',which='both',drawstyle= 'steps-pre')
                    col.set_axisbelow(True)
                    # col.set_xlabel('Tag Name', fontsize=19)
                    # col.set_ylabel('Frequency', fontsize=19)
                    ct += 1

                if ct >= len(dfs_created_in_RefineData):
                    break
            
            
            fig.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50)
            fig.tight_layout()
         
            return self.convertImage(fig)

        else:
            fig, ax = plt.subplots(nrows=row_col[0], ncols=row_col[1],figsize = (25, 10))

            for i in ax:
                df_individual = dfs_created_in_RefineData[ct]
                my_colors = [(x/10.0, x/15.0, 0.75) for x in range(len(df_individual))]
                i.bar(globals()[df_individual]['tag_name'], globals()[df_individual]['frequency'],alpha=0.6,color=my_colors) 
                i.set_title(str(self.years[ct]),fontdict={'fontsize': 20})
                i.set_xticklabels(globals()[df_individual]['tag_name'],rotation=90,fontdict={'fontsize': 19})
                i.grid(axis='y',which='both',drawstyle= 'steps-pre')
                i.set_axisbelow(True)
                # i.set_xlabel('Tag Name', fontsize=19)
                # i.set_ylabel('Frequency', fontsize=19)
                ct += 1 

            fig.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50)
            fig.tight_layout()
            
            
            return self.convertImage(fig)
            

    def GenerateBarGraph_seaborn(self, dfs_created_in_RefineData):
        """Generate Bar plot from seaborn for all years"""
        if len(self.years) > 5 and self.is_prime(len(self.years)):
            row_col = self.get_factors(len(self.years)+1)
        else:
            row_col = self.get_factors(len(self.years))

        c=0

        if row_col[0] > 1:
            fig, ax = plt.subplots(row_col[0], row_col[1], figsize=(30, 25))

            if len(self.years) > 5 and self.is_prime(len(self.years)):
                fig.delaxes(ax[row_col[0]-1,row_col[1]-1])

            for i in range(row_col[0]):
                for j in range(row_col[1]):

                    if c >= len(dfs_created_in_RefineData):
                        break

                    df_individual = dfs_created_in_RefineData[c]
                    sns.set_theme(font_scale=2)
                    
                    bar = sns.barplot(ax=ax[i,j], data=globals()[df_individual], 
                                x ='tag_name', y='frequency', palette="flare")
                            
                    bar.set(title=str(self.years[c]))
                    bar.set_xticklabels(bar.get_xticklabels(),rotation=90,fontdict={'fontsize': 19})
                    c += 1  

                if c >= len(dfs_created_in_RefineData):
                    break
                

            plt.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50) 
            fig.tight_layout()

            return self.convertImage(fig)

        else:
            fig, ax = plt.subplots(nrows=row_col[0], ncols=row_col[1],figsize = (25, 10))
            for i in range(row_col[1]):
                df_individual = dfs_created_in_RefineData[c]
                sns.set_theme(font_scale=2)
                    
                bar = sns.barplot(ax=ax[i], data=globals()[df_individual], 
                            x ='tag_name', y='frequency', palette="flare") #estimator=sum
                            
                bar.set(title=str(self.years[c]))
                bar.set_xticklabels(bar.get_xticklabels(),rotation=90,fontdict={'fontsize': 19})
                c += 1  

            plt.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50) 
            fig.tight_layout()

            return self.convertImage(fig)    

    def GenerateGraph_seaborn_year(self,df_ofGivenYear,year):
        """Bar plot for one year, one category of a country"""
        fig = plt.figure(figsize = (20, 15))
        sns.set_theme(font_scale=2)
        ax = sns.barplot( data=df_ofGivenYear, 
                        x ='tag_name', y='frequency', palette="flare")

        ax.set(title=str(year))
        ax.set_xticklabels(ax.get_xticklabels(),rotation=45,fontdict={'fontsize': 19})
        fig.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50)
        fig.tight_layout()

        return self.convertImage(fig)


    def RefineData_and_GenerateGraph(self, plot_kind):
        """Does the job it is told to"""
        # pprint(inspect.getmembers(Data_Manipulation, inspect.isfunction))

        try:
            if len(self.years) > 1:
                grouped_df = self.data.groupby(self.data.index)
                dfs_created_in_RefineData = []

                for year in self.years:
                    df_name = 'df_'+ str(year)
                    globals()[df_name] = grouped_df.get_group(str(year))
                    dfs_created_in_RefineData.append(df_name)
                    
                if plot_kind.lower() == 'bar':
                    return self.GenerateBarGraph_in_subplots(dfs_created_in_RefineData)

            else:
                if plot_kind.lower() == 'bar':
                    return self.GenerateGraph_seaborn_year(self.data,str(self.years[0]))
        except Exception:
            return Exception
        
    

        
