#******************************************************************************
#	TABO SPACE REALISTIC ENGINE 
# 	THIS IS MAIN FILE OF THIS ENGINE
#	AUTHOR  : LUCOMSTUDIO / Pi 
#  	LISENCE : MIT
#	VERSION : 2019 JAN 29 LATE
#******************************************************************************

#******************************************************************************
# 1: MODULE IMPORTS

# DISCORD
import asyncio
import discord

# FUNCTIONS
import datetime
import os
import shutil
import smtplib
import random
import PIL
import requests
from io import BytesIO
from io import BytesIO
from PIL import Image 
from PIL import ImageFont 
from PIL import ImageDraw 
from email.mime.text import MIMEText
from usrconfig import tabo_conf
from bin import items
from discord.utils import get
#******************************************************************************



#******************************************************************************
# LOG DEF
# printlog(표시이름, 메시지) 호출시 '[시간/표시이름]-메시지' 반환
def printlog(user, msg):
    print('[%s|%s] - %s'%(datetime.datetime.now(), user, msg))
#******************************************************************************


client = discord.Client()
printlog(tabo_conf.logusr, 'discord.py: ' + discord.__version__)


#******************************************************************************
# DATABASE LINES PATH
line_email = 1
line_pass = 3
line_discordacc = 5
line_money = 7
line_stock = 13
#******************************************************************************


#******************************************************************************
# DB MODULE
# AUTHOR : LucomStudio
def db(usr, line, value):
    usrdata = open(os.getcwd() + '/bin/usr/' + usr + '.txt', mode = 'r', encoding='utf-8')
    usrlines = usrdata.readlines()
    usrdata.close()
    usrlines[line] = value + '\n'
    usrdata = open(os.getcwd() + '/bin/usr/' + usr + '.txt', mode = 'w', encoding='utf-8')
    usrdata.writelines(usrlines)
    usrdata.close()
    printlog('DATABASE', usr + '님의 ' + str(line) + '(ID)값을 ' + value + '로 변경하였습니다.')

def getdb(usr, line):
    usrdata = open(os.getcwd() + '/bin/usr/' + usr + '.txt', mode = 'r', encoding='utf-8')
    usrlines = usrdata.readlines()
    usrdata.close()
    return usrlines[line]
#******************************************************************************


#******************************************************************************
# CASH MODULE
# AUTHOR : Pi

def getmoney(usr, money):
    m = int(getdb(usr, line_money).replace('\n',''))
    m = m + money
    db(usr, line_money, str(m))
#******************************************************************************


#******************************************************************************
# SYSTEM MODULE
# AUTHOR : LucomStudio
# Argument : <@ID>
# Return : discord.Server.User

def get_mention(mt):
    msgmt = mt
    msgmt = msgmt.replace("<@", "")
    msgmt = msgmt.replace(">", "")
    return msgmt
    
#******************************************************************************


#******************************************************************************
# ITEM MODULE
# AUTHOR : LucomStudio

def add_item(usr, id, many):
    stat = getdb(usr, id)
    if(stat == '\n'):
        db(usr, id, many)
    elif int(stat) == 0:
        db(usr, id, many)
    else:
        db(usr,id,int(stat) + many)
#******************************************************************************


#******************************************************************************
# STOCK MODULE
# AUTHOR : Pi
stocknamelist_low = {}
stocknamelist_high = {}
tendency_len_low = []
tendency_low = []
tendency_len_high = []
tendency_high = []
change_amount_low = []
change_amount_high = []


