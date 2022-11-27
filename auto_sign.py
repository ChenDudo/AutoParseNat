import re
import time
import requests

# Server酱申请的skey
SCKEY = ''

# 钉钉机器人的 webhook
webhook = ''

global contents
contents = ''

# 输出方式
def output(content):
    global contents
    content += '  '
    contents += content + '\n'
    content += '  '
    print(content)

# server酱推送
def server():
    global contents
    message = {"text": "NATAPP + YouDao 通知", "desp": contents}
    r = requests.post("https://sc.ftqq.com/" + SCKEY + ".send", data=message)
    if r.status_code == 200:
        print('[+]server酱已推送，请查收')

# 钉钉消息推送
def dingtalk():
    webhook_url = webhook
    dd_header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    global contents
    dd_message = {
        "msgtype": "text",
        "text": {
            "content": f'有道云笔记签到通知！\n{contents}'
        }
    }
    r = requests.post(url=webhook_url,
                      headers=dd_header,
                      data=json.dumps(dd_message))
    if r.status_code == 200:
        print('[+]钉钉消息已推送，请查收  ')

# 解析log文件，输出content
pattern_list = r'"Url":"[a-zA-Z]+://([a-zA-z0-9]+.[a-zA-Z0-9]+.cc(:)?[0-9]*)"'
url_context = []
def logparser(filepath):
    linenum = 0
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            result = re.compile(pattern_list).search(line)
            if not result:
                linenum = linenum + 1
                continue;
            else:
                if 1:
                    url_context.append("http://" + result.group(1))
                    # print("http://" + result.group(1)+"\n")
                else:
                    content = "http://" + result.group(1)
                    output(content)

# 获取最新两条url链接
def output_Last2_element():
    num = len(url_context)
    output("[Server 1] : "+url_context[-1])
    for i in range(2, num):
        if len(url_context[-i]) != len(url_context[-1]):
            output("[Server 2] : "+url_context[-i])
            return
        else:
            continue

class NeteaseAPI:
    def check_neteast_note(self):
        """ 有道云笔记签到 """
        checkin_url = "http://note.youdao.com/yws/mapi/user?method=checkin"
        headers = {
            "Cookie": " ",
            "User-Agent": "you dao yun bi ji/7.0.6 (iPhone; iOS 14.3; Scale/2.00)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
        }
        response = requests.post(url=checkin_url, headers=headers, verify=False)

        if response.status_code != 200:
            # send_wechat("有道云笔记签到失败，原因：{}".format(response.json()))
            output('Task Failed!')
            print("有道云笔记签到失败，原因：{}".format(response.json()))
            # sys.exit(1)

        # 格式化
        info = response.json()
        # 一共签到获得
        total = info['total'] / 1048576
        # 本次签到获得空间
        space = info['space'] / 1048576
        # 当前时间
        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info['time'] / 1000))
        msg = """Task Success! First sign time: {}""".format(times)
        output(msg)
        msg = """Today: {} MB, Total : {} MB""".format(space, total)
        output(msg)

if __name__ == '__main__':
    # STEP 1: NATAPP 获取
    output('【1】 NATAPP Get URL Info')
    logparser("./nohup.out")
    output_Last2_element()
    output('--- --- --- --- --- ---')

    # STEP2: YouDao Note
    output('【2】 YouDaoNote Sign Info')
    signNew = NeteaseAPI()
    signNew.check_neteast_note()

    try:
        server()
    except Exception:
        print('[+]请检查server酱配置是否正确')

def main_handler(event, context):
    return main()
