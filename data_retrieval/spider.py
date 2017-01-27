# -*- coding: utf-8 -*-
import json
import scrapy
import re

class SouqSpider(scrapy.Spider):
    name = "TripAdvisor"  # Name of the Spider, required value
    start_urls = ["https://www.tripadvisor.in/Attractions-g304551-Activities-New_Delhi_National_Capital_Territory_of_Delhi.html"]  # The starting url, Scrapy will request this URL in parse
    # start_urls = ["https://www.tripadvisor.in"]  # The starting url, Scrapy will request this URL in parse

    # Entry point for the spider
    def parse(self, response):
        url_scheme = 'https://www.tripadvisor.in'
        # for href in response.css('.poiTitle::attr(href)'):

        self.base_city = "New Delhi"
        
        for href in response.css('.entry .property_title a::attr(href)'):
            # print "fdbdgkhjgfhjkgbhg-------------------------------######################"
            # print type(href.extract())
            url = url_scheme+href.extract()
            yield scrapy.Request(url, callback=self.parse_item)
            # break

    # Method for parsing a product page
    def parse_item(self, response):
        
        print "heading"
        heading = response.css('#HEADING::text').extract()
        heading = '|'.join(heading)
        heading = heading.replace('\n','')
        heading = heading.replace(',',' ')
        print heading

        print "Rating"
        rating = response.css('.wrap .fr::text').extract()[0:5]
        for x in range(0,len(rating)):
            rating[x] = rating[x].replace(',',' ')
            rating[x] = rating[x].replace('\n','')
        rating = '&'.join(rating)
        print rating

        print "address street"
        street_address = response.css('.format_address .street-address::text').extract()
        if len(street_address) > 0:
            street_address = street_address[0].replace(',',' ')
            street_address = street_address.replace('\n','')
        else:
            street_address = ''
        print street_address

        print "locality"
        address_locality = response.css('.format_address .locality span[property="addressLocality"]::text').extract()
        if len(address_locality) > 0:
            address_locality = address_locality[0].replace(',',' ')
            address_locality = address_locality.replace('\n','')
        else:
            address_locality = ''
        print address_locality

        print "pincode"
        address_pincode = response.css('.format_address .locality span[property="postalCode"]::text').extract()
        if len(address_pincode) > 0:
            address_pincode = address_pincode[0].replace(',',' ')
            address_pincode = address_pincode.replace('\n','')
        else:
            address_pincode = ''
        print address_pincode

        print "country"
        country = response.css('.country-name::text').extract()
        if len(country) > 0:
            country = country[0].replace(',',' ')
            country = country.replace('\n','')
        else:
            country = ''
        print country

        print "details"
        details = response.css('.listing_details p::text').extract()
        if len(country) > 0:
            details = ' '.join(details)
            details = details.replace(',',' ')
            details = details.replace('\n','')
        else:
            details = ''
        print details

        print "ranking"
        ranking = response.css('.heading_ratings .wrap span::text').extract()
        if len(ranking) > 0:
            ranking = ranking[0][1:]
        print ranking

        print "duration"
        duration = response.css('.detail::text').extract()
        # print duration
        if len(duration) > 4:
            duration = duration[4].replace(',',' ')
            duration = duration.replace('\n','')
        else:
            duration = ''
        print duration

        print "open_hours"
        open_hours = []
        days = response.css('.hoursOverlay .days::text').extract()
        hours = response.css('.hoursOverlay .hours::text').extract() 
        print days
        print hours

        print "geolocation"
        # geolocation = response.css('.mapWxH img').extract()
        pattern = re.compile(r"var lazyImgs = \[.*?\]", re.MULTILINE | re.DOTALL)
        coordinate_pattern = re.compile(r'{.*}')
        geolocation = response.xpath("//script[contains(., 'var lazyImgs = [')]/text()").re(pattern)[0]
        # geolocation = geolocation.re(pattern)
        geolocation = coordinate_pattern.search(str(geolocation))
        if geolocation != None:
            print type(geolocation)
            # print geolocation
            geolocation = geolocation.group(0)
            geolocation = json.loads(geolocation)
            # print geolocation['data']
            coordinate_pattern = re.compile(r'center=(.*)&')
            geolocation = coordinate_pattern.search(geolocation['data'])
            if geolocation != None:
                geolocation = geolocation.group(0)
                geolocation = geolocation[7:]
                geolocation = geolocation.split('&')[0]
                # geolocation = geolocation.split(',')[0]
                print geolocation
            else:
                return
        else:
            return

        if len(days) > 0:
            for x in range(0,len(days)):
                temp = days[x]+"|"+hours[x]
                temp = temp.replace(',',' ')
                temp = temp.replace('\n','')
                open_hours.append(temp)
            open_hours = '$'.join(open_hours)
        else:
            open_hours = ''

        print open_hours

        # seller_rating = response.css('.vip-product-info .stats .inline-block small::text'). extract()[0]
        # seller_rating = int(filter(unicode.isdigit,seller_rating))

        # Not all deals are discounted
        # if response.css('.vip-product-info .subhead::text').extract():
        #     original_price = response.css('.price::text').extract()[0].replace("AED", "")
        #     discounted = True
        #     savings = response.css('.noWrap').extract()[0].replace("AED", "")
        yield {
            'rating': rating,
            'ranking': ranking,
            'details': details,
            'geolocation': geolocation,
            'open_hours': open_hours,
            'duration': duration,
            'country': country,
            'address_locality': address_locality,
            'address_street': street_address, 
            'address_pincode': address_pincode,
            'heading': heading,
            'base_city': self.base_city,
            'url': response.url

            # 'Title': response.css('.product-title h1::text').extract()[0],
            # 'Category': response.css('.product-title h1+ span a+ a::text').extract()[0],
            # 'CurrentPrice': response.css('.vip-product-info .price::text').extract()[0].replace(u"\xa0", ""),
            # 'Discounted': discounted,
            # 'Savings': savings,
            # 'SoldBy': response.css('.vip-product-info .stats a::text').extract()[0],
            # 'SellerRating': seller_rating,
        }
