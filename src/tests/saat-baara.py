from bs4 import BeautifulSoup

import time
import csv
import json
import ast

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch
from wrappers.sn import driverInitialize,driverFinalize,displayInitialize,displayFinalize

from selenium.webdriver.support.ui import Select

#######################
# Global Declarations
#######################

timeout = 10

url = "https://mahabhulekh.maharashtra.gov.in/"
filename = 'z.html'

dc = "32"
did = "32"
dn = "रत्नागिरी"
surveyno = "21"
gat = "100"
sno = gat + "/" + surveyno
tc = "3"
tid = "3"
tn = "खेड"
vid = "273200030399810000"
vn = "वावे तर्फे खेड"

cmd = '''curl 'https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx/getSnos' -X POST -H 'Accept: application/json, text/plain, */*' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Content-Length: 60' -H 'Content-Type: application/json;charset=utf-8' -H 'Cookie: ASP.NET_SessionId=xgahrcwef0hoicteddbwrxxo' -H 'Host: mahabhulekh.maharashtra.gov.in' -H 'Referer: https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' -d "{'ptxt':'%s','vid':'273200030399810000','did':'32','tid':'3'}" -o %s.json ''' % (gat, gat)

gat_list = [ 1, 2, 3, 4, 5, 6, 7, 13, 21, 23, 25, 26, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 72, 86, 91, 92, 93, 94, 95, 96, 97, 98, 105, 128, 129, 143, 149, 150, 151, 152, 153, 154, 155, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 175, 176, 177, 178, 179, 180, 182, 186, 188, 191, 192, 193, 194, 196, 197, 198, ]

#############
# Functions
#############

def runTestSuite():
  logger = loggerFetch("info")
  logger.info("BEGIN PROCESSING...")
  
  display = displayInitialize(0)
  driver = driverInitialize()

  '''
  content = csv.reader(open('./gats.csv', 'r'), delimiter=',', quotechar='"')
  for (gat, d) in content:
  '''
  
  for gat in gat_list:
    json_file = './json/%s.json' % gat

    if gat >= 179 or not os.path.exists(json_file):
#      cmd = '''curl -s 'https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx/getSnos' -X POST -H 'Accept: application/json, text/plain, */*' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Content-Length: 60' -H 'Content-Type: application/json;charset=utf-8' -H 'Cookie: ASP.NET_SessionId=iiu3ekqoppg0tbdmoq0pwovv' -H 'Host: mahabhulekh.maharashtra.gov.in' -H 'Referer: https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' -d "{'ptxt':'%s','vid':'273200030399810000','did':'32','tid':'3'}" -o %s ''' % (gat, json_file)
      cmd = '''curl -s 'https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx/getSnos' -X POST -H 'Host: mahabhulekh.maharashtra.gov.in' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json;charset=utf-8' -H 'Referer: https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx' -H 'Content-Length: 62' -H 'Cookie: ASP.NET_SessionId=iiu3ekqoppg0tbdmoq0pwovv' -H 'Connection: keep-alive' -d "{'ptxt':'%s','vid':'273200030399810000','did':'32','tid':'3'}" -o %s ''' % (gat, json_file)
      
      logger.info('Executing [%s]' % cmd)
      os.system(cmd)

    with open(json_file, 'r') as json_hdl:
      d = json_hdl.read()

    logger.info('Obtained json for gat[%s] is [%s]' % (gat, d))

    logger.info("Fetching...[%s]" % url)
    driver.get(url)

    try:
      driver.find_element_by_xpath("//form[@id='aspnetForm']/div[3]/div/div/div[3]/a[3]/p").click()
    except:
      logger.error('Cant find element for [%s]' % gat)
      continue
      
    Select(driver.find_element_by_id("distSelect")).select_by_visible_text(dn)
    Select(driver.find_element_by_id("talSelect")).select_by_visible_text(tn)
    Select(driver.find_element_by_id("vilSelect")).select_by_visible_text(vn)
    driver.find_element_by_css_selector("option[value=\"string:273200030399810000\"]").click()
    driver.find_element_by_id("rbsryno").click()
    driver.find_element_by_xpath("//input[@type='number']").clear()
    driver.find_element_by_xpath("//input[@type='number']").send_keys(gat)
    driver.find_element_by_css_selector("input[type=\"button\"]").click()
    sno_dict = ast.literal_eval(d)
    sno_list = sno_dict["d"]
    logger.info("Gat[%s], Details[%s]" % (gat, sno_list)) # .get("d")))

    data = json.loads(sno_list)
    logger.debug(data)

    time.sleep(5)
    for sno_dict in data:
      logger.debug(sno_dict)
      logger.info("sno[%s], snov[%s]" % (sno_dict["sno"], sno_dict["snov"]))
      sno = sno_dict["sno"]
      filename = '/home/mayank/wd/SaatBaara/7-12-mahabhulekh/%s.html' % sno.replace('/','_')
      if os.path.exists(filename):
        #time.sleep(1)
        continue
      Select(driver.find_element_by_xpath("//form[@id='aspnetForm']/div[3]/div/div/div[3]/div/div[3]/table/tbody/tr[3]/td/select")).select_by_visible_text(sno)
      #logger.info(driver.find_element_by_link_text(sno))
      driver.find_element_by_css_selector("td.last-rows > input[type=\"button\"]").click()
      time.sleep(1)
      
      parent_handle = driver.current_window_handle
      logger.info("Handles : %s Number : %s" % (driver.window_handles, len(driver.window_handles)))

      if len(driver.window_handles) == 2:
        driver.switch_to_window(driver.window_handles[-1])
      else:
        logger.error("Handlers gone wrong [" + str(driver.window_handles) + "]")
        driver.save_screenshot('z.png')

      html_source = driver.page_source.replace('<head>',
                                               '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>').encode('utf-8')

      logger.debug("HTML Fetched [%s]" % html_source)
      if(driver.title != '७/१२'):
        logger.error(driver.title)
        continue
        
      bs = BeautifulSoup(html_source, "html.parser")
      body = bs.find('tbody')
      try:
        body = body.findNext('tbody')
      except:
        logger.error('Empty body for [%s]' % sno)
        continue
      body = body.findNext('tbody')
      logger.info(body)
      td = body.find('td')
      td = td.findAll('td')

      logger.info("Checking [%s]" % td[2].text)
      if(sno != td[2].text):
        continue

      with open(filename, 'wb') as html_file:
        logger.info('Writing [%s]' % filename)
        html_file.write(html_source)
    
      driver.close()
      driver.switch_to_window(parent_handle)
      time.sleep(1)
    time.sleep(1)

  driverFinalize(driver)
  displayFinalize(display)


  logger.info("...END PROCESSING")     


def main():
  runTestSuite()
  exit(0)

if __name__ == '__main__':
  main()
