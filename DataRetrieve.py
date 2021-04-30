import matplotlib.pyplot as plt
import seaborn as sns

class Data_Manipulation:

    def __init__(self, data, years, category, country):
        self.data = data
        self.years = years
        self.category = category 
        self.country = country

    def GenerateBarGraph_in_subplots(self, dfs_created_in_RefineData):
        # print(dfs_created_in_RefineData)

        def get_factors(n):
            for i in range(1, int(pow(n, 1 / 2))+1):
                if n % i == 0:
                    res =  [i,int(n / i)]
            return res

        
        row_col = get_factors(len(self.years))

        # graph generation begins here
        fig, ax = plt.subplots(nrows=row_col[0], ncols=row_col[1],figsize = (25, 25))
        ct=0

        for row in ax:
            for col in row:
                df_individual = dfs_created_in_RefineData[ct]
                # print(globals()[df_individual])
                ct += 1 
                
                col.bar(globals()[df_individual]['tag_name'], globals()[df_individual]['frequency'])
                col.set_title(str(self.country)+'_'+str(self.category))
                # plt.savefig(str(self.country) + '.png',bbox_inches='tight', dpi=300)
        
        return fig 

    def RefineData_and_GenerateGraph(self):
        df = self.data
        # print('Given category -- ',self.category)
        # print('years of data -- ',self.years)

        grouped_df = df.groupby(df.index)
        dfs_created_in_RefineData = []

        for year in self.years:
            df_name = 'df_'+ str(year)
            globals()[df_name] = grouped_df.get_group(str(year))
            #print(globals()[df_name])
            dfs_created_in_RefineData.append(df_name)
            

        return self.GenerateBarGraph_in_subplots(dfs_created_in_RefineData)

    

        
