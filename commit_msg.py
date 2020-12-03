# coding=utf-8
import sys
import time
import httplib
import math
import re

regular_list = ['\\[new\\](.*)', '\\[fix\\](.*)',
                '\\[update\\](.*)', 'server(.*)',
                'Merge(.*)', 'Revert(.*)']


def getServerTime():
    try:
        conn = httplib.HTTPConnection('time1909.beijing-time.org')
        conn.request('GET', '/time.asp', '', {'User-Agent': 'Mozilla/5.0'})
        response = conn.getresponse()
        if response.status == 200:
            result = response.read()
            data = result.split(';')
            year = data[1][len("nyear") + 3: len(data[1])]
            month = '{0:02d}'.format(int(data[2][len("nmonth") + 3: len(data[2])]))
            day = '{0:02d}'.format(int(data[3][len("nday") + 3: len(data[3])]))
            hrs = '{0:02d}'.format(int(data[5][len("nhrs") + 3: len(data[5])]))
            minute = '{0:02d}'.format(int(data[6][len("nmin") + 3: len(data[6])]))
            sec = '{0:02d}'.format(int(data[7][len("nsec") + 3: len(data[7])]))
            timeStr = "%s-%s-%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
            return timeStr
    except:
        return -1


def parseArgument():
    if len(sys.argv) < 3:
        raise Exception("参数错误：长度小于3")
    return {"message": sys.argv[1], "branch": sys.argv[2]}


if __name__ == '__main__':
    argus = parseArgument()
    commit_message = argus["message"]
    commit_branch = argus["branch"]
    print "*" * 32

    if commit_branch == "master":

        # 检查提交格式
        flag_format = False
        for reg in regular_list:
            if re.match(reg, commit_message):
                flag_format = True
                break
        if not flag_format:
            print "\nxxx 提交信息格式不正确，请核查后重新提交 xxx"
            print('\n请参考以下格式重新提交:')
            print('[new]加入xx功能')
            print('[update]修改xx逻辑')
            print('[fix]解决xx功能bug\n')
            print "*" * 32
            print "\n"
            exit(1)

        # 检查提交时间
        serverTime = getServerTime()
        if serverTime == -1:
            print "*" * 32
            print "xxx 无法获取网络时间，请检查是否联网后重新提交 xxx"
            print "*" * 32
            exit(1)

        serverTimeArray = time.strptime(serverTime, "%Y-%m-%d %H:%M:%S")
        serverTimeStamp = int(time.mktime(serverTimeArray))

        times = time.localtime()
        clientTime = time.strftime("%Y-%m-%d %H:%M:%S", times)
        clientTimeStamp = int(time.mktime(times))

        diff = serverTimeStamp - clientTimeStamp
        if math.fabs(diff) > 3600:
            print "\nxxx 提交时间有误，请校对后重新提交 xxx"
            print "网络时间: {0} ".format(serverTime)
            print "提交时间: {0} \n".format(clientTime)
            print "*" * 32
            print "\n"
            exit(1)

    print "\n提交检查结束，没有发现问题，你是最棒的！\n"
    print "*" * 35
    print "\n"
    exit(0)
