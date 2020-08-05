# [AllUrl]
# detials = http://m.weather.com.cn/data/{city_code}.html
# 实时天气 = http://d1.weather.com.cn/sk_2d/{city_code}.html?_=1571537621000
# 逐小时天气 = http://www.weather.com.cn/weather1dn/{city_code}.shtml
# 近7天天气 = http://www.weather.com.cn/weathern/{city_code}.shtml
# 7至15天天气 = http://www.weather.com.cn/weather15dn/{city_code}.shtml
# 雷达图列表 = http://d1.weather.com.cn/radar_channel/radar/json/radar_list.json?callback=readRadarList&_={time_stamp}
# 雷达图下载 = http://d1.weather.com.cn/radar_channel/radar/pic/{file_name}
# 降水图列表 = http://d1.weather.com.cn/radar_channel/prec1h/rainList.json?callback=getPreObs1h&_={time_stamp}
# 降水图下载 = http://d1.weather.com.cn/radar_channel/prec1h/{file_name}
# 云图列表 = http://d1.weather.com.cn/satellite2015/JC_YT_DL_WXZXCSYT_4A.html?jsoncallback=readSatellite&callback=jQuery18204042381380404867_{time_stamp}&_={time_stamp}
# 云图下载 = http://pi.weather.com.cn/i/product/pic/m/{file_name}
# 雷电位置 = http://d1.weather.com.cn/radar_channel/prec1h/rainList.json?callback=getPreObs1h&_={time_stamp}

# [WindDirectionCode]
# 0 = 无持续风向
# 1 = 东北风
# 2 = 东风
# 3 = 东南风
# 4 = 南风
# 5 = 西南风
# 6 = 西风
# 7 = 西北风
# 8 = 北风

wind_direction_code = {
    '0': '无持续风向',
    '1': '东北风',
    '2': '东风',
    '3': '东南风',
    '4': '南风',
    '5': '西南风',
    '6': '西风',
    '7': '西北风',
    '8': '北风',
}

# [WindSpeedCode]
# 0 = <3级
# 1 = 3~4级
# 2 = 4~5级
# 3 = 5~6级
# 4 = 6~7级


wind_speed_code = {
    '0': '<3级',
    '1': '3~4级',
    '2': '4~5级',
    '3': '5~6级',
    '4': '6~7级',
}

# [WeatherCode]
# 00 = 晴
# 01 = 多云
# 02 = 阴
# 03 = 阵雨
# 04 = 雷阵雨
# 05 = 雷阵雨伴有冰雹
# 06 = 雨夹雪
# 07 = 小雨
# 08 = 中雨
# 09 = 大雨
# 10 = 暴雨
# 11 = 大暴雨
# 12 = 特大暴雨
# 13 = 阵雪
# 14 = 小雪
# 15 = 中雪
# 16 = 大雪
# 17 = 暴雪
# 18 = 雾
# 19 = 冻雨
# 20 = 沙尘暴
# 21 = 小雨-中雨
# 22 = 中雨-大雨
# 23 = 大雨-暴雨
# 24 = 暴雨-大暴雨
# 25 = 大暴雨-特大暴雨
# 26 = 小雪-中雪
# 27 = 中雪-大雪
# 28 = 大雪-暴雪
# 29 = 浮尘
# 30 = 扬沙
# 31 = 强沙尘暴
# 32 = 霾

weather_code = {
    '00': '晴',
    '01': '多云',
    '02': '阴',
    '03': '阵雨',
    '04': '雷阵雨',
    '05': '雷阵雨伴有冰雹',
    '06': '雨夹雪',
    '07': '小雨',
    '08': '中雨',
    '09': '大雨',
    '10': '暴雨',
    '11': '大暴雨',
    '12': '特大暴雨',
    '13': '阵雪',
    '14': '小雪',
    '15': '中雪',
    '16': '大雪',
    '17': '暴雪',
    '18': '雾',
    '20': '沙尘暴',
    '21': '小雨-中雨',
    '22': '中雨-大雨',
    '23': '大雨-暴雨',
    '24': '暴雨-大暴雨',
    '25': '大暴雨-特大暴雨',
    '26': '小雪-中雪',
    '27': '中雪-大雪',
    '28': '大雪-暴雪',
    '29': '浮尘',
    '30': '扬沙',
    '31': '强沙尘暴',
    '32': '霾',
}

code_dict = {
    'ja': '天气',
    'jd': '风向',
    'jb': '温度',
    'jf': '日期',
    'jc': '风速',
    'je': '湿度',
}