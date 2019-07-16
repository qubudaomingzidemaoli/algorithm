#黑白棋问题
#黑白棋哪一方可以必胜（或者必不败）
'''
罗列一些特殊情况：
1.如果A方下完棋子，B方没有一个点可以下，则A可以继续下棋
2.会出现A方下完之后吃完B的所有棋子，此时游戏结束
3.
4.帮黑子下第一颗子，好像是可以减掉3/4的运算量
5.在程序实际的运行过程中，出现了 （棋盘未满 and 双方都有棋 and 双方都无法继续下） 的情况
'''

import copy
import sys
sys.setrecursionlimit(1000000)

class ChessSituation():
    def __init__(
        self,
        Size=8,#棋盘的大小
        White=[],#白棋坐标的列表
        Black=[],#黑棋坐标的列表
        PreS=None,#指向先前的棋盘
        NxtS=[],#指向下几个棋盘
        Flag=True,#下一方的颜色
        PNxtS=0,#指针指向下第几个棋盘，用于判断NxtS是否完全遍历
        Lead=0,#代表领先的棋子数量，黑子比白子多则为负，反之为正
        ):
        self.Size=Size
        self.White=[(Size/2,Size/2)]
        self.Black=[(Size/2-1,Size/2),(Size/2,Size/2-1),(Size/2-1,Size/2-1),(Size/2-1,Size/2-2)]
        self.PreS=PreS
        self.NxtS=NxtS
        self.Flag=Flag
        self.PNxtS=PNxtS
        self.Lead=Lead

