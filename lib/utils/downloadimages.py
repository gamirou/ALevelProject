from icrawler.builtin import BingImageCrawler

folder_name = r"dataset/train/dog"
keyword='dog'
max_num=10

bing_crawler = BingImageCrawler(storage={'root_dir': folder_name})
bing_crawler.crawl(keyword=keyword, max_num=max_num)

# google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'dataset/train/dog'})
# google_Crawler.crawl(keyword = 'dog', max_num = 10)