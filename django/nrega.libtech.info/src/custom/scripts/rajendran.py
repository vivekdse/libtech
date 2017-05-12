from bs4 import BeautifulSoup
from datetime import datetime,date
import requests
import os
import sys
import re
import time
from customSettings import repoDir,djangoDir,djangoSettings

sys.path.insert(0, repoDir)
fileDir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(djangoDir)

from nregaFunctions import stripTableAttributes,htmlWrapperLocal,getFullFinYear,savePanchayatReport
from wrappers.logger import loggerFetch

import django
from django.core.wsgi import get_wsgi_application
from django.core.files.base import ContentFile
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", djangoSettings)
django.setup()

from nrega.models import State,District,Block,Panchayat,Muster,WorkDetail,PanchayatReport

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='These scripts will initialize the Database for the district and populate relevant details')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-limit', '--limit', help='Limit on the number of results', required=False)
  parser.add_argument('-f', '--finyear', help='Financial year for which data needs to be crawld', required=True)
  parser.add_argument('-s', '--stateCode', help='StateCode for which the numbster needs to be downloaded', required=False)

  args = vars(parser.parse_args())
  return args


def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))
  if args['limit']:
    limit = int(args['limit'])
  else:
    limit =1
  finyear=args['finyear']
  stateCodes=['33','34','27','24','15','18','16','31','05','17']
  stateCodes=['34']
  for stateCode in stateCodes:
    myPanchayats=Panchayat.objects.filter(crawlRequirement='FULL',block__district__state__code=stateCode)
 
    for eachPanchayat in myPanchayats:
      logger.info("**********************************************************************************")
      logger.info("Createing work Payment report for panchayat: %s panchayatCode: %s ID: %s" % (eachPanchayat.name,eachPanchayat.code,str(eachPanchayat.id)))
      PanchayatReports=PanchayatReport.objects.filter(panchayat=eachPanchayat)
      for report in PanchayatReports:
        reportType=report.reportType
        reportURL=report.reportFile.url
        logger.info("Panchyat Name: %s, reportType: %s, reportURL : %s " % (eachPanchayat.name,reportType,reportURL)) 
        filepath="/tmp/rajendran/%s/" % (eachPanchayat.block.district.state.name)
        cmd="mkdir -p %s && cd %s && wget  %s " %(filepath,filepath,reportURL) 
        logger.info(cmd)
        os.system(cmd)
  logger.info("...END PROCESSING") 
  exit(0)
if __name__ == '__main__':
  main()