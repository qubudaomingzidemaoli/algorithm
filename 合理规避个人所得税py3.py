'''
通过合理调配月薪和年薪使得总缴税最低
'''
def count(mm=0,ym=0,om=0,b=None):#月工资，年工资，月免税，税前总收入
    
    cm=mm-om-5000#月工资减去扣除再减去5000
        
    l={'omm':0,#旧月税后收入
       'omt':0,#旧月缴税
       'oym':0,#旧年终税后收入
       'oyt':0,#旧年终缴税
       'nmm':0,#新月税后收入
       'nmt':0,#新月缴税
       'nym':0,#新年终税后收入
       'nyt':0,#新年终缴税
       'om':0,#旧税后收入
       'ot':0,#旧税收总和
       'nm':0,#新税后收入
       'nt':0#新税收总和
         }

    QuitSub=[0,#速算扣除数
             210,
             1410,
             2660,
             4410,
             7160,
             15160]
    
    Temp=[(0,3000),#月收入区间
          (3000,12000),
          (12000,25000),
          (25000,35000),
          (35000,55000),
          (55000,80000),
          (80000,9999999999999)]
    YearTemp=[(0,36000),#年化月收入区间
              (36000,144000),
              (144000,300000),
              (300000,420000),
              (420000,660000),
              (660000,960000),
              (960000,9999999999999),]
    TaxRate=[0.03,#税率
             0.1,
             0.2,
             0.25,
             0.3,
             0.35,
             0.45]
    TaxRange=[(240000,263100),#五个特殊区间
              (504000,552000),
              (780000,806200),
              (1140000,1154167),
              (1680000,1728889)]
    
    #计算旧的月收入和月税收,omm,omt
    if(cm<0):
        l['omm']=mm-om
        l['omt']=0
    else:
        for _ in range(len(Temp)):
            if(Temp[_][0]<cm<=Temp[_][1]):
                l['omt']=cm*TaxRate[_]-QuitSub[_]
                l['omm']=mm-l['omt']-om
    #计算旧的年收入和年税收,oym,oyt
    mym=ym/12#年收入月化
    for _ in range(len(Temp)):
        if(Temp[_][0]<mym<=Temp[_][1]):
            l['oyt']=ym*TaxRate[_]-QuitSub[_]
            l['oym']=ym-l['oyt']
    #计算旧税后收入和旧税收总和，om,ot
    l['om']=l['omm']*12+l['oym']
    l['ot']=l['omt']*12+l['oyt']
    #计算税前总收入,bm
    bm=None
    if(b==None):
        bm=l['om']+l['ot']
    else:
        bm=b
    #计算新税后收入
    TRTF=False#特殊标志
    c=-1#特殊区间位置
    for _ in range(len(TaxRange)):
        if(TaxRange[_][0]<=bm<TaxRange[_][1]):#这里的等号待求证
            TRTF=True
            c=_
    if(TRTF):#如果在特殊区间内的情况,把多的钱挂在月薪上
        if(c==0):
            l['nyt']=36000*0.03
            l['nym']=36000*0.97
            
            m_=bm-36000-60000#减去放在年收入中的和60k的免税金额
            m_t=m_*0.2-1410*12#年化的应缴税额
            m_m=m_-m_t+60000#年化后的税后收入

            l['nmt']=m_t/12
            l['nmm']=m_m/12

            l['nm']=l['nym']+l['nmm']*12
            l['nt']=l['nyt']+l['nmt']*12
        if(c==1):
            l['nyt']=144000*0.1-210
            l['nym']=144000-l['nyt']

            m_=bm-144000-60000
            m_t=m_*0.25-2660*12
            m_m=m_-m_t+60000

            l['nmt']=m_t/12
            l['nmm']=m_m/12

            l['nm']=l['nym']+l['nmm']*12
            l['nt']=l['nyt']+l['nmt']*12
        if(c==2):
            l['nyt']=300000*0.2-1410
            l['nym']=300000-l['nyt']

            m_=bm-300000-60000
            m_t=m_*0.3-4410*12
            m_m=m_-m_t+60000

            l['nmt']=m_t/12
            l['nmm']=m_m/12

            l['nm']=l['nym']+l['nmm']*12
            l['nt']=l['nyt']+l['nmt']*12
        if(c==3):
            l['nyt']=420000*0.25-2660
            l['nym']=420000-l['nyt']

            m_=bm-420000-60000
            m_t=m_*0.35-7160*12
            m_m=m_-m_t+60000

            l['nmt']=m_t/12
            l['nmm']=m_m/12

            l['nm']=l['nym']+l['nmm']*12
            l['nt']=l['nyt']+l['nmt']*12
        if(c==4):
            l['nyt']=660000*0.3-4410
            l['nym']=660000-l['nyt']

            m_=bm-660000-60000
            m_t=m_*0.45-15160*12
            m_m=m_-m_t+60000

            l['nmt']=m_t/12
            l['nmm']=m_m/12

            l['nm']=l['nym']+l['nmm']*12
            l['nt']=l['nyt']+l['nmt']*12
    else:#如果不在特殊区间内的情况
        n=[#顺序，（钱数，位置）0代表月薪，1代表年薪
           (36000,0),
           (36000,1),
           (108000,0),
           (108000,1),
           (156000,0),
           (156000,1),
           (120000,0),
           (120000,1),
           (240000,0),
           (240000,1),
           (300000,0),
           (300000,1),
           (999999999999,0)]
        l0=[]#月收入放进来
        l1=[]#年收入放进来
        if(bm<=60000):
                l['nyt']=0
                l['nym']=0
                l['nmt']=0
                l['nmm']=bm/12
                l['nm']=bm
                l['nt']=0
        else:
            bm=bm-60000
            while(bm>=n[0][0]):
                bm=bm-n[0][0]
                t=(n[0][0],n[0][1])
                n.pop(0)
                if(t[1]==0):
                    l0.append(t[0])
                else:
                    l1.append(t[0])
            t=(n[0][0],n[0][1])
            n.pop(0)
            if(t[1]==0):
                l0.append(bm)
            else:
                l1.append(bm)
            amm=sum(l0)
            aym=sum(l1)
            for _ in range(len(YearTemp)):
                if(YearTemp[_][0]<amm<=YearTemp[_][1]):
                    l['nmt']=amm/12*TaxRate[_]-QuitSub[_]
                    l['nmm']=amm/12-l['nmt']+5000
                if(YearTemp[_][0]<aym<=YearTemp[_][1]):
                    l['nyt']=aym*TaxRate[_]-QuitSub[_]
                    l['nym']=aym-l['nyt']
            l['nm']=l['nmm']*12+l['nym']
            l['nt']=l['nmt']*12+l['nyt']
    print('旧月税后收入'+str(l['omm']))
    print('旧月缴税'+str(l['omt']))
    print('旧年终税后收入'+str(l['oym']))
    print('旧年终缴税'+str(l['oyt']))
    print('新月税后收入'+str(l['nmm']))
    print('新月缴税'+str(l['nmt']))
    print('新年终税后收入'+str(l['nym']))
    print('新年终缴税'+str(l['nyt']))
    print('旧税后总收入'+str(l['om']))
    print('旧缴税总和'+str(l['ot']))
    print('新税后总收入'+str(l['nm']))
    print('新缴税总和'+str(l['nt']))

while(True):
    print('输入1标准模式，输入2老板模式：')
    try:
        ipt=int(input())
        if(ipt==1):
            print('请输入月工资：')
            mm=int(input())
            print('请输入免税金额（如五险一金）：')
            om=int(input())
            print('请输入年终奖：')
            ym=int(input())
            count(mm=mm,om=om,ym=ym)
            input()
        elif(ipt==2):
            print('请输入需要发的工资：')
            b=int(input())
            count(b=b)
            input()
    except(ValueError):
        print('输入错误')
        continue 
        
