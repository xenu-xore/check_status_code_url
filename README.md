# Check status code url
Многопоточный чекинг статуса URL c функционалом crawl page

## Start
``` 
pip install -r ./requirements.txt
python ./check_sitemap_url.py 
```

## Input url sitemap.xml

``` Input sitemap url: https://www.google.com/admob/sitemap.xml ```

## Input number of threads
```Input sitemap url: 5 ```

### Result
``` 
    {'status': 302, 'url': 'https://www.google.com/intl/ar_ae/admob/resources.html'}
    {'status': 404, 'url': 'https://www.google.com/intl/es_es/admob/businesskit/growth/'}
    {'status': 404, 'url': 'https://www.google.com/intl/de_de/admob/businesskit/takeaways/'}
```
