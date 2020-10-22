# DACScraper

> DACScraper is a set of spiders to scrape data from https://www.dac.unicamp.br/portal/graduacao/catalogos-de-cursos
> using the scrapy library.

## Spiders

### coursesLister

Spider to list all courses urls for a catalog year and add to 'CourseIdURLItem'.

How to run:
```
scrapy crawl coursesLister -a filename="samples/coursesListerSample.json" -o .scrapy/outputCoursesLister.json
```
where the filename must be the location of a json file with an 'urls' key and an array of urls, sample:
``` 
{
  "urls": [
    "https://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2020/TiposDisciplinas.html"
  ]
}
```

The output can be used as input for the ```coursesRetriever``` spider.

### coursesRetriever

Spider to retrieve info about courses and add to a 'CourseItem' using the urls from ```coursesLister``` output.

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

### semestersLister

Spider to list all the 'majors' codes and add to 'CourseListItem' objects.

How to run:
```
crawl semestersLister -a first_year="2019" -a last_year="2020" -o ".scrapy/outputSemesterLister.json"
```
The oldest ```first_year``` supported is 2013, and the ```last_year``` is the year of the last catalog available. 

The output can be used as input for the ```semestersRetriever``` spider.


## Pipelines

Currently there is a single pipeline that uses MySQL, there are json and default Feed Exports available native to scrapy
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
