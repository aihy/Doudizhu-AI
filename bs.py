# -*- coding=utf-8 -*-
import itertools
import random
import time

global sigb  # 谁是地主
sigb = 1

DEBUG0 = 0
MAXLEVEL = 3


class DTree(object):
    def __init__(self, iupltype, iuplvalue, ugyupl, player, value=-1, buiu=0, level=0, score=0):
        self.iupltype = iupltype
        self.iuplvalue = iuplvalue
        self.ugyupl = ugyupl
        self.player = player
        self.value = value
        self.buiu = buiu
        self.level = level
        self.nodes = []
        self.score = score

    def addNode(self, iupltype, iuplvalue, ugyupl, player, value=-1, buiu=0, level=0):
        if buiu > 2:
            return
        if level >= MAXLEVEL:
            score = judge(ugyupl[0])
        else:
            score = -1
        # print("\n{{出牌", iupltype, iuplvalue,
        #       "\n{{剩余牌", ugyupl,
        #       "\n{{player value buiu", player, value, buiu,
        #       "\n{{level", level,
        #       "\n{{score", score)
        node = DTree(iupltype, iuplvalue, ugyupl, player, value, buiu, level, score)
        self.nodes.append(node)
        return


def findfirst(handcards, num):
    listtoappend = []
    for i in range(len(handcards)):
        if handcards[i] >= num:
            listtoappend.append(1)
        else:
            listtoappend.append(0)
    return listtoappend


def findshun(find, findlist):
    # 函数说明
    # find 找几个 单顺就是5 连对就是3
    # findlist 从哪找 单顺就是dj 连对就是dv
    # listtoappend 结果保存list
    left = 0
    #    right = 0
    listtoappend = []
    for i in range(15):
        if findlist[i] == 0:
            continue
        elif findlist[i] == 1:
            if i == 0 or findlist[i - 1] == 0:
                left = i
            else:
                right = i
                if right - left > find - 2:
                    # 组成顺子 加到顺子列表里
                    if right < 12:
                        listtoappend.append((left, right))
        else:
            print("Wrong!")
            exit(-1)
    return listtoappend


def findxdx(a, b, m):
    '''
    :param a: 带list
    :param b: 被带list
    :param m: 带几张
    :return: 带好的list
    '''
    temp = []
    for i in range(15):
        if b[i] == 1:
            temp.append(i)  # 可以带的list
    if m > 1:
        temp = list(itertools.combinations(temp, m))
    listtoappend = []
    for i in range(15):
        if a[i] == 1:  # 说明sj[i]可以带
            for ii in range(len(temp)):
                if m > 1:
                    ok = 1
                    for iii in range(len(temp[0])):
                        if temp[ii][iii] == i:
                            ok = 0
                else:
                    if temp[ii] != i:
                        ok = 1
                    else:
                        ok = 0
                if ok:
                    listtoappend.append((i, temp[ii]))
    return listtoappend


def findfzji(a, b, ln, rn):
    '''
    :param a: 带的list
    :param b: 被带的list
    :param ln: 带的数目
    :param rn: 被带的数目
    :return: 飞机list
    '''
    temp = []
    for i in range(len(a)):
        if a[i][1] - a[i][0] == ln - 1:
            temp.append(a[i])
    btemp = []
    for i in range(15):
        if b[i] == 1:
            btemp.append(i)  # 可以带的list
    btemp = list(itertools.combinations(btemp, rn))
    listtoappend = []
    for i in range(len(temp)):
        for ii in range(len(btemp)):
            ok = 1
            for iii in range(rn):
                if temp[i][0] <= btemp[ii][iii] <= temp[i][1]:
                    ok = 0
            if ok:
                listtoappend.append((temp[i], btemp[ii]))
    return listtoappend


def display(handcards, nhandcards, lhandcards):
    print("handcards:", handcards)
    print("nhandcards:", nhandcards)
    print("lhandcards:", lhandcards)
    return


