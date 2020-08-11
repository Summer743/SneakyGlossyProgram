import requests
from bs4 import BeautifulSoup
import json
import re


#https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019017
crtfc_key='8896736e78cfd879d8476af7704d914b8fffd5f5'
corp_code1='00523307'
corp_code2='00334624'
bsns_year='2019'
reprt_code='11014'

# step 1 : 해당년도의 사업보고서 검색
req=requests.get('https://opendart.fss.or.kr/api/fnlttMultiAcnt.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code1+','+corp_code2+'&bsns_year='+bsns_year+'&reprt_code='+reprt_code)

html=req.text
code=json.loads(html)
url='https://dart.fss.or.kr/dsaf001/main.do?rcpNo='+code['list'][0]['rcept_no']
print('사업보고서 url= '+url)


#  step 2 : 사업보고서를 크롤링
req2=requests.get(url)
html2=req2.text
soup2=BeautifulSoup(html2, 'html.parser')
#제무제표 페이지 찾기
body=str(soup2.find('head'))
a=re.search(' 재무제표', body).span()
# 요약재무정보 근처에서 숫자 정보 찾기(자바스크립트로 되어있지만 정규표현식으로 검색)
b=re.search(r'viewDoc(.*);',body[a[0]:a[1]+1000]).group()
#필요없는 부분 제거
list=b[8:-2].split(', ')
list=[i[1:-1] for i in list]
url_final='http://dart.fss.or.kr/report/viewer.do?rcpNo='+list[0]+'&dcmNo='+list[1]+'&eleId='+list[2]+'&offset='+list[3]+'&length='+list[4]+'&dtd=dart3.xsd'
print('재무제표 url = '+url_final)


# step 3 : 사업보고서의 재무제표 페이지까지 진입 후, 테이블 크롤링. 이 곳부터 자신의 방식에 맞게 Pandas나 csv를 사용하세요. 저는 그냥 텍스트 탭(\t) 크롤링.

req3=requests.get(url_final)
html3=req3.text
print(req3.text)
#판다스 이용해서 테이블 얻어내기
#import pandas as pd
#import lxml
#df = pd.read_html(html3)

#import openpyxl
#df[1].to_excel('data.xlsx')