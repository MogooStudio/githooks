# coding=utf-8
import sys
import time
import httplib
import math


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
    if len(sys.argv) < 2:
        raise Exception("参数是必须的")
    return {"message": sys.argv[1], "branch": sys.argv[2]}


if __name__ == '__main__':
    argus = parseArgument()
    commit_message = argus["message"]
    commit_branch = argus["branch"]
    print "*" * 32

    if commit_branch == "master":
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

    print "\n时间校验结束，没有发现问题\n"
    print "*" * 35
    print "\n"
    exit(0)