def randomcard():
    handcards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lhandcards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    nhandcards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fcards = random.sample(range(54), 54)
    for m in range(54):
        if m < 17:
            if fcards[m] == 53:
                lhandcards[14] += 1
            else:
                lhandcards[fcards[m] // 4] += 1
        elif 17 <= m < 34:
            if fcards[m] == 53:
                nhandcards[14] += 1
            else:
                nhandcards[fcards[m] // 4] += 1
        else:
            if fcards[m] == 53:
                handcards[14] += 1
            else:
                handcards[fcards[m] // 4] += 1
    return handcards, nhandcards, lhandcards


def chaipai(handcards):
    # 拆牌
    dj = findfirst(handcards, 1)
    dv = findfirst(handcards, 2)
    sj = findfirst(handcards, 3)
    si = findfirst(handcards, 4)
    djvh = []
    dvzi = []
    sjvh = []
    vadj = []
    for i in range(14):
        if dj[i] == 1:
            djvh.append(i)
        if dv[i] == 1:
            dvzi.append(i)
        if sj[i] == 1:
            sjvh.append(i)
        if si[i] == 1:
            vadj.append(i)
        if dj[13] == 1 and dj[14] == 1:
            vadj.append(13)
    # 下面建立顺子列表 从单张列表里找到连续5个以上有值的
    upzi = findshun(5, dj)
    lmdv = findshun(3, dv)
    sjlm = findshun(2, sj)
    silm = findshun(2, si)
    # 下面建立x带x列表
    sjdlyi = findxdx(sj, dj, 1)
    sjdlor = findxdx(sj, dv, 1)
    sidlor = findxdx(si, dj, 2)
    sidllddv = findxdx(si, dv, 2)
    #  下面建立飞机列表
    orlmfzji = findfzji(sjlm, dj, 2, 2)
    orlmfzji2 = findfzji(sjlm, dv, 2, 2)
    sjlmfzji = findfzji(sjlm, dj, 3, 3)
    sjlmfzji2 = findfzji(sjlm, dv, 3, 3)
    silmfzji = findfzji(sjlm, dj, 4, 4)
    silmfzji2 = findfzji(sjlm, dv, 4, 4)
    wulmfzji = findfzji(sjlm, dj, 5, 5)
    hhtmfzji = findfzji(silm, dj, 2, 4)
    hhtmfzji3 = findfzji(silm, dj, 3, 6)
    hhtmfzji2 = findfzji(silm, dv, 2, 4)
    # 可出牌list建立完毕
    if DEBUG0:
        if djvh:
            print('单张', djvh)
        if dvzi:
            print('对子', dvzi)
        if sjvh:
            print('三张', sjvh)
        if vadj:
            print('炸弹', vadj)
        if upzi:
            print("顺子", upzi)
        if lmdv:
            print("连对", lmdv)
        if sjlm:
            print("三连", sjlm)
        if silm:
            print("四连", silm)
        if sjdlyi:
            print("三带一：", sjdlyi)
        if sjdlor:
            print("三带二：", sjdlor)
        if sidlor:
            print("四带二：", sidlor)
        if sidllddv:
            print("四带两对：", sidllddv)
        if orlmfzji:
            print("二连飞机", orlmfzji)
        if orlmfzji2:
            print("二连飞机 对", orlmfzji2)
        if sjlmfzji:
            print("三连飞机", sjlmfzji)
        if sjlmfzji2:
            print("三连飞机 对", sjlmfzji2)
        if silmfzji:
            print("四连飞机", silmfzji)
        if silmfzji2:
            print("四连飞机 对", silmfzji2)
        if wulmfzji:
            print("五连飞机", wulmfzji)
        if hhtmfzji:
            print("二连航天飞机", hhtmfzji)
        if hhtmfzji2:
            print("二连航天飞机 对", hhtmfzji2)
        if hhtmfzji3:
            print("三连航天飞机", hhtmfzji3)
    return {"djvh": djvh, "dvzi": dvzi, "sjvh": sjvh, "vadj": vadj, "upzi": upzi, "lmdv": lmdv, "sjlm": sjlm,
            "silm": silm, "sjdlyi": sjdlyi, "sjdlor": sjdlor, "sidlor": sidlor, "sidllddv": sidllddv,
            "orlmfzji": orlmfzji, "orlmfzji2": orlmfzji2, "sjlmfzji": sjlmfzji, "sjlmfzji2": sjlmfzji2,
            "silmfzji": silmfzji, "silmfzji2": silmfzji2, "wulmfzji": wulmfzji, "hhtmfzji": hhtmfzji,
            "hhtmfzji2": hhtmfzji2, "hhtmfzji3": hhtmfzji3}


def checkhandsdict(pushcarddict):  # 去掉空的项
    keydel = []
    for key in pushcarddict:
        if len(pushcarddict[key]) == 0:
            keydel.append(key)
    for i in keydel:
        pushcarddict.pop(i)
    return pushcarddict


def isend(handcards, nhandcards, lhandcards, sigb):
    '''

    :param handcards:
    :param nhandcards:
    :param lhandcards:
    :param sigb:    1   我是地主
                    2   下家是地主
                    3   上家是地主
    :return:    1   赢
                0   输
                -1  未完待续
    '''

    sig = 4

    sum = 0
    for i in range(14):
        sum += handcards[i]
    if sum == 0:
        sig = 1

    sum = 0
    for i in range(14):
        sum += nhandcards[i]
    if sum == 0:
        sig = 2

    sum = 0
    for i in range(14):
        sum += lhandcards[i]
    if sum == 0:
        sig = 3

    if sig == 4:
        return -1
    if (sigb == 1 and (sig == 2 or sig == 3)) or (sigb == 2 and sig == 2) or (sigb == 3 and sig == 3):
        return 0
    else:
        return 1


def sumofcards(type, value):
    numdict = {"djvh": 1, "dvzi": 2, "sjvh": 3, "vadj": 4, "sjdlyi": 4, "sjdlor": 5, "sidlor": 6, "sidllddv": 8,
               "orlmfzji": 8, "orlmfzji2": 10, "sjlmfzji": 12, "sjlmfzji2": 15,
               "silmfzji": 16, "silmfzji2": 20, "wulmfzji": 20, "hhtmfzji": 12,
               "hhtmfzji2": 16, "hhtmfzji3": 18}
    if type in numdict.keys():
        return numdict[type]
    upnumdict = {"upzi": 1, "lmdv": 2, "sjlm": 3, "silm": 4}
    if type in upnumdict.keys():
        return (value[1] - value[0]) * upnumdict[type]
    else:
        print("Wrong in 005")
        return -1


def isbigger(type, myvalue, hisvalue):
    # TODO(炸弹 王炸)
    type1 = ["djvh", "dvzi", "sjvh", "vadj"]
    type2 = ["sjdlyi", "sjdlor", "sidlor", "sidllddv", "upzi", "lmdv", "sjlm", "silm"]
    if DEBUG0:
        print("type:", type, "  myvalue:", myvalue, "  hisvalue:", hisvalue)
    if type in type1:
        if myvalue > hisvalue:
            return 1
        else:
            return 0
    elif type in type2:
        if myvalue[0] > hisvalue[0]:
            return 1
        else:
            return 0
    else:
        if myvalue[0][0] > hisvalue[0][0]:
            return 1
        else:
            return 0


def hvfu(type, value):  # 把出牌恢复成01的形式
    odlcards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    numdict = {"djvh": 1, "dvzi": 2, "sjvh": 3, "vadj": 4, "upzi": 1, "lmdv": 2, "sjlm": 3, "silm": 4, "sjdlyi": (3, 1),
               "sjdlor": (3, 2), "sidlor": (4, 1), "sidllddv": (4, 2), "orlmfzji": (3, 1), "orlmfzji2": (3, 2),
               "sjlmfzji": (3, 1), "sjlmfzji2": (3, 2), "silmfzji": (3, 1), "silmfzji2": (3, 2), "wulmfzji": (3, 1),
               "hhtmfzji": (4, 1), "hhtmfzji2": (4, 2), "hhtmfzji3": (4, 1)}
    if type in {"djvh", "dvzi", "sjvh", "vadj"}:
        odlcards[value] = numdict[type]
    if type in {"upzi", "lmdv", "sjlm", "silm"}:
        for i in range(value[0], value[1] + 1):
            odlcards[i] = numdict[type]
    if type in {"sjdlyi", "sjdlor"}:
        odlcards[value[0]] = numdict[type][0]
        odlcards[value[1]] = numdict[type][1]
    if type in {"sidlor", "sidllddv"}:
        odlcards[value[0]] = numdict[type][0]
        odlcards[value[1][0]] = numdict[type][1]
        odlcards[value[1][1]] = numdict[type][1]
    if type in {"orlmfzji", "orlmfzji2", "sjlmfzji", "sjlmfzji2",
                "silmfzji", "silmfzji2", "wulmfzji", "hhtmfzji",
                "hhtmfzji2", "hhtmfzji3"}:
        for i in range(value[0][0], value[0][1] + 1):
            odlcards[i] = numdict[type][0]
        for i in value[1]:
            odlcards[i] = numdict[type][1]
    return odlcards


def gen_game_tree(root):
    # 把可出牌list 包括不出, 出牌后剩余牌,该谁出牌了 加到root下1层
    # 遍历这一层 每个节点当成root 建立可出list 有人赢了就停止
    # 列出所有能出的情况
    # print("$$$root level", root.level)
    # print("出牌 ", root.iupltype, root.iuplvalue)
    # print("剩余牌 ", root.ugyupl)
    if root.value != -1:
        return
    if root.level > MAXLEVEL:
        return
    (handcards, nhandcards, lhandcards) = root.ugyupl
    a = root.level % 3  # a:0该我出 1该n出 2该2出
    if root.iupltype == 'root' or root.buiu == 2:  # 随便出
        canpush = chaipai(root.ugyupl[a])
        canpush = checkhandsdict(canpush)
    else:  # 按root.iupl出
        odlcards = hvfu(root.iupltype, root.iuplvalue)  # 把出牌恢复成01的形式
        canpush = keiu(odlcards, root.ugyupl[a])
    backup = (handcards, nhandcards, lhandcards)
    if canpush:
        for key in canpush:
            for i in range(len(canpush[key])):
                handcards, nhandcards, lhandcards = backup
                odlcards = hvfu(key, canpush[key][i])
                if root.player == 'w':
                    handcards = list(map(lambda x: x[0] - x[1], zip(handcards, odlcards)))
                    player = 'n'
                elif root.player == 'n':
                    nhandcards = list(map(lambda x: x[0] - x[1], zip(nhandcards, odlcards)))
                    player = 'l'
                elif root.player == 'l':
                    lhandcards = list(map(lambda x: x[0] - x[1], zip(lhandcards, odlcards)))
                    player = 'w'
                endvalue = isend(handcards, nhandcards, lhandcards, sigb)  # 判断是否游戏结束了
                if endvalue == 1:  # 如果结束了就加上权值
                    value = 100  # 赢了100
                elif endvalue == 0:
                    value = 0  # 输了0
                else:
                    value = -1
                uupp = (handcards, nhandcards, lhandcards)
                if DEBUG0:
                    print("原手牌\n", root.ugyupl[a],
                          "出牌", key, canpush[key][i], "\n",
                          "现手牌\n", uupp[0], "\n", uupp[1], "\n", uupp[2], "\n")
                if value not in {-1, 0, 100}:
                    print("ERROR value", value)
                root.addNode(key,
                             canpush[key][i],
                             uupp,
                             player,
                             value,
                             0,
                             root.level + 1)
        # 下面是不出
        if root.player == 'w':
            player = 'n'
        elif root.player == 'n':
            player = 'l'
        elif root.player == 'l':
            player = 'w'
        root.addNode(root.iupltype, root.iuplvalue, root.ugyupl, player, -1, root.buiu + 1, root.level + 1)
    else:
        # 下面是不出
        if root.player == 'w':
            player = 'n'
        elif root.player == 'n':
            player = 'l'
        elif root.player == 'l':
            player = 'w'
        root.addNode(root.iupltype, root.iuplvalue, root.ugyupl, player, -1, root.buiu + 1, root.level + 1)
    for i in root.nodes:
        gen_game_tree(i)
    return


def keiu(odlcards, handcards):
    '''

    :param odlcards: 需要跟的牌
    :param handcards: 手牌
    :return: 可出dict
    '''
    sum = 0
    for i in odlcards:
        sum += i
    odlcardsdict = chaipai(odlcards)
    # 下面需要把odl的出牌类型确定 也就是把冗余类型删除
    keydel = []
    numdict = {"djvh": 1, "dvzi": 2, "sjvh": 3, "vadj": 4, "upzi": 0, "lmdv": 0, "sjlm": 0,
               "silm": 0, "sjdlyi": 4, "sjdlor": 5, "sidlor": 6, "sidllddv": 8,
               "orlmfzji": 8, "orlmfzji2": 10, "sjlmfzji": 12, "sjlmfzji2": 15,
               "silmfzji": 16, "silmfzji2": 20, "wulmfzji": 20, "hhtmfzji": 12,
               "hhtmfzji2": 16, "hhtmfzji3": 18}

    for key in odlcardsdict:
        upnumdict = {"upzi": 1, "lmdv": 2, "sjlm": 3, "silm": 4}
        if key in upnumdict.keys():  # 如果是顺子   要选最大的那一个
            upzilist = odlcardsdict[key]
            if not upzilist:  # 如果是空的 直接continue
                continue
            seg = upzilist[len(upzilist) - 1]  # seg 是最后一个
            isum = (seg[1] - seg[0] + 1) * upnumdict[key]  # isum是顺子长度
            if isum == sum:
                odlcardsdict = {key: [seg]}
                break
    for key in odlcardsdict:
        if len(odlcardsdict[key]) != 1:
            keydel.append(key)
            continue
        if numdict[key] < sum:
            keydel.append(key)
    for i in keydel:
        odlcardsdict.pop(i)
    if DEBUG0:
        print("我需要跟：", odlcardsdict)  # 我需要跟什么牌
    handsdict = chaipai(handcards)
    handsdict = checkhandsdict(handsdict)  # 我可以出什么牌
    try:
        histype = list(odlcardsdict.keys())[0]  # 需要跟的牌型
        hisvalue = list(odlcardsdict.values())[0][0]  # 需要跟的牌值
    except:
        # print("WARNING:", odlcardsdict)
        hisvalue = 'x'
        histype = 'x'
    canpush = {}  # 可出字典
    for key in handsdict:
        if key == "vadj" and histype != "vadj":
            jud1 = 1
        else:
            jud1 = 0
        if key == histype:
            jud2 = 1
        else:
            jud2 = 0
        for i in range(len(handsdict[key])):
            if sumofcards(key, handsdict[key][i]) == sum:
                jud3 = 1
            else:
                jud3 = 0
            if jud1 or jud2 and jud3 and isbigger(key, handsdict[key][i], hisvalue):
                if key in canpush:
                    canpush[key].append(handsdict[key][i])
                else:
                    canpush[key] = [handsdict[key][i]]
    return canpush


def judge(cards):
    # cardsdict = chaipai(cards)
    # cardsdict = checkhandsdict(cardsdict)
    # score = 0
    # scoredict = {"djvh": 10, "dvzi": 20, "sjvh": 40, "vadj": 200, "upzi": 50, "lmdv": 60, "sjlm": 50,
    #              "silm": 50, "sjdlyi": 50, "sjdlor": 50, "sidlor": 60, "sidllddv": 60,
    #              "orlmfzji": 100, "orlmfzji2": 100, "sjlmfzji": 100, "sjlmfzji2": 100,
    #              "silmfzji": 100, "silmfzji2": 100, "wulmfzji": 100, "hhtmfzji": 100,
    #              "hhtmfzji2": 100, "hhtmfzji3": 100}
    # for key in cardsdict:
    #     score += scoredict[key]
    score2 = 200
    for i in cards:
        score2 -= i * 10
    return score2


def judge_tree(root):
    # print(root.level, root.iupltype, root.iuplvalue, root.score)
    if not root.nodes:
        return root.score
    a = []
    for i in root.nodes:
        i.score = judge_tree(i)
        a.append(i.score)

    # print(a)
    root.score = max(a)
    return root.score


def main():
    # handcards = [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # nhandcards = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # lhandcards = [0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    (handcards, nhandcards, lhandcards) = randomcard()
    # cards ready
    ijb = 99
    while True:  # not end:
        display(handcards, nhandcards, lhandcards)
        sig = input('请输入状态码：（0-游戏结束 1-该其他玩家出牌了 2-该我出牌了)')
        if sig == '0':  # end
            exit()
        elif sig == '1':  # others's turn
            whost = input('该上家(l)出牌了还是下家(n)？(n/l)')
            ij = input("他出牌了吗？(y/n)")
            if ij == 'y':
                while True:
                    ijb = 0
                    ocards = input("请输入他出的牌")
                    odcards = (ocards.split(' '))
                    try:
                        odlcards = [int(odcards[i]) for i in range(len(odcards))]
                    except:
                        print("输入有误")
                        continue
                    if len(odlcards) != 15:
                        print("输入有误")
                        continue
                    if whost == 'n':
                        nhandcards = list(map(lambda x: x[0] - x[1], zip(nhandcards, odlcards)))
                    elif whost == 'l':
                        lhandcards = list(map(lambda x: x[0] - x[1], zip(lhandcards, odlcards)))
                    else:
                        print("输入有误")
                        exit(-1)
                    break
            elif ij == 'n':
                ijb += 1
            else:
                print("输入有误")
                exit(-1)
        elif sig == '2':  # my turn
            if DEBUG0:
                print("ijb = ", ijb)
            if ijb > 1:  # 随便出
                pushcarddict = chaipai(handcards)
                pushcarddict = checkhandsdict(pushcarddict)
                if DEBUG0:
                    print(pushcarddict)
                # iuma = input("出牌吗?(y/n)")
                # if iuma == "y":
                #     while True:
                #         display(handcards, nhandcards, lhandcards)
                #         ocards = input("请输入你出的牌")
                #         odcards = (ocards.split(' '))
                #         try:
                #             odlcards = [int(odcards[i]) for i in range(len(odcards))]
                #         except:
                #             print("输入有误")
                #             continue
                #         if len(odlcards) != 15:
                #             print("输入有误")
                #             continue
                #         handcards = list(map(lambda x: x[0] - x[1], zip(handcards, odlcards)))
                #         break
                # else:
                #     continue
                ugyupl = (handcards, nhandcards, lhandcards)
                root = DTree("root", "root", ugyupl, "w")
                print(time.clock())
                gen_game_tree(root)  # 博弈树建立结束
                maxa = judge_tree(root)
                print(time.clock())
                for i in root.nodes:
                    if maxa == i.score:
                        print("出牌：", i.iupltype, i.iuplvalue)
                        break
                # for i in range(len(root.nodes)):
                #     print(root.nodes[i].score)
                # print(maxa)
            else:  # 根据odlcards出
                canpush = keiu(odlcards, handcards)
                if not canpush:
                    print("要不起！")
                else:
                    if DEBUG0:
                        print("可出：", canpush)
                    # iuma = input("出牌吗?(y/n)")
                    # if iuma == "y":
                    #     while True:
                    #         display(handcards, nhandcards, lhandcards)
                    #         ocards = input("请输入你出的牌")
                    #         odcards = (ocards.split(' '))
                    #         try:
                    #             odlcards = [int(odcards[i]) for i in range(len(odcards))]
                    #         except:
                    #             print("输入有误")
                    #             continue
                    #         if len(odlcards) != 15:
                    #             print("输入有误")
                    #             continue
                    #         handcards = list(map(lambda x: x[0] - x[1], zip(handcards, odlcards)))
                    #         break

                    # 建立决策树
                    # 反向评分
                    # 选择评分最高的项 并出牌
                    ugyupl = (handcards, nhandcards, lhandcards)
                    root = DTree("root", "root", ugyupl, "w")
                    gen_game_tree(root)  # 博弈树建立结束
                    maxa = judge_tree(root)
                    for i in root.nodes:
                        if maxa == i.score:
                            print("出牌：", i.iupltype, i.iuplvalue)
                            break
        else:
            print("Wrong in 003")
            exit(-1)
        isendnum = isend(handcards, nhandcards, lhandcards, sigb)
        if isendnum == 1:
            print("我赢了")
            break
        elif isendnum == 2:
            print("下家赢了")
            break
        elif isendnum == 3:
            print("上家赢了")
            break
        else:
            print("继续游戏")
    return


main()
