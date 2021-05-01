import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
from itertools import count, islice

class Data_Manipulation:

    def __init__(self, data, years, category, country):
        self.data = data
        self.years = years
        self.category = category 
        self.country = country

    def get_factors(self, n):
        for i in range(1, int(pow(n, 1 / 2))+1):
            if n % i == 0:
                res =  [i,int(n / i)]
        return res
    
    def is_prime(self, n):
        return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))

    # graph generation begins here
    def GenerateBarGraph_in_subplots(self, dfs_created_in_RefineData):

        row_col = self.get_factors(len(self.years))
        fig, ax = plt.subplots(nrows=row_col[0], ncols=row_col[1],figsize = (25, 25))
        ct=0

        for row in ax:
            for col in row:
                df_individual = dfs_created_in_RefineData[ct]
                ct += 1 
                
                col.bar(globals()[df_individual]['tag_name'], globals()[df_individual]['frequency'])
                col.set_title(str(self.country)+'_'+str(self.category))

        return fig 

    def GenerateBarGraph_seaborn(self, dfs_created_in_RefineData):
        
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

                    print(c)
                    print(dfs_created_in_RefineData[c])
                    df_individual = dfs_created_in_RefineData[c]
                    sns.set_theme(font_scale=2)
                    
                    bar = sns.barplot(ax=ax[i,j], data=globals()[df_individual], 
                                x ='tag_name', y='frequency',estimator=sum,
                                saturation=0.5, palette="flare")
                            
                    bar.set(title=str(self.years[c]))
                    bar.set_xticklabels(bar.get_xticklabels(),rotation=90,fontdict={'fontsize': 19})
                    c += 1  

                if c >= len(dfs_created_in_RefineData):
                    break
                

            plt.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50) 
            fig.tight_layout()
            c=0
            return fig

        else:
            fig, ax = plt.subplots(nrows=row_col[0], ncols=row_col[1],figsize = (25, 10))
            for i in range(row_col[1]):
                df_individual = dfs_created_in_RefineData[c]
                sns.set_theme(font_scale=2)
                    
                bar = sns.barplot(ax=ax[i], data=globals()[df_individual], 
                            x ='tag_name', y='frequency',estimator=sum,
                            saturation=0.5, palette="flare")
                            
                bar.set(title=str(self.years[c]))
                bar.set_xticklabels(bar.get_xticklabels(),rotation=90,fontdict={'fontsize': 19})
                c += 1  

            plt.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50) 
            fig.tight_layout()
            c=0
            return fig    

    def RefineData_and_GenerateGraph(self, plot_kind):
        df = self.data
        grouped_df = df.groupby(df.index)
        dfs_created_in_RefineData = []

        for year in self.years:
            df_name = 'df_'+ str(year)
            globals()[df_name] = grouped_df.get_group(str(year))
            dfs_created_in_RefineData.append(df_name)
            
        if plot_kind.lower() == 'bar':
            return self.GenerateBarGraph_seaborn(dfs_created_in_RefineData)
        
        

    

        
