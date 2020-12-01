# coding = utf-8
# encoding:utf-8

import sys
import re

# 设置编码格式
reload(sys)
sys.setdefaultencoding('utf8')

# 正则表达式
regular_list = ['^\\[机能追加\\] *\\[.+\\] *.+', '^【机能追加】 *【.+】 *.+',
                '^\\[BUG修正\\] *\\[.+\\] *.+', '^【BUG修正】 *【.+】 *.+',
                '^\\[样式变更\\] *\\[.+\\] *.+', '^【样式追加】 *【.+】 *.+',
                '^\\[重构\\] *\\[.+\\] *.+', '^【重构】 *【.+】 *.+']

# 解析shell脚本传过来的参数
def parseArgument():
    if len(sys.argv) < 2:
        print('shell脚本没有传参数\n')
        raise Exception("参数是必须的!")

    # init
    argus = {}
    argus["message"] = u""

    # set
    argv_msg = u''
    for tempstr in sys.argv[1:]:
        argv_msg += tempstr

    argus["message"] = argv_msg

    return argus



def reg_message(message, restr):
    temp = message.decode('utf8')
    pat = restr.decode('utf8')
    pattern = re.compile(pat, flags=re.IGNORECASE)
    results = pattern.findall(temp)
    return len(results)

if __name__ == "__main__":
    argus = parseArgument()
    push_message = argus['message']
    print('\n\n执行提交信息校验 \n')
    print('\n提交信息：{0}\n'.format(push_message))

    reg_result = False

    for reg in regular_list:
        if reg_message(push_message, reg) > 0:
            reg_result = True

    if reg_result:
    
        exit(0)
    else:
        print('*' * 50)
        print('  ❌❌❌ 提交信息格式不正确 禁止提交代码 ❌❌❌   ')
        print('*' * 50)
        print('\n')
        
        print('------------------------------------')
        print('     请参考以下格式 重新提交: \n')
        print('[功能追加][通用]加入英文语言支持 \n')
        print('[BUG修正][XF01]解决车机定制需求引起的XX bug \n')
        print('[样式变更][XF03]新增定制需求，加入广播 \n')
        print('[重构] [通用]增加xx类代码注释 \n')
        print('------------------------------------')

        exit(1)
