# DACScraper

> DACScraper is a set of spiders to scrape data from https://www.dac.unicamp.br/portal/graduacao/catalogos-de-cursos
> using the scrapy library.

## Spiders

### coursesRetriever

How to run:
```
scrapy crawl coursesRetriever -a filename="samples/coursesRetrieverSample.json"
```
where the filename must be the location of a json file with an array of objects
with keys 'url' and 'year', sample:
``` 
[
  {
    "url": "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0023/0023.html#MC001",
    "year": 2019
  },
  {
    "url": "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2019/coordenadorias/0032/0032.html#MA044",
    "year": 2019
  }
]
```

## Pipelines

Currently there is a single pipeline that uses MySQL as a database, 
there are json and default Feed Exports available native to scrapy
https://docs.scrapy.org/en/latest/topics/feed-exports.html

### MySQLPipeline
The ```MySQLPipeline``` uses the following settings to connect to the database   
```
dac_user = os.getenv('dac_user')
dac_pwd = os.getenv('dac_pwd')
database_name = os.getenv('database_name', 'dac_database')
dac_host = os.getenv('dac_host', '127.0.0.1')
```
and the files inside the ```sql``` folder to create the tables.
