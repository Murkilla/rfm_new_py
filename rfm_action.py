import json
import datetime
import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def rfm_do_action(data):
    data_key = {'profile_id','enddate','dayType'}
    check_data = all(elem in data for elem in data_key)
    if(not check_data):
        return msg('error','missingKey')
    
    if( not data or not data['profile_id'] or not data['enddate'] or not data['dayType']):
        return msg('error','fail')
    res = actionPrepare(data,'all')
    res = json.dumps(res)

    return res

def actionPrepare(arr,actionType):
    profile_id = arr['profile_id']
    enddate = parse(arr['enddate'])
    enddate = enddate + relativedelta(months=1)
    enddate = datetime.datetime.strftime(enddate,'%Y-%m-%d')
    dayType = int(arr['dayType'])
    startdate = timeFormat(enddate,dayType,'m')

    data = get_ga_data(arr,startdate,enddate)
    newData = resetData(data,enddate,dayType)
    
    return newData

def get_ga_data(arr,startdate,enddate):

    profile_id = arr['profile_id']
    start = parse(startdate)
    end = parse(enddate)
    
    data = []
    data = pd.DataFrame(data)
    while(start < end):
        print(start)
        index = 1
        while(True):
            try:
                json_data = {
                    "profile_id" : profile_id,
                    "start" : datetime.datetime.strftime(start,'%Y-%m-%d'),
                    "end" : datetime.datetime.strftime(start,'%Y-%m-%d'),
                    "metrics" : ["ga:transactionRevenue"],
                    "dimensions" : ["ga:transactionId,ga:date,ga:userType"],
                    'filters':'',
                    "start_index": index
                }
                headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
                r = requests.post("http://td.turingdigital.com.tw/get_ga_data", data={'query_json' : json.dumps(json_data)})
                index = index + 1000
                res = json.loads(r.text)
                if data.empty:
                    data = pd.DataFrame(res['rows'])
                else:
                    data = data.append(pd.DataFrame(res['rows']))
            except KeyError:
                break
        start = start + relativedelta(days=1)
    data = data.reset_index(drop=True)
    data.columns = ['id','date','userType','price']
    return data

def resetData(data,enddate,dayType):
    if data.empty:
        msg('error','missingData')
    
    day30 = timeFormat(enddate,1,'m')
    day90 = timeFormat(enddate,3,'m')
    day180 = timeFormat(enddate,6,'m')
    day360 = timeFormat(enddate,12,'m')
    dateData = {
        'day30' : day30,
        'day90' : day90,
        'day180' : day180,
        'day360' : day360
    }
    data['price'] = data['price'].astype('float')
    data['price'] = data['price'].astype('int')
    mean = int(data['price'].mean())
    mode = data['price'].mode().max()
    
    if mean > mode:
        maxx = mean
        minn = mode
    else:
        maxx = mode
        minn = mean
    range_data = {
        'maxx' : maxx,
        'minn' : minn,
        'mean' : mean,
        'mode' : mode
    }

    list_data = processData(data,dateData,enddate,range_data,dayType)
    list_data.update({"mode":[str(mode),str(mode),str(mode)],"mean":[str(mean),str(mean),str(mean)]})
    return list_data

def processData(data,dateData,enddate,range_data,dayType):
    
    enddate = datetime.datetime.strftime(parse(enddate),'%Y%m%d')
    if dayType == 1:
        days = 'day30'
    elif dayType == 3:
        days = 'day90'
    elif dayType == 6:
        days = 'day180'
    elif dayType == 12:
        days = 'day360'

    if data.empty:
        msg('error','missingProcessData')
    title = ["x ≤ " + str(range_data['minn']),str(range_data['minn']) + " < x ≤ " + str(range_data['maxx']),str(range_data['maxx']) + " < x"]
    dict_data = {
        "title":title,
        "All":[],
        "New":[],
        "Return":[]
    }
    for i in range(0,3):
        if i == 0:
            userType = ''
        elif i == 1:
            userType = 'New Visitor'
        elif i == 2:
            userType = 'Returning Visitor'
        else:
            userType = ''
        tmpEndDate = enddate
        for k,v in dateData.items():
            tmp = []
            if  userType :
                first = data[(data['date'] >= datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')) & (data['date'] < tmpEndDate) & (data['price'] <= range_data['minn']) & (data['userType'] == userType)]['id'].count()
                second = data[(data['date'] >= datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')) & (data['date'] < tmpEndDate) & (data['price'] > range_data['minn']) & (data['price'] <= range_data['maxx']) & (data['userType'] == userType)]['id'].count()
                third = data[(data['date'] >= datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')) & (data['date'] < tmpEndDate) & (data['price'] > range_data['maxx']) & (data['userType'] == userType)]['id'].count()
                tmp = [str(first),str(second),str(third)]
                if i == 1:
                    dict_data['New'].append({k:tmp})
                else:
                    dict_data['Return'].append({k:tmp})
            else:
                first = data[(data['date'] >= datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')) & (data['date'] < tmpEndDate) & (data['price'] <= range_data['minn'])]['id'].count()
                second = data[(data['date'] >= datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')) & (data['date'] < tmpEndDate) & (data['price'] > range_data['minn']) & (data['price'] <= range_data['maxx'])]['id'].count()
                third = data[(data['date'] >= datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')) & (data['date'] < tmpEndDate) & (data['price'] > range_data['maxx'])]['id'].count()
                tmp = [str(first),str(second),str(third)]
                dict_data['All'].append({k:tmp})
                
            tmpEndDate = datetime.datetime.strftime(parse(dateData[k]),'%Y%m%d')
            if k == days:
                break
    return dict_data

def timeFormat(startdate = datetime.date.today(),gap = 1,actionType = 'm'):
    
    if(type(startdate) != datetime.datetime):
        if(type(startdate) == str):
            startdate = parse(startdate)
    if(actionType == 'm'):
        new = startdate - relativedelta(months=gap)
    else:
        new = startdate + relativedelta(months=gap)

    res = datetime.datetime.strftime(new,'%Y-%m-%d')
    
    return res

def msg(title,content):
    obj = {title:content}
    return json.dumps(obj)