async def changestock():
    global stocknamelist_low
    global stocknamelist_high
    global change_amount_low
    global change_amount_high
    timek = 0
    while 1:
        timem = datetime.datetime.now().timetuple().tm_min
        times = datetime.datetime.now().timetuple().tm_sec
        if timem%5==0 and times==0 and timek==0:
            timek=1
            usrdata = open(os.getcwd() + '/bin/stock.txt', mode='r', encoding='utf-8')
            usrlines = usrdata.readlines()
            usrdata.close()
            stocknamelist_low = eval(usrlines[0])
            stocknamelist_high = eval(usrlines[1])

            for i in range(0,len(tendency_len_low)):
                tendency_len_low[i] = tendency_len_low[i] - 1
                if tendency_len_low[i]<=0:
                    tendency_low[i] = random.randint(-20,21)

                change_amount_low[i] = random.randint(tendency_low[i]-50, tendency_low[i]+51)
                stocknamelist_low[list(stocknamelist_low.keys())[i]] = stocknamelist_low[list(stocknamelist_low.keys())[i]] + change_amount_low[i]

            for i in range(0,len(tendency_len_high)):
                tendency_len_high[i] = tendency_len_high[i] - 1
                if tendency_len_high[i]<=0:
                    tendency_high[i] = random.randint(-50,51)
                
                change_amount_high[i] = random.randint(tendency_high[i]-100, tendency_high[i]+101)
                stocknamelist_high[list(stocknamelist_high.keys())[i]] = stocknamelist_high[list(stocknamelist_high.keys())[i]] + change_amount_high[i]


            usrlines[0] = str(stocknamelist_low) + "\n"
            usrlines[1] = str(stocknamelist_high)
            usrdata = open(os.getcwd() + '/bin/stock.txt', mode='w', encoding='utf-8')
            usrdata.writelines(usrlines)
            usrdata.close()

            embed=discord.Embed(title='TABO 증권 거래소 - **주가 변동 알림**', color=0xad52c6)
            for i in range(0,len(stocknamelist_low)):
                chs = ""
                if change_amount_low[i]>0:
                    chs = "(▲" + str(change_amount_low[i]) + ")"
                elif change_amount_low[i]<0:
                    chs = "(▼" + str(-change_amount_low[i]) + ")"
                else:
                    chs = "(-0)"
                embed.add_field(name='**'+str(list(stocknamelist_low.keys())[i])+'**', value='**' + str(list(stocknamelist_low.values())[i]) +'** COIN' + chs, inline=True)
            for i in range(0,len(stocknamelist_high)):
                chs = ""
                if change_amount_high[i]>0:
                    chs = "(▲" + str(change_amount_high[i]) + ")"
                elif change_amount_high[i]<0:
                    chs = "(▼" + str(-change_amount_high[i]) + ")"
                else:
                    chs = "(-0)"
                embed.add_field(name='**'+str(list(stocknamelist_high.keys())[i])+'**', value='**' + str(list(stocknamelist_high.values())[i]) +'** COIN' + chs, inline=True)

            dtime = datetime.datetime.now()
            embed.set_footer(text=str(dtime.year)+"년 "+str(dtime.month)+"월 "+str(dtime.day)+"일 "+str(dtime.hour)+"시 "+str(dtime.minute)+"분 "+str(dtime.second)+"초")
            # datetime.datetime.year 이렇게는 안되나?

            async for m in client.logs_from(discord.Object(id='531361212668182538'), limit=1): await client.delete_message(m)
            await client.send_message(discord.Object(id='531361212668182538'), embed=embed)
            
            
        else:
            await asyncio.sleep(1)
            if timem%5!=0:
                timek=0

def addstock(n, name):
    global stocknamelist_low
    global stocknamelist_high
    usrdata = open(os.getcwd() + '/bin/stock.txt', mode='r', encoding='utf-8')
    usrlines = usrdata.readlines()
    usrdata.close()
    if n==0:
        stocknamelist_low[name] = 10000
        usrlines[n] = str(stocknamelist_low) + "\n"
    elif n==1:
        stocknamelist_high[name] = 10000
        usrlines[n] = str(stocknamelist_high)

    usrdata = open(os.getcwd() + '/bin/stock.txt', mode='w', encoding='utf-8')
    usrdata.writelines(usrlines)
    usrdata.close()
#******************************************************************************

