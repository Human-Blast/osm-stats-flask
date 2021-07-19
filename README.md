# OSM Flask API 

## Introduction

This API is developed by [Errol Joshua][1] and [Jyotsna Sweedle][2] for analysis of the data from OpenStreetMap. The analysis is done on Google Collab and the results of it is stored in Firebase Real-Time Database. The data is served using Flask API hosted on Heroku (See below for API usage).


## API Usage

This API will only work for limited countries and categories which we have chosen and analysed. This is due to the time and data processing retrictions we faced. These are the availabel countries and categories
### Countries

* India
* China
* Brazil
* South Africa
* Russia

These are the BRICS nations which have closed relations in terms of socio-economic growth. 

### Categories

* **Building** : Any structure that is built regardless of using it for commercial or residencial use
* **Leisure** : A place designated as an area to enaged by the public for leisure i.e. Parks
* **Amenity** : Area which provides facilities for people to live in comfort i.e Schools 
* **Office** : Commercial Area where services are traded as commodities
* **Man Made** : A structure of artistic or commercial or public value made by the local governing authorities
* **Advertising** : Structure where adverts are placed
* **Shop**: Commercial Area where goods are traded as commodities
* **Craft** : Small scale industries where goods and manufactured and sold
* **Historic** : Site with Historic importance
* **Landuse** : This describes what the land is used for
* **Tourism** : A place where the tourists frequent and its main source of income is from tourism
* **Boundary** : Sites marked by the governing authorities for different purposes

### Basic Usage
```
https://osm-stats-server.herokuapp.com/osmapi/
```
This is the API endpoint for all the queries. Currently the API will only return Graphs in a base64 string format which needs to be decoded and converted to png to be displayed.

### Getting Graphs

According to our analysis not all countires have the data from the beginning of OSM. India has data from 2014 but Russia has data starting from 2017. Because of this there might be bit mismatch while comparing all years across different nations. Refer the table below

|Country|Starting Year|Ending Year|
|:--:|:--:|:--:|
|India|2014|2021|
|Brazil|2014|2021|
|China|2014|2021|
|South Africa|2017|2021|
|Russia|2016|2019|


But the data is enough to shown one nations across different years and hence we created the API to suit this purpose.

#### All years

``` 
https://osm-stats-server.herokuapp.com/osmapi/pygraph/<country>/<category>
```
This coupled with the countries and categories mentioned above will return a graph in terms of Base64 String which needs to be decoded (Look below for JS code for decoding)

#### One Year

```
https://osm-stats-server.herokuapp.com/osmapi/pygraph/<country>/<category>/<year>
```
This coupled with the countries, categories and years mentioned above will return a graph in terms of Base64 string which needs to be decoded (Look below for JS code for decoding)

**Note** : The years needs ```0101``` added to its end. Example if you are trying to access Indian Craft information of 2019 the it will look like
```
osmapi/pygraph/india/craft/20190101
```


### Decoding Base64 String

JavaScript used for decoding the Base64 string returned by the API for getting the PNG or JPG

```html
<img :src="data" width="100%" height="80%" />
```
Set the variable for the img tag

```javascript
axios.get(this.api_url + "/api/pygraph/"+country+"/" + category)
        .then((res) => {
          this.data = "data:image/png;base64, " + res.data;
        });
```
Using [Axois][3] you can retrive and attach it to the img tag and display it



## Restrictions

Currently one cant retrive the the details of all countries at once

[1]: https://github.com/DocMonster7
[2]: https://github.com/JyotsnaSDsilva
[3]: https://www.npmjs.com/package/axios