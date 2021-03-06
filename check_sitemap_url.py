from multiprocessing import Pool
import requests
import bs4
import csv
# import lxml.html
import signal
import argparse


class Crawl(object):


    HEADERS = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    FILE = 'file_name1'
    # SITEMAP = r"C:\Users\xor\Desktop\sitemap-model_main-000.xml"

    def __init__(self, sitemap, format_file="url"):
        self.sitemap = sitemap
        self.format_file = format_file

    def fetch_urls(self):
        """Сбор URL из sitemap для дальнейшего обхода в behavior(data_urls)"""
        try:
            if self.format_file == 'url':
                c = requests.get(self.sitemap, allow_redirects=True, headers=self.HEADERS, timeout=1)
                soup = bs4.BeautifulSoup(c.content, 'html.parser')

                list_urls_s = [i.get_text() for i in soup.find_all('loc')]
                return list_urls_s

            elif self.format_file == 'txt':
                with open(self.sitemap, 'r') as f:
                    list_urls_s = f.read().splitlines()
                    return list_urls_s

            elif self.format_file == 'xml':
                with open(self.sitemap, 'r') as f:
                    soup = bs4.BeautifulSoup(f, 'html.parser')
                    list_urls_s = [i.get_text() for i in soup.find_all('loc')]
                    return list_urls_s

        except Exception as e:
            return e

    # noinspection PyAttributeOutsideInit
    def behavior(self, data_urls, timeout=5):
        """Поведение(обработка) полученых из data() URL"""
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        global status, urls
        try:

            r = requests.get(data_urls, allow_redirects=False, headers=self.HEADERS, timeout=timeout)

            # check content page (crawl)
            """
            soup1 = bs4.BeautifulSoup(r.content, 'html.parser')
            lxml_xpath = lxml.html.fromstring(r.content)
            description = lxml_xpath.xpath('//meta[@name="description"]/@content')[0]
            title = lxml_xpath.xpath('//title/text()')[0]
            h1 = soup1.find('h1').get_text()
            text = soup1.get_text(strip=False)
            """

            # check status code
            urls = r.url
            status = r.status_code

            # full check crawl and status code add data dict
            # dicts = {'status': status, 'h1': h1, 'description': description, 'title': title, 'url': url, 'text': text}
            dicts = {'status': status, 'url': urls}
            print(dicts)

        except Exception as e:
            # dicts = {'status': 'None', 'h1': 'None', 'description': 'None', 'title': 'None', 'url': data_urls,
            #         'text': 'None'}
            print('Ошибка: %r' % e)
            dicts = {'status': status, 'url': urls}
            print(dicts)

        self.csv_writer(dicts)
        return None

    # noinspection PyAttributeOutsideInit
    def csv_writer(self, data):
        self.data = data
        """Запись полученых данных из behavior(data_urls)"""
        with open(self.FILE + '.csv', 'a') as f:
            writer = csv.writer(f, delimiter=";", lineterminator="\r")
            # full write data csv crawl and status code and url
            # writer.writerow((self.data['status'], self.data['h1'], self.data['description'], self.data['title'], \
            #                 self.data['url'], self.data['text']))
            writer.writerow((self.data['status'], self.data['url']))
            f.close()

    def PoolCrawl(self, n):
        """Построение событий мультипроцессеринга"""
        pool = Pool(n)

        try:
            pool.map_async(self.behavior, self.fetch_urls()).get(900)
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url", type=str, help="Url")
    parser.add_argument("-F", "--file_name", type=str, help="File_name")
    parser.add_argument("-t", "--threads", type=int, help="Threads")
    # parser.add_argument("-f", "--format_file", type=str, help="Format_file")
    args = parser.parse_args()

    if args.url and args.threads:
        m = Crawl(args.url)
        m.PoolCrawl(args.threads)

    elif args.file_name and args.threads:
        format_file_split = args.file_name.split(".")
        m = Crawl(args.file_name, format_file=format_file_split[-1])
        m.PoolCrawl(args.threads)

    else:
        parser.print_help()