#******************************************************************************
@client.event
async def on_ready():
    global stocknamelist_low
    global stocknamelist_high
    global tendency_len_low
    global tendency_low
    global tendency_len_high
    global tendency_high
    global change_amount_low
    global change_amount_high
    printlog(tabo_conf.logusr, 'System now connected on Discord API')
    await client.change_presence(game=discord.Game(name="ALPHA_TEST", type=1))
    usrdata = open(os.getcwd() + '/bin/stock.txt', mode='r', encoding='utf-8')
    usrlines = usrdata.readlines()
    usrdata.close()
    stocknamelist_low = eval(usrlines[0])
    stocknamelist_high = eval(usrlines[1])
    print(stocknamelist_low)
    print(stocknamelist_high)
    tendency_len_low = [0]*len(stocknamelist_low)
    tendency_low = [0]*len(stocknamelist_low)
    tendency_len_high = [0]*len(stocknamelist_high)
    tendency_high = [0]*len(stocknamelist_high)
    change_amount_low = [0]*len(stocknamelist_low)
    change_amount_high = [0]*len(stocknamelist_high)
    for i in range(0,len(stocknamelist_low)):
        tendency_len_low[i] = random.randint(1,21)
        tendency_low[i] = random.randint(-20,21)
    for i in range(0,len(stocknamelist_high)):
        tendency_len_high[i] = random.randint(1,21)
        tendency_high[i] = random.randint(-50,51)
    await changestock()
    

