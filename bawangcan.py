import requests
import json
import re
import io
import xlwt
import datetime
import configparser
import os
from tqdm import tqdm

#从config.ini中读取dper和cityId
cf = configparser.ConfigParser()
path = os.path.abspath('config.ini')
cf.read(path)
dper = cf.get('basic', 'dper')
cityId = cf.get('basic','cityId')

# 创建一个workbook
workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('霸王餐')
row0 = ["序号","霸王餐名称","报名状态","报名地址","异常原因"]
for i in range(0,len(row0)):
    worksheet.write(0,i,row0[i])

orgin_url = 'http://s.dianping.com/event/'

#获取霸王餐列表
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://s.dianping.com/event/beijing',
    'Origin': 'http://s.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Content-Type': 'application/json',
}


ids = []
activityTitles = []
types_food = [1, 2, 6, 99]
types_all = [0]
data = {"cityId":cityId,"type":0,"mode":"","page":1}
for t in types_food:
  for page in range(1,15):
      data["page"] = str(page)
      data["type"] = str(t)
      response = requests.post('http://m.dianping.com/activity/static/pc/ajaxList', headers=headers, data=str(json.dumps(data)))
      # print(page)
      for item in response.json()['data']['detail']:
          activityTitles.append(item['activityTitle'])
          ids.append(item['offlineActivityId'])
          # print(str(page) + ":" + item['activityTitle'])

print('搜索到'+str(len(ids))+'条霸王餐')
cookies = {
    'dper':dper
}

#报名霸王餐
headers = {
    'Origin': 'http://s.dianping.com',
    'Accept-Encoding': 'gzip, deflate',
    'X-Request': 'JSON',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'application/json, text/javascript',
    'Referer': 'http://s.dianping.com/event/1063463422',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = {
  'offlineActivityId': '1063463422',
  'phoneNo': '180****3715',
  'shippingAddress': '',
  'extraCount': '',
  'birthdayStr': '',
  'email': '',
  'marryDayStr': '',
  'babyBirths': '',
  'pregnant': '',
  'marryStatus': '0',
  'comboId': '1',
  'branchId': '568675',
  'usePassCard': '0',
  'passCardNo': '',
  'isShareSina': 'false',
  'isShareQQ': 'false'
}
def set_color(color,bold):
    style=xlwt.XFStyle()
    font=xlwt.Font()
    font.colour_index=color
    font.bold = bold
    style.font=font
    return style

success = []
successed = []
fail = []
count = 1
for _id in tqdm(ids):
    text = requests.get(orgin_url+str(_id),headers=headers,cookies=cookies).text
    shopid = re.search(r'shopid:[0-9]*',text).group()
    shopid = shopid.split('shopid:')[1]
    data['offlineActivityId'] = str(_id)
    data['branchId'] = shopid
    response = requests.post('http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo', headers=headers,cookies=cookies, data=data)

    msg = json.loads(response.text)

    if "不要重复报名" in msg["msg"]:
        successed.append(activityTitles[ids.index(_id)])
        worksheet.write(count,0,count)
        worksheet.write(count,1,activityTitles[ids.index(_id)])
        worksheet.write(count,2,"已报名过")
        worksheet.write(count,3,"http://s.dianping.com/event/"+str(_id))
    elif "报名成功" in msg["msg"]["html"]:
        success.append(activityTitles[ids.index(_id)])
        worksheet.write(count,0,count)
        worksheet.write(count,1,activityTitles[ids.index(_id)])
        worksheet.write(count,2,"报名成功")
        worksheet.write(count,3,"http://s.dianping.com/event/"+str(_id))
    else :
        print(msg)
        fail.append(activityTitles[ids.index(_id)])
        worksheet.write(count,0,count)
        worksheet.write(count,1,activityTitles[ids.index(_id)])
        worksheet.write(count,2,"报名异常",set_color(0x02,True))
        worksheet.write(count,3,"http://s.dianping.com/event/"+str(_id))
        worksheet.write(count,4,msg["msg"]["html"])
    count=count+1
worksheet.write(0,5,'成功登记'+str(len(success))+'个活动')
worksheet.write(1,5,'已经登记过'+str(len(successed))+'个活动')
worksheet.write(2,5,'登记异常'+str(len(fail))+'个活动')
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H`%M`%S')#现在
workbook.save('霸王餐'+nowTime+'.xls')

print('成功登记'+str(len(success))+'个活动')
# for i in success:
#     print(i)

print('已经登记过'+str(len(successed))+'个活动')
# for i in successed:
#     print(i)

print('登记异常'+str(len(fail))+'个活动')
# for i in fail:
#     print(i)