class BlackWhiteChess():
    def __init__(self,Size=8,TiePriorRegret=True):
        self.Size=Size#棋盘大小
        self.TiePriorRegret=TiePriorRegret#平局优先反悔，默认为白色，即如果平局，由白子先寻找
        self.Start=ChessSituation(Size=self.Size)#棋盘的开始

    def Solution(self):
        p=self.Start#p相当于指针，指向正在使用的棋盘
        SizeSize=self.Size**2#棋盘的总大小

        def Find(CS):
            #参数是一个ChessSituation对象，返回一个list对象
            #用于寻找是否有可能的方法，给的参数是一个ChessSituation，返回一个list对象，其中存放的
            #每一项的值的形式为（（x，y），z）其中x，y是坐标，z是方向，该方向指的是能下的点的哪个方
            #向可以吃子
            S=[]#用于返回的set对象
            pc=None
            pnc=None
            if(CS.Flag==True):#如果是白棋
                pc=CS.White
                pnc=CS.Black
            else:#如果是黑棋
                pc=CS.Black
                pnc=CS.White
            for _ in pc:
                #检测左上角7所在的直线是否有可以下的点
                if((_[0]-1,_[1]-1) in pnc):#如果该点的7方向有异色点
                    p7=(_[0]-1,_[0]-1)#指针指向(x-1,y-1)
                    while(p7[0]>0 and p7[1]>0):#如果这个点横纵坐标大于0
                        p7=(p7[0]-1,p7[1]-1)#向7方向移动一步
                        if(p7 in pnc):#在此方向出现异色点
                            continue#继续移动
                        if(p7 in pc):#在此方向出现同色点
                            break#退出循环
                        else:#在此方向出现了空格
                            S.append((p7,3))#将此点加入S中,3是7的相反方向
                            break
                if((_[0],_[0]-1) in pnc):#8
                    p8=(_[0],_[1]-1)
                    while(p8[1]>0):
                        p8=(p8[0],p8[1]-1)
                        if(p8 in pnc):
                            continue
                        if(p8 in pc):
                            break
                        else:
                            S.append((p8,2))
                            break
                if((_[0]+1,_[1]-1) in pnc):#9
                    p9=(_[0]+1,_[1]-1)
                    while(p9[0]<self.Size-1 and p9[1]>0):
                        p9=(p9[0]+1,p9[1]-1)
                        if(p9 in pnc):
                            continue
                        if(p9 in pc):
                            break
                        else:
                            S.append((p9,1))
                            break
                if((_[0]-1,_[1]) in pnc):#4
                    p4=(_[0]-1,_[1])
                    while(p4[0]>0):
                        p4=(p4[0]-1,p4[1])
                        if(p4 in pnc):
                            continue
                        if(p4 in pc):
                            break
                        else:
                            S.append((p4,6))
                            break
                if((_[0]+1,_[1]) in pnc):#6
                    p6=(_[0]+1,_[1])
                    while(p6[0]<self.Size-1):
                        p6=(p6[0]+1,p6[1])
                        if(p6 in pnc):
                            continue
                        if(p6 in pc):
                            break
                        else:
                            S.append((p6,4))
                            break
                if((_[0]-1,_[1]+1) in pnc):#1
                    p1=(_[0]-1,_[1]+1)
                    while(p1[0]>0 and p1[1]<self.Size-1):
                        p1=(p1[0]-1,p1[1]+1)
                        if(p1 in pnc):
                            continue
                        if(p1 in pc):
                            break
                        else:
                            S.append((p1,9))
                            break
                if((_[0],_[1]+1) in pnc):#2
                    p2=(_[0],_[1]+1)
                    while(p2[1]<self.Size-1):
                        p2=(p2[0],p2[1]+1)
                        if(p2 in pnc):
                            continue
                        if(p2 in pc):
                            break
                        else:
                            S.append((p2,8))
                            break
                if((_[0]+1,_[1]+1) in pnc):#3
                    p3=(_[0]+1,_[1]+1)
                    while(p3[0]<self.Size-1 and p3[1]<self.Size-1):
                        p3=(p3[0]+1,p3[1]+1)
                        if(p3 in pnc):
                            continue
                        if(p3 in pc):
                            break
                        else:
                            S.append((p3,7))
                            break
            return S

        def SetDown(CS,S):
            #参数是一个ChessSituation和一个list对象，不需要返回
            #参数中S的值表示：（（x，y），z）在x，y能下，并且在z方向可以吃子
            #list中的每一个变量：list[n].White，list[n].Black
            #list[n].PreS=CS
            #list[n].Flag=not list[n].PreS.Flag（调换颜色）
            #CS中需要修改的东西：CS.NxtS=list
            Temp=[]#CS.NxtS指向的列表
            a=[]#无用，中间变量
            b=[]#无用，中间变量
            c=[]#合并后的变量，其中的形式为[((x,y),[a,b,c])，···]，其中x,y是坐标，abc是方向
            for s1,s2 in S:
                if(not s1 in a):
                    a.append(s1)
                    b.append([s2])
                else:
                    b[a.index(s1)].append(s2)
            c=list(zip(a,b))
            for _ in c:#((x,y),[a,b,c])
                CSTemp=copy.deepcopy(CS)
                if(CS.Flag==True):#如果先前的棋盘的颜色是白色
                    CSTemp.White.append(_[0])#白色棋子中添加可以下的棋子
                else:#如果先前下的棋盘的颜色是黑色
                    CSTemp.Black.append(_[0])#黑色棋子中添加可以下的棋子
                if(7 in _[1]):#如果在列表中有7方向的标记
                    pp=(_[0][0]-1,_[0][1]-1)
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0]-1,pp[1]-1)
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0]-1,pp[1]-1)
                if(8 in _[1]):
                    pp=(_[0][0],_[0][1]-1)
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0],pp[1]-1)
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0],pp[1]-1)
                if(9 in _[1]):
                    pp=(_[0][0]+1,_[0][1]-1)
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0]+1,pp[1]-1)
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0]+1,pp[1]-1)
                if(4 in _[1]):
                    pp=(_[0][0]-1,_[0][1])
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0]-1,pp[1])
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0]-1,pp[1])
                if(6 in _[1]):
                    pp=(_[0][0]+1,_[0][1])
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0]+1,pp[1])
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0]+1,pp[1])
                if(1 in _[1]):
                    pp=(_[0][0]-1,_[0][1]+1)
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0]-1,pp[1]+1)
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0]-1,pp[1]+1)
                if(2 in _[1]):
                    pp=(_[0][0],_[0][1]+1)
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0],pp[1]+1)
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0],pp[1]+1)
                if(3 in _[1]):
                    pp=(_[0][0]+1,_[0][1]+1)
                    if(CS.Flag==True):#如果吃棋方是白色，被吃方是黑色
                        while(pp in CSTemp.Black):
                            CSTemp.Black.remove(pp)
                            CSTemp.White.append(pp)
                            pp=(pp[0]+1,pp[1]+1)
                    else:#如果吃方是黑色，被吃方是白色
                        while(pp in CSTemp.White):
                            CSTemp.White.remove(pp)
                            CSTemp.Black.append(pp)
                            pp=(pp[0]+1,pp[1]+1)
                CSTemp.Flag=not CSTemp.Flag
                CSTemp.PreS=CS
                Temp.append(CSTemp)
            CS.NxtS=Temp


        while(True):
            if(len(p.NxtS)==0):#如果指向的下面的棋盘为空
                if(len(p.Black)+len(p.White)==SizeSize):#如果棋盘下满
                    p.Lead=len(p.White)-len(p.Black)#算出领先
                    '''标记'''
                    print(p.Lead)
                    if(p.Lead>0):#如果是白子赢了,则寻找黑子的悔棋
                        while(p.PreS.Flag!=False):
                            p=p.PreS
                        p=p.PreS
                    elif(p.Lead<0):#如果是黑子赢了，则寻找白子的悔棋
                        while(p.PreS.Flag!=True):
                            p=p.PreS
                        p=p.PreS
                    else:#如果平局，则寻找平局优先反悔的悔棋
                        while(p.PreS.Flag!=self.TiePriorRegret):
                            p=p.PreS
                        p=p.PreS
                elif(len(p.Black)==0):#黑子被吃完，寻找黑子的悔棋
                    while(p.PreS.Flag!=False):
                        p=p.PreS
                    p=p.PreS
                elif(len(p.White)==0):#白子被吃完，寻找白子的悔棋
                    while(p.PreS.Flag!=True):
                        p=p.PreS
                    p=p.PreS
                else:#如果棋局没有结束，开始算出NxtS，然后走到下一层
                    ST=Find(p)
                    if(len(ST)!=0):#假如可以下子，就是正常情况
                        SetDown(p,ST)#落子
                        p.PNxtS+=1#将棋盘指针加一
                        p=p.NxtS[p.PNxtS-1]#进入棋盘指针减一的棋盘
                    else:#假如不能下子，就是出现了正常一方无法下，另一方要继续下
                        p.Flag=not p.Flag#将标记置反
                        ST=Find(p)#继续寻找是否能下
                        if(len(ST)!=0):#假如另一方可以下
                            SetDown(p,ST)
                            p.PNxtS+=1
                            p=p.NxtS[p.PNxtS-1]
                        else:#另一方也无法继续下，视为结束，开始回溯
                            p.Lead=len(p.White)-len(p.Black)#算出领先值
                            '''标记'''
                            print(p.Lead)
                            if(p.Lead>0):#如果是白子赢了,则寻找黑子的悔棋
                                while(p.PreS.Flag!=False):
                                    p=p.PreS
                                p=p.PreS
                            elif(p.Lead<0):#如果是黑子赢了，则寻找白子的悔棋
                                while(p.PreS.Flag!=True):
                                    p=p.PreS
                                p=p.PreS
                            else:#如果平局，则寻找平局优先反悔的悔棋
                                while(p.PreS.Flag!=TiePriorRegret):
                                    p=p.PreS
                                p=p.PreS
            else:#如果指向的下面的棋盘不为空
                if(p.PNxtS<len(p.NxtS)):#如果指针PNxtS没有遍历完所有的情况
                    p.PNxtS+=1
                    p=p.NxtS[p.PNxtS-1]
                else:#如果遍历完所有的情况
                    newFlag=p.Flag
                    if(p.PreS==None):
                        return
                    while(p.PreS.Flag!=newFlag):
                        p=p.PreS
                        if(p.PreS==None):
                            return
                    p=p.PreS

a=BlackWhiteChess(Size=4,TiePriorRegret=True)
a.Solution()