@client.event
async def on_message(message):

    global stocknamelist_low
    global stocknamelist_high
    global change_amount_high
    global change_amount_low
    printlog(message.author, message.content)
    if message.author == client.user:
        return
    elif message.content.startswith(tabo_conf.CommandPrefix):
            if message.content.startswith(tabo_conf.CommandPrefix + '공지'):
                servers = list(client.servers)
                role = discord.utils.get(message.server.roles, name="ADMIN")
                if role in [y for y in message.author.roles]:
                    before = message.content
                    splited = before.split(':')
                    em_notice = discord.Embed(title=splited[1], description=splited[2], color=0x7519ff)
                    
                    
                    await client.send_message(discord.Object(splited[3]), embed=em_notice)
                else:
                    await client.send_message(message.channel, ':x:** 권한이 없습니다**\n')
                    
                    
            elif message.content.startswith(tabo_conf.CommandPrefix + '캐시'):
                # /캐시 주기 멘션 금액
                if message.content.startswith(tabo_conf.CommandPrefix + '캐시 주기'):
                    servers = list(client.servers)
                    role = discord.utils.get(message.server.roles, name="ADMIN")
                    if role in [y for y in message.author.roles]:
                        before = message.content
                        splited = before.split()
                        who = splited[2]
                        who = who.replace('<@', '')
                        who = who.replace('>', '')
                        print('who' + who)
                        getmoney(who, int(splited[3]))
                        msguser = message.server.get_member(int(who))
                        em_cash = discord.Embed(title="캐시 지급 됨", description="<@"+ message.author.id + ">" + "님이 \n" + '<@' + who + '>' + "님 에게" +  splited[3] + "캐시를 지급했습니다.", color=0x7519ff)
                        em_cash.set_footer(text="TABO SPACE 관리팀")
                        await client.send_message(message.channel, embed=em_cash)
                    else:
                        await client.send_message(message.channel, ':x:** 권한이 없습니다**\n')
                        
                        
                #캐시 보내기 @Pi 500
                elif message.content.startswith(tabo_conf.CommandPrefix + '캐시 보내기'):
                    servers = list(client.servers)
                    before = message.content
                    splited = before.split()
                    sp = splited[2]
                    sp = sp.replace('<@', '')
                    sp = sp.replace('>', '')
                    usrmoney = getdb(message.author.id, line_money)
                    if 0 > int(splited[3]):
                        await client.send_message(message.channel, ':x: **음수는 송금 할 수 없습니다.**')
                        return
                    if message.author.name == splited[2]:
                        await client.send_message(message.channel, ':x: **자신에게 캐시를 송금할 수 없습니다.**')
                        return
                    if int(usrmoney)-int(splited[3]) >= 0:
                        getmoney(sp, int(splited[3]))
                        getmoney(message.author.id, -int(splited[3]) )
                        em_cash = discord.Embed(title="캐시 송금 됨", description="<@"+ message.author.id + ">" + "님이 " + '<@' + sp + '>' + "님 에게 **" +  splited[3] + "**캐시를 송금했습니다.", color=0x00ff00)
                        #em_cash.set_thumbnail( url="https://avatars2.githubusercontent.com/u/46317549?s=460&v=4")
                        em_cash.set_footer(text="TABO SPACE BANK")
                        await client.send_message(message.channel, embed=em_cash)

                    else:
                        await client.send_message(message.channel, ':x:**' + str(abs(int(usrmoney)-int(splited[3]))) + ' 캐시가 부족합니다.**\n')
                        
            #캐시 @Pi
                elif message.content.startswith(tabo_conf.CommandPrefix + '캐시'):
                    before = message.content
                    splited = before.split()
                    if message.content == '/캐시': 
                        await client.send_message(message.channel, '<@' + message.author.id + '>'+ '님의 돈:' + getdb(message.author.id, line_money))       
                        em_cash = discord.Embed(title= message.author.name + "님의 정보", description='', color=0x00ff00)
                        em_cash.set_footer(text="TABO SPACE 관리팀")
                        embed=discord.Embed(title="TABO SPACE 시즌 12", description=message.author.name + " 님의 TABO SPACE REALISTIC 시즌12 유저 정보입니다.", color=0xad52c6)
                        embed.set_author(name=message.author.name,url="http://google.com", icon_url= message.author.avatar_url)
                        embed.add_field(name='ROLE', value='DOCTOR', inline=True)
                        embed.add_field(name='CREDIT', value=60000000, inline=True)
                        embed.add_field(name='MONEY', value='**' + getdb(message.author.id, line_money) + '**', inline=True)
                        embed.add_field(name='RANKING', value=50, inline=True)
                        await client.send_message(message.channel, embed=embed)
             
                    else:
                        servers = list(client.servers)
                        role = discord.utils.get(message.server.roles, name="STAFF")
                        
                        if role in [y for y in message.author.roles]:
                            msg = splited[1]
                            msg = msg.replace("<@", "")
                            msg = msg.replace(">", "")
                            await client.send_message(message.channel, '<@' + msg + '>' + '님의 돈:' + getdb(msg, line_money))
                        else:
                            await client.send_message(message.channel, ':x:** 권한이 없습니다**\n다른 사람의 캐시는 스탭만 볼 수 있습니다.')

            elif message.content.startswith(tabo_conf.CommandPrefix + '상장'):
                splited = (message.content).split(' ')
                addstock(int(splited[1]), splited[2])
            
            
            elif message.content.startswith(tabo_conf.CommandPrefix + '시세'):
                changestock()
                
                embed=discord.Embed(title='TABO 증권 거래소 - **현재 주식 시세**', color=0xad52c6)
                for i in range(0,len(stocknamelist_low)):
                    chs = ""
                    if change_amount_low[i]>0:
                        chs = "(▲" + str(change_amount_low[i]) + ")"
                    elif change_amount_low[i]<0:
                        chs = "(▼" + str(-change_amount_low[i]) + ")"
                    else:
                        chs = "(-0)"
                    embed.add_field(name='**'+str(list(stocknamelist_low.keys())[i])+'**', value='**' + str(list(stocknamelist_low.values())[i]) +'** COIN' + chs, inline=True)
                for i in range(0,len(stocknamelist_high)):
                    chs = ""
                    if change_amount_high[i]>0:
                        chs = "(▲" + str(change_amount_high[i]) + ")"
                    elif change_amount_high[i]<0:
                        chs = "(▼" + str(-change_amount_high[i]) + ")"
                    else:
                        chs = "(-0)"
                    embed.add_field(name='**'+str(list(stocknamelist_high.keys())[i])+'**', value='**' + str(list(stocknamelist_high.values())[i]) +'** COIN' + chs, inline=True)
                
                waitsec = 300-60*(datetime.datetime.now().timetuple().tm_min%5)-datetime.datetime.now().timetuple().tm_sec
                embed.set_footer(text="다음 변동까지 "+str(int(waitsec/60))+"분 "+str(waitsec%60)+"초")

                await client.send_message(message.channel, embed=embed)
            
            elif message.content.startswith(tabo_conf.CommandPrefix + '매수'):
                mymoney = int(getdb(str(message.author.id), line_money))
                buystr = message.content.split(' ')
                buy_stock = buystr[1]
                buy_amount = int(buystr[2])
                if buy_stock in stocknamelist_low or buy_stock in stocknamelist_high:
                    for i in stocknamelist_low.keys():
                        if i == buy_stock:
                            nowstock = stocknamelist_low[i]
                            if nowstock*buy_amount<=mymoney:
                                mymoney=mymoney-nowstock*buy_amount
                                db(str(message.author.id), line_money, str(mymoney))
                                stockdic = eval(getdb(str(message.author.id), line_stock))
                                if stockdic.get(buy_stock, 0)!=0:
                                    stockdic[buy_stock] = stockdic[buy_stock] + buy_amount
                                else:
                                    stockdic[buy_stock] = buy_amount
                                db(str(message.author.id), line_stock, str(stockdic))
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 매수 요청이 성공적으로 처리되었습니다. ``"+buy_stock+"`` `` "+str(buy_amount)+"``주 구매 / 잔액은 ``"+str(mymoney)+"``COIN입니다.")
                            else:
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 잔액이 부족합니다. 필요한 캐시 : ``"+str(nowstock*buy_amount-mymoney)+"``COIN")
                    for i in stocknamelist_high.keys():
                        if i == buy_stock:
                            nowstock = stocknamelist_high[i]
                            if nowstock*buy_amount<=mymoney:
                                mymoney=mymoney-nowstock*buy_amount
                                db(str(message.author.id), line_money, str(mymoney))
                                stockdic = eval(getdb(str(message.author.id), line_stock))
                                if stockdic.get(buy_stock, 0)!=0:
                                    stockdic[buy_stock] = stockdic[buy_stock] + buy_amount
                                else:
                                    stockdic[buy_stock] = buy_amount
                                db(str(message.author.id), line_stock, str(stockdic))
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 매수 요청이 성공적으로 처리되었습니다. ``"+buy_stock+"`` `` "+str(buy_amount)+"``주 구매 / 잔액은 ``"+str(mymoney)+"``COIN입니다.")
                            else:
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 잔액이 부족합니다. 필요한 캐시:``"+str(nowstock*buy_amount-mymoney)+"``COIN")
                else:
                    await client.send_message(message.channel,  "<@"+str(message.author.id)+"> 해당 이름의 주식은 존재하지 않습니다.")
            
            elif message.content.startswith(tabo_conf.CommandPrefix + '매도'):
                mymoney = int(getdb(str(message.author.id), line_money))
                buystr = message.content.split(' ')
                buy_stock = buystr[1]
                buy_amount = int(buystr[2])
                if buy_stock in stocknamelist_low or buy_stock in stocknamelist_high:
                    for i in stocknamelist_low.keys():
                        if i == buy_stock:
                            nowstock = stocknamelist_low[i]
                            stockdic = eval(getdb(str(message.author.id), line_stock))
                            if stockdic.get(buy_stock, 0)>=buy_amount:
                                mymoney=mymoney+nowstock*buy_amount
                                db(str(message.author.id), line_money, str(mymoney))
                                stockdic[buy_stock] = stockdic[buy_stock] - buy_amount
                                db(str(message.author.id), line_stock, str(stockdic))
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 매도 요청이 성공적으로 처리되었습니다. ``"+buy_stock+"`` `` "+str(buy_amount)+"``주 판매 / 잔액은 ``"+str(mymoney)+"``COIN입니다.")
                            else:
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 잔고가 부족합니다. 부족한 잔고 : ``"+str(buy_amount-stockdic.get(buy_stock,0))+"``주")
                    for i in stocknamelist_high.keys():
                        if i == buy_stock:
                            nowstock = stocknamelist_high[i]
                            stockdic = eval(getdb(str(message.author.id), line_stock))
                            if stockdic.get(buy_stock, 0)>=buy_amount:
                                mymoney=mymoney+nowstock*buy_amount
                                db(str(message.author.id), line_money, str(mymoney))
                                stockdic[buy_stock] = stockdic[buy_stock] - buy_amount
                                db(str(message.author.id), line_stock, str(stockdic))
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 매도 요청이 성공적으로 처리되었습니다. ``"+buy_stock+"`` `` "+str(buy_amount)+"``주 판매 / 잔액은 ``"+str(mymoney)+"``COIN입니다.")
                            else:
                                await client.send_message(message.channel, "<@"+str(message.author.id)+"> 잔고가 부족합니다. 부족한 잔고 : ``"+str(buy_amount-stockdic[buy_stock])+"``주")
                else:
                    await client.send_message(message.channel,  "<@"+str(message.author.id)+"> 해당 이름의 주식은 존재하지 않습니다.")
                    
            elif message.content.startswith(tabo_conf.CommandPrefix + '잔고'):
                stockinmyaccount = getdb(str(message.author.id), line_stock)
                moneyinmyaccount = getdb(str(message.author.id), line_money)
                await client.send_message(message.channel, "캐시 : ``"+moneyinmyaccount+"``\n주식 : "+stockinmyaccount)
                            

            elif message.content.startswith(tabo_conf.CommandPrefix + '<@'):
                dsserver = message.server
                msg = message.content
                msg = msg.replace("<@", "")
                msg = msg.replace(">", "")
                await client.send_message(dsserver.get_member(int(msg)), )
                
            elif message.content.startswith(tabo_conf.CommandPrefix + '튜토리얼'):
                await client.send_message(message.author, '튜토리얼 예제입니다.')
                
            elif message.content.startswith(tabo_conf.CommandPrefix + '시작하기'):
                servers = list(client.servers)
                shutil.copy(os.getcwd() + '/bin/example_usr.txt', os.getcwd() + '/bin/usr/' + message.author.id + '.txt')
                printlog('SYSTEM', message.author.name + '에게 USER 권한이 성공적으로 부여되었습니다.')
                user = discord.utils.get(servers[0].members, name=message.author.name)
                role = discord.utils.get(servers[0].roles, name="1:USER")
                await client.send_message(message.author, '**TABO SPACE에 오신걸 진심으로 환영합니다!!**\n이제 TABO SPACE의 모든 기능을 이용할 수 있답니다 :)')
                await client.add_roles(user, role)
                
                
@client.event
async def on_message_edit(before, after):
    printlog(after.author, '(수정) ' + after.content)
                
@client.event
async def on_member_join(member):
    if os.path.exists(os.getcwd() + '/bin/usr/' + member.id + '.txt'):
        await client.send_message(member, ":yellowtabo: TABO SPACE에 다시 오신걸 환영합니다!\n전에 TABO SPACE를 이용해보신적이 있다고 조회되는데, 그래도 튜토리얼과 함께 시작하시려면 /튜토리얼 을,\n건너뛰고 바로 시작하시려면 /시작하기 를 저에게 전송해주세요!")
    else:
        await client.send_message(member, ":yellowtabo: TABO SPACE에 오신걸 환영합니다!\n튜토리얼과 함께 시작하시려면 /튜토리얼 을,\n건너뛰고 바로 시작하시려면 /시작하기 를 저에게 전송해주세요!")
    printlog(member, member + '멤버가 서버에 입장했습니다.')

#******************************************************************************


client.run(tabo_conf.Token)
