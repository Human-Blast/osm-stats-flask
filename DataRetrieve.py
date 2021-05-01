import matplotlib.pyplot as plt
import seaborn as sns

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
        
        row_col = self.get_factors(len(self.years))
        fig, ax = plt.subplots(row_col[0], row_col[1], figsize=(30, 25))
        c=0

        for i in range(row_col[0]):
            for j in range(row_col[1]):
                df_individual = dfs_created_in_RefineData[c]
                # sns.set(font_scale = 2)
                sns.set_theme(font_scale = 2)
                bar = sns.barplot(ax=ax[i,j], data=globals()[df_individual], 
                            x ='tag_name', y='frequency',estimator=sum,
                            saturation=0.5, palette="flare")
                # sns.set_context("paper", font_scale=0.9)
                        
                bar.set(title=str(self.years[c]))
                bar.set_xticklabels(bar.get_xticklabels(),rotation=90,fontdict={'fontsize': 19})
                c += 1   
        plt.suptitle(str(self.country).upper()+ '-' +str(self.category).upper(), fontsize=50) 
        fig.tight_layout() 
        
       
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
        
        

    

        
