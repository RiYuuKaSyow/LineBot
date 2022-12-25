from django.db import models
import json
import requests
import datetime

# Create your models here.
class Reply:
    def __init__(self,cmd='', auth='',location='',duration='3'):
        self.exist = True
        if cmd == '天氣':
            self.process = Weather(auth,location,duration)
        elif cmd == '訂閱天氣':
            self.process = Weather(location)
        elif cmd == '更改地區':
            self.process = Weather(location)
        elif cmd == '取消訂閱':
            self.process = Weather(location)
        elif cmd == '發票':
            self.process = Weather(location)
        elif cmd == '指令':
            self.process = Weather(location)
        elif cmd == '地區':
            self.process = Weather(location)
        else:
            self.exist = False
    def reply(self,event,api):
        api.reply_message(
            reply_token = event.replyToken,
            messages = self.process.msg()
        )
        return

class Weather:

    all_location = ['宜蘭縣', '花蓮縣', '臺東縣', '臺北市', '新北市', '桃園市', '臺中市', 
    '臺南市', '高雄市', '基隆市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣',
    '嘉義市', '屏東縣', '澎湖縣', '金門縣', '連江縣']

    def __init__(self, auth='',location='宜蘭縣',duration=3):
        self.elements = 'MaxAT,MinAT,PoP12h,UVI,WeatherDescription,T' ;
        self.location = location
        self.duration = 7 if duration > 7 else duration
        self.auth = auth
        self.info = self._getinf()
        self._dealInfo()
    def msg(self):
        res = {
            'type' : 'flex',
            'altText' : '後' + self.duration + '天的' + self.location + '天氣預報',
            'contents' : [
                {
                    'type' : 'carousel',
                    'contents' : self._result()
                }
            ]
        }
        return json.dumps(res)
    def _getinf(self):
        tz = datetime.timezone( datetime.timedelta(hours=+8) )
        now = datetime.datetime.now(tz)
        duration =  datetime.timedelta( days=7 )
        timeto = now + duration
        tf = now.strftime('%Y-%m-%d%Z%H:%M:%S')
        tt = timeto.strftime('%Y-%m-%d%Z%H:%M:%S')
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?'
        url = url + 'Authorization=' + self.auth
        url = url + '&locationName=' + self.location
        url = url + '&elementName=' + self.elements
        url = url + '&timeFrom=' + tf
        url = url + '&timeTo=' + tt
        res = requests.get(url).json()
        return res['records']['locations'][0]['location'][0]['weatherElement']
    def _dealInfo(self):
        self.PoP12h = []
        self.T = []
        self.MaxAT = []
        self.WeatherDescription = []
        self.MinAT = []
        self.startTime = []
        self.endTime = []
        self.UVI = []
        for i in range(0,14):
            self.PoP12h.append( self.info[0]['time'][i]['elementValue'][0]['value'] + '%' )
            self.T.append( self.info[1]['time'][i]['elementValue'][0]['value'] + '℃' )
            self.MaxAT.append( self.info[2]['time'][i]['elementValue'][0]['value'] + '℃' )
            self.WeatherDescription.append( self.info[4]['time'][i]['elementValue'][0]['value'].split('。')[0] )
            self.MinAT.append( self.info[5]['time'][i]['elementValue'][0]['value'] + '℃' )
            self.startTime.append( self.info[0]['time'][i]['startTime'] )
            self.endTime.append( self.info[0]['time'][i]['endTime'] )
            if i < len( self.info[3]['time'] ):
                self.UVI.append( self.info[3]['time'][i]['elementValue'][0]['value'] )
            else:
                self.UVI.append( '' )
        return
    def _result(self):
        res = []
        for i in range(0,self.duration):
            temp = {
                'type' : 'bubble',
                'body' : {
                    'type' : 'box',
                    'layout' : 'vertical',
                    'contents' : [
                        {
                            'type' : 'box',
                            'layout' : 'vertical',
                            'contents' : {
                                {
                                    'type' : 'text',
                                    'text' : '從' + self.startTime[i*2]
                                },
                                {
                                    'type' : 'text',
                                    'text' : '到' + self.endTime[i*2]
                                },
                                {
                                    'type' : 'text',
                                    'text' : self.WeatherDescription[i*2]
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '降雨機率' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.PoP12h[i*2]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '平均溫度' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.T[i*2]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '最高體感溫度' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.MaxAT[i*2]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '最低體感溫度' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.MinAT[i*2]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '紫外線指數' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.UVI[i*2]
                                        }
                                    }
                                }
                            },
                        },
                        {
                            'type' : 'separator',
                            'margin' : 'xl',
                            'color' : '#000000'
                        },
                        {
                            'type' : 'box',
                            'layout' : 'vertical',
                            'contents' : {
                                {
                                    'type' : 'text',
                                    'text' : '從' + self.startTime[i*2+1]
                                },
                                {
                                    'type' : 'text',
                                    'text' : '到' + self.endTime[i*2+1]
                                },
                                {
                                    'type' : 'text',
                                    'text' : self.WeatherDescription[i*2+1]
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '降雨機率' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.PoP12h[i*2+1]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '平均溫度' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.T[i*2+1]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '最高體感溫度' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.MaxAT[i*2+1]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '最低體感溫度' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.MinAT[i*2+1]
                                        }
                                    }
                                },
                                {
                                    'type' : 'box',
                                    'layout' : 'horizontal',
                                    'contents' : {
                                        {
                                            'type' : 'text',
                                            'text' : '紫外線指數' 
                                        },
                                        {
                                            'type' : 'text',
                                            'text' : self.UVI[i*2+1]
                                        }
                                    }
                                }
                            },
                        }
                    ]
                }    
            }
            res.append(temp)
        return res


class Receipt:
    def __init__(self):
        return
    def msg(self):
        return
class Subscribe:
    def __init__(self,location='宜蘭縣',duration=3):
        return
    def msg(self):
        return