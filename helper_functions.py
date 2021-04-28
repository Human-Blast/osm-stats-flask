def download_csv(country,category):
    store.child(country+"/"+category+".csv").download("./download/"+country+"_"+category+".csv")
    os.remove("./download/"+country+"_"+category+".csv")

