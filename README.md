# OSM Flask API 

## API Usage

```
https://osm-stats-server.herokuapp.com/<Country>/<Category>
```
Is the basic syntax of the API. Following countries are valid for quering

```python
countries =['brazil','india','china','south africa','russia']
```
And Following categories are valid

```python
category_ = ['building','leisure','amenity','office','man_made','advertising','shop','craft','historic','landuse','tourism','boundary']
```
To get the details of all categories ```all``` must added instead of a specific category

### GET Request
    This can be used to check whether a countires exists or not as well as a category

### POST Request
    The content is access only through a POST request due to the size of the json data

## Restrictions

Currently one cant retrive the the details of all countries at once