from bs4 import BeautifulSoup
from datetime import datetime,date
import httplib2
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import sys
import re
from customSettings import repoDir,djangoDir,djangoSettings

sys.path.insert(0, repoDir)
fileDir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(djangoDir)

from nregaFunctions import stripTableAttributes,htmlWrapperLocal,getjcNumber,getCurrentFinYear
from wrappers.logger import loggerFetch

import django
from django.core.wsgi import get_wsgi_application
from django.core.files.base import ContentFile
from django.db.models import F,Q
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", djangoSettings)
django.setup()

from nrega.models import State,District,Block,Panchayat,Applicant,PanchayatReport

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='This script would parse the worker list from MIS')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-limit', '--limit', help='Limit on the number of results', required=False)

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
  reportType="jobcardRegisterHTML"
  curfinyear=getCurrentFinYear() 
  myPanchayats=Panchayat.objects.filter( Q(jobcardCrawlDate__gt = F('jobcardProcessDate')) | Q(jobcardCrawlDate__isnull=False,jobcardProcessDate__isnull=True)   )[:limit]
  for eachPanchayat in myPanchayats:
    logger.info(eachPanchayat.name+","+eachPanchayat.code)
    panchayatReport=PanchayatReport.objects.filter(reportType=reportType,finyear=curfinyear,panchayat=eachPanchayat).first()
    if panchayatReport is not None:
      logger.info("Panchayat Report Exists")
      myhtml=panchayatReport.reportFile.read()  
      #myhtml=eachPanchayat.jobcardRegisterFile.read()
      htmlsoup=BeautifulSoup(myhtml,"html.parser")
      myTable=htmlsoup.find('table',id="libtechDetails")
      jobcardPrefix=eachPanchayat.block.district.state.stateShortCode+"-"
      logger.info(jobcardPrefix)
      if myTable is not None:
        logger.info("Found the table")
        rows=myTable.findAll('tr')
        for row in rows:
          cols=row.findAll('td')
          if jobcardPrefix not in cols[3].text:
            logger.info("Header Row")
            header=[]
            for i,col in enumerate(cols):
              header.append(col.text.lstrip().rstrip())
            logger.info(str(header))
            villageIndex=header.index("Village Name")
            nameIndex=header.index("Applicant Name")
            headOfHouseholdIndex=header.index("Head of Household")
            fatherHusbandNameIndex=header.index("Father/Husband Name")
            casteIndex=header.index("Caste")
            genderIndex=header.index("Gender")
            ageIndex=header.index("Age")
            jobcardIndex=header.index("Registration No.")
            applicantNoIndex=header.index("Applicant No.")
            bankCodeIndex=header.index("Bank Code")
            bankNameIndex=header.index("Bank Name")
            bankBranchCodeIndex=header.index("Branch Code")
            bankBranchNameIndex=header.index("Branch Name")
            ifscCodeIndex=header.index("IFSC Code")
            micrCodeIndex=header.index("MICR Code")
            poCodeIndex=header.index("Post Office Code")
            poNameIndex=header.index("Post Office Name")
            poAddressIndex=header.index("Post Office Address")
            poAccountNameIndex=header.index("Name As Per Post Office")
            accountFrozenIndex=header.index("Ac Frozen")
            logger.info(villageIndex)
          if jobcardPrefix in cols[3].text:
            for i,col in enumerate(cols):
              cols[i]=col.text.lstrip().rstrip()
            jobcard=cols[jobcardIndex]
            applicantNo=cols[applicantNoIndex]
            jcNo=getjcNumber(jobcard)
            if jcNo.isdigit():
              jcNo=jcNo
            else:
              jcNo=0
            logger.info("Processing Jobcard: %s applicantNo: %s " % (jobcard,applicantNo))
            myApplicant=Applicant.objects.filter(jobcard=jobcard,applicantNo=applicantNo).first()
            if myApplicant is None:
              logger.info("Creating Applicant: %s " % (jobcard))
              Applicant.objects.create(jobcard=jobcard,applicantNo=applicantNo,panchayat=eachPanchayat)
            a=Applicant.objects.filter(jobcard=jobcard,applicantNo=applicantNo).first()
            a.village=cols[villageIndex]
            a.name=cols[nameIndex]
            a.headOfHousehold=cols[headOfHouseholdIndex]
            a.fatherHusbandName=cols[fatherHusbandNameIndex]
            a.caste=cols[casteIndex]
            a.gender=cols[genderIndex]
            a.age=cols[ageIndex]
            a.bankCode=cols[bankCodeIndex]
            a.bankName=cols[bankNameIndex]
            a.bankBranchCode=cols[bankBranchCodeIndex]
            a.bankBranchName=cols[bankBranchNameIndex]
            a.ifscCode=cols[ifscCodeIndex]
            a.micrCode=cols[micrCodeIndex]
            a.poCode=cols[poCodeIndex]
            a.poName=cols[poNameIndex]
            a.poAddress=cols[poAddressIndex]
            a.poAccountName=cols[poAccountNameIndex]
            a.accountFrozen=cols[accountFrozenIndex]
           # [a.village,a.name,a.headOfHousehold,a.fatherHusbandName,a.caste,a.gender,a.age]=[village,name,headOfHousehold,fatherHusbandName,caste,gender,age]
           # [a.bankCode,a.bankName,a.bankBranchCode,a.bankBranchName,a.ifscCode,a.micrCode]=[bankCode,bankName,bankBranchCode,bankBranchName,ifscCode,micrCode]
           # [a.poCode,a.poName,a.poAddress,a.accountNo,a.poAccountName,a.accountFrozen,a.uid]=[poCode,poName,poAddress,accountNo,poAccountName,accountFrozen,uid]
            a.jcNo=jcNo
            a.save() 
    eachPanchayat.jobcardProcessDate=timezone.now()
    eachPanchayat.save()
          
  logger.info("...END PROCESSING") 
  exit(0)
if __name__ == '__main__':
  main()
