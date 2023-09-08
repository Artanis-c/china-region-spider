import requests
from lxml import etree
import time
from queue import Queue
from threading import Thread


def getHtml(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    response = requests.get(url, headers=headers)
    response.encoding = 'UTF-8'
    data = response.text
    return data


def getProvince(url, file):
    provinceData = []
    provinceHtml = getHtml(url)
    selector = etree.HTML(provinceHtml)
    provinceList = selector.xpath('//tr[@class="provincetr"]')
    for pro in provinceList:
        provinceNameArr = pro.xpath('td/a/text()')
        provinceLinkArr = pro.xpath('td/a/@href')
        for i in range(len(provinceLinkArr)):
            provinceUrl = url[:-10] + provinceLinkArr[i]
            provinceData.append({'name': provinceNameArr[i], 'link': provinceUrl})
            file.write(provinceNameArr[i] + "\r")
            getCity(provinceUrl, file)


def getCity(proLink, file):
    cityData = []
    cityHtml = getHtml(proLink)
    selector = etree.HTML(cityHtml)
    cityList = selector.xpath('//tr[@class="citytr"]')
    for i in cityList:
        cityCode = i.xpath('td[1]/a/text()')
        cityLink = i.xpath('td[1]/a/@href')
        cityName = i.xpath('td[2]/a/text()')
        for j in range(len(cityLink)):
            cityURL = proLink[:-7] + cityLink[j]
            cityData.append({'name': cityName[j], 'code': cityCode[j], 'link': cityURL})
            file.write(cityName[j] + '/' + cityCode[j] + "\r")
            getCounty(cityURL, file)


def getCounty(cityUrl, file):
    data = getHtml(cityUrl)
    selector = etree.HTML(data)
    countyList = selector.xpath('//tr[@class="countytr"]')
    # 下面是爬取每个区的代码、URL
    for i in countyList:
        countyCode = i.xpath('td[1]/a/text()')
        countyLink = i.xpath('td[1]/a/@href')
        countyName = i.xpath('td[2]/a/text()')
        # 上面得到的是列表形式的，下面将其每一个用字典存储
        for j in range(len(countyLink)):
            countyURL = cityUrl[:-9] + countyLink[j]
            file.write(countyName[j] + '/' + countyCode[j] + "\r")
            getTown(countyURL, file)


def getTown(countyUrl, file):
    data = getHtml(countyUrl)
    selector = etree.HTML(data)
    townList = selector.xpath('//tr[@class="towntr"]')
    # 下面是爬取每个区的代码、URL
    for i in townList:
        townCode = i.xpath('td[1]/a/text()')
        townLink = i.xpath('td[1]/a/@href')
        townName = i.xpath('td[2]/a/text()')
        for j in range(len(townLink)):
            file.write(townName[j] + '/' + townCode[j] + "\r")


if __name__ == '__main__':
    f = open('data.txt', 'w')
    prData = getProvince('http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/index.html', f)
    f.close()
