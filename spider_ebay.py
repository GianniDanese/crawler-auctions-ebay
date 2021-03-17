import scrapy, re, os
import my_spider_functions as sp_fun
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import telegramfunctions as telegram

class MySpider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['www.ebay.it']
    start_urls = []
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36' 

    def __init__(self, time_set, max_price, urls=[], *args, **kwargs):
        self.time_set = int(time_set)
        self.max_price = float(max_price)
        self.start_urls = urls.split(',')
        super(MySpider, self).__init__(*args, **kwargs)


    ###                                          ###
    #Collecting auction links on the results page#
    ###                                          ###
    def parse(self, response):
        all_item = response.xpath("//div[@id='srp-river-results']/ul[@class='srp-results srp-list clearfix']/li")
        for item in all_item:
            item_url = item.xpath(".//div[@class='s-item__info clearfix']/a/@href").extract_first()
            yield scrapy.Request(item_url, callback=self.parse_item)
        next_page = response.xpath("//a[@class='pagination__next']/@href").extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)


    ###                                   ###
    #Single auction information collection#  
    ###                                   ###
    def parse_item(self, response):
        title = response.xpath("//h1[@id='itemTitle']/text()").extract_first()

        time_left = response.xpath("//span[@class='vi-tm-left']/span/text()").extract()
        time_left = [n.replace('(','') for n in time_left]
        time_left = [n.replace(')','') for n in time_left]
        time_left = time_left[0]+' '+time_left[1].split(sep=' ')[0] #[6]
        currency = response.xpath("//span[@id='prcIsum_bidPrice']/text()").extract_first().split(sep=' ')[0] #[2]
        number_bids = int(response.xpath("//span[@id='qty-test']/text()").extract_first())
        current_price = response.xpath("//span[@id='prcIsum_bidPrice']/text()").extract_first()
        res = re.search(r'([0-9]*,[0-9]*)', current_price)
        current_price = float(res.groups(0)[0].replace('.','').replace(',','.'))
        
        shipping_cost = response.xpath("//span[@id='fshippingCost']/span/text()").extract_first() #[3]
        try:
            if re.search(r'[0-9]',shipping_cost):
                res = re.search(r'([0-9]*,[0-9]*)', shipping_cost)
                shipping_cost = float(res.groups(0)[0].replace('.','').replace(',','.'))
            else:
                shipping_cost = 0
        except TypeError:
            shipping_cost = 0

        payments = response.xpath("//div[@class='vi-non-us-cclogo']/div/img/@title").extract() #[5]
        item_link = response.request.url

        item = []
        item.extend([title, time_left, current_price, shipping_cost, payments, item_link])

        if sp_fun.validation_item(item, self.time_set, self.max_price):
            message = "<a href=\"{}\">{}</a> \Price: {} {}\Shipping: {} {}\Bids: {}\Expiration: {}\Time left: {:0.1f} minutes".format(item[5], 
            item[0], item[2], currency, item[3], currency, number_bids, item[1], 
            sp_fun.difference_time(datetime.strptime(item[1], '%d %b %Y %H:%M:%S')))
            telegram.send_message_html(message, 'TOKEN')
        

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

file_start = open(script_dir+'/info_start_spider.txt', 'r') #[7]
process = CrawlerProcess(settings={ #[8]
    "DOWNLOAD_DELAY": 2.5,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
})

#arguments_list[0] : url web page
#arguments_list[1] : remaining auction time
#arguments_list[2] : max price

for element in file_start:
    arguments_list = element.rstrip().split(',')
    process.crawl(MySpider, arguments_list[1], arguments_list[2], arguments_list[0])
     
process.start() 
file_start.close()








#- -C O M M E N T S - - S E C T I O N 
#
#   Given the page resulting from the query of a given object on ebay, it selects the links related to each auction and 
#   for each one a function is invoked which extracts the information from the main page of the auction. 
#   The spider sends a telegram notification to the user when an auction reaches an expiration time less than/equal 
#   to the indicated one and does not exceed the price value entered by the user.
# 
#   
#
# 
#
#- -[2] The currency (e.g. EUR) used for the auction is extrapolated. The price is formatted like this:
#           -e.g. 'EUR 100,00' 
# 
#        
#- -[3] The comma is replaced with the point, operation necessary for the conversion from string to float.
#       When the auction uses "local pickup" as shipping, it changes the id that allows the information to be retrieved. 
#       In this case shipping_cost = [] and raises an exception when you apply the search() function. 
#       So, when you raise the exception it means that the object has 'pickup in area' as shipping cost.
#
#
#- -[5] Payment methods can be multiple (paypal, mastercard, etc), so we use the extract() function to get the complete list. 
#       When an empty list is returned, it means that the payment method is only "bank transfer".
#
#
#- -[6] After extrapolating the time zone, delete it from the list and create a single item consisting of date and time
#           - Before: ['02 mar 2021', '17:09:12 CET']
#           - After: '02 mar 2021 17:09:12'
#       
#
#- -[7] .txt file containing auction search information. Each line contains: 
#           1)link_page_results, 
#           2)time remaining in the auction, 
#           3)maximum price.
#       
#   
#- -[8] Delay to avoid exceeding the rate limit of telegram requests per second 
#
#
