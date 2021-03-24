

PROJECT_NAME = "sayfa_dev"

CRONJOB_PATH = "/etc/cron.d/"+PROJECT_NAME
CRONJOBS = [
    '0 */4 * * * /usr/bin/python {}/get_news.py',
    '0 */4 * * * /usr/bin/python {}/rank_db.py'
]

REQUIRED_NEWS_FIELDS = ['title','category','url']

LINK_PATH_LIST = [
    "/mnt/News/Documents/PROJECTS/sayfa_dev/init/link_list.csv",
    "/mnt/News/Documents/PROJECTS/sayfa_dev/init/rss_list.csv"
    ]
CATEGORY_PATH_LIST = [
    "/mnt/News/Documents/PROJECTS/sayfa_dev/init/category_list.txt"
]

#this value determines ranking range(comparing pool) and also what we serve
#week-start,debug are the only implemented presets
RANK_DATE_EPOCH = "debug"

MONGO_URL = "mongodb://localhost:27017/"

#to avoid common name collisions...
MONGO_DB_NAME = "db_"+PROJECT_NAME

COL_CRAWL_TARGET = "crawl_target"
COL_LINK_INDEX = "link_index"
COL_CATEGORY = "category"
COL_NEWS_CONTENT = "news"
