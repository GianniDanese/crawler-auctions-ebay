# scrapy-crawler-auctions-ebay
A simple scrapy crawler to scrape sebay auctions created using scrapy and telegram api.

Given the page resulting from the query of a given object on ebay, it selects the links related to each auction and for each one a function is invoked which 
extracts the information from the main page of the auction. The spider sends a telegram notification to the user when an auction reaches an expiration time less 
than/equal to the indicated one and does not exceed the price value entered by the user.

A .txt file (info_start_spider) is used to retrieve the information needed for the spider to work, such as:
  - url auction results page;
  - maximum time remaining at the end of the auction within which to warn the user;
  - maximum price of interest for the object on sale.

The info_start_spider file already contains some test information.
