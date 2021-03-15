# Warning !
```
this app is in it's early stages and everything below is in the sketch state.
``` 

# Intro

This project aims to create a platform to develop ranking algorithms for news
i tried to maximize modularity to keep modifications easy

I'm also hoping to share the database once the dev cycle settles

currently it only keeps track of scientific news but its trivial to add new news targets.

check the TODO file for problems

# Folder Structure
123


# Running your own server

## Installation
front end uses semantic ui

Project has seed links by default but if you want to use your own links, edit the `link_list.csv`  `rss_list.csv`  `category_list.txt`

make sure you have mongodb, python installed
1. Install python requirements
```bash
$ pip install -r requirements.txt
```
2. Confirm settings on config.py
3. Run <b>`insert_links.py`</b> provides seed links <b>to other url feeds</b> for crawlers, meant to be crawled reqularly.
4. Run <b>`insert_categories.py`</b> (provides possible category names)
5. Run <b>`cronjobs.py`</b> sets the cronjob for crawler and ranker (check `config.py` for path )
6. Run <b>`get_news.py`</b> starts calling each crawler and collect data
7. Run <b>`rank_db.py`</b> queries collected news data and ranks them with available rankers. 
query has a specific date range (check `config.py` for date range )

Now you are ready to run the server !
```
python server.py
```

`rank_db.py`
Explanation
`get_news.py`
Explanation

## Collected Data
### News Data

Not every field crawlers collect are required but can changed in the `config.py` file
After crawler parses the data `validate.py` checks the data for specified key's existence
| Field Key | Required ? | Comment
| ------------- |-------------|-------------|
|`title`| YES |   |
|`category`| YES |  |
|`url`| YES |  |
|page_type| NO | determines which crawler to use|
|date| NO | utc format |
|subtitle| NO | decription |
|author| NO |  |
|domain| NO | url's domain |



# Adding a new Ranker

Only requirement for each ranker package is that <b>it accepts and returns a dict object.</b>

You have to check for field existence since news data keys can vary
ranker package should be located in the `rank` folder and start with the prefix `rank_` 


### After you create your ranker update the following files
1. project_root/rank/`__init__.py` (links package)
2. project_root/static/`ranker_data.js` add json to link your ranker to front end

## ranker_data.js example json
```
    {
    "text":"Shortest Title",
    "value":"shortest_title",  
    "icon":"eye",     
    },
```
| key |  purpose
| -------------|-------------|
|`text`| what user sees
|`value`|must match with __init__.py file in your package
|`icon`|possible values; [Semantic UI Icons](https://semantic-ui.com/elements/icon.html) |


## Adding a new link
if you haven't started the server you should add it to `link_list.csv` or `rss_list.csv `

if you started the server use the `add_link.py` inside the `utils` folder
it will handle category creation and insert the link to mongo collection `crawl_target`


## License
[MIT](https://choosealicense.com/licenses/mit/)
