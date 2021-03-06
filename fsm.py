from transitions.extensions import GraphMachine
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction
# from utils import send_button_message,send_text_message,send_fsm
from utils import *

class TocMachine(GraphMachine):
    breakfast = {'calorie':0,'starch':0,'protein':0,'money':0,'meal':'none'} #starch:澱粉
    lunch     = {'calorie':0,'starch':0,'protein':0,'money':0,'meal':'none'}   
    dinner    = {'calorie':0,'starch':0,'protein':0,'money':0,'meal':'none'}
    height = 160
    weight = 60
    Totalmoney = 0
    Totalcalorie = 0
    Totalstarch = 0
    Totalprotein = 0
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    #start
    def is_going_to_start(self, event):
        text = event.message.text
        return text.lower() == "start"
    def on_enter_start(self, event):
        TocMachine.breakfast['calorie'] = 0
        TocMachine.breakfast['starch'] = 0
        TocMachine.breakfast['protein'] = 0
        TocMachine.breakfast['money'] = 0
        TocMachine.breakfast['meal'] = 'none'
        
        TocMachine.lunch['calorie'] = 0
        TocMachine.lunch['starch'] = 0
        TocMachine.lunch['protein'] = 0
        TocMachine.lunch['money'] = 0
        TocMachine.lunch['meal'] = 'none'
        
        TocMachine.dinner['calorie'] = 0
        TocMachine.dinner['starch'] = 0
        TocMachine.dinner['protein'] = 0
        TocMachine.dinner['money'] = 0
        TocMachine.dinner['meal'] = 'none'
        
        btn_action=[
            MessageTemplateAction(
                label='設定個人資訊',
                text='modified information'
            ),
            MessageTemplateAction(
                label='分析早/午/晚餐營養指標',
                text='check nutrition'
            ),
            MessageTemplateAction(
                label='建議營養比例',
                text='show suggestion'
            ),
            MessageTemplateAction(
                label='show FSM',
                text='show fsm'
            ),
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"功能表單","提供以下功能")

    #input the food
    def is_going_to_checknutrition(self, event):
        text = event.message.text
        return text.lower() == "check nutrition"
    def on_enter_checknutrition(self, event):
        btn_action=[
            MessageTemplateAction(
                label='早餐',
                text='breakfast'
            ),
            MessageTemplateAction(
                label='午餐',
                text='lunch'
            ),
            MessageTemplateAction(
                label='晚餐',
                text='dinner'
            ),
            MessageTemplateAction(
                label='顯示您的攝取資訊',
                text='show nutrition'
            ),
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"選擇餐點","返回功能選單請輸入return")
    
    #input the information
    def is_going_to_information(self, event):
        text = event.message.text
        if(text.lower() == "start" or text.lower() == "modified information"):
            return True
        else:
            return False
        # return text.lower() == "information"
    def on_enter_information(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Welcome!\n******請先輸入基本資訊******\n\n輸入身高(cm)")
    #input the height
    def is_going_to_height(self, event):
        text = event.message.text
        return True
    def on_enter_height(self, event):
        print("in height")
        text = event.message.text
        TocMachine.height = int(text)
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入體重(kg)")
    #input the weight
    def is_going_to_weight(self, event):
        text = event.message.text
        return True
    def on_enter_weight(self, event):
        text = event.message.text
        TocMachine.weight = int(text)
        print("in weight")
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入預算(dollar)")

    #input the money
    def is_going_to_money(self, event):
        text = event.message.text
        return True
    def on_enter_money(self, event):
        text = event.message.text
        TocMachine.Totalmoney = int(text)
        print("in money")
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入年齡")
    #input the age
    def is_going_to_age(self, event):
        text = event.message.text
        return True
    def on_enter_age(self, event):
        text = event.message.text
        TocMachine.age = int(text)
        # bmr = (13.7 x 體重) + (5.0 x 身高) – (6.8 x 年齡) + 66
        bmr = (13.7*TocMachine.weight) + (5*TocMachine.height) - (6.8*TocMachine.age) + 66
        tdee = bmr * 1.375 - 300
        TocMachine.Totalstarch = tdee * 0.3/4 #starch=tdee*0.3/4
        TocMachine.Totalcalorie = tdee
        TocMachine.Totalprotein = TocMachine.weight #(1 kg need 1g protein)
        print(TocMachine.Totalmoney,"totalmoney")
        print(tdee,'tdee')
        print(TocMachine.Totalcalorie,"Totalcalorie")
        print(TocMachine.Totalstarch,"Totalstarch")
        print(TocMachine.Totalprotein,"Totalprotein")
        self.go_backtostart(event)

    #check
    def on_enter_examine(self, event, strback):
        print("in examine")
        print(strback)
        self.go_money(event,strback)
    
    def on_enter_money_check(self, event, strback):
        print("in money check")
        sum = TocMachine.dinner['money'] +TocMachine.breakfast['money'] + TocMachine.lunch['money'] 
        print(TocMachine.breakfast['money'],"breakfast")
        print(TocMachine.lunch['money'],"lunch")
        print(TocMachine.dinner['money'],"dinner")
        print(sum,"sum = ")
        if sum <= TocMachine.Totalmoney:
            self.go_calorie(event,strback)
        else:
            self.go_money_deny(event,strback,sum)

    def on_enter_calorie_check(self, event,strback):
        print("in calorie check")
        sum = TocMachine.dinner['calorie'] + TocMachine.breakfast['calorie'] + TocMachine.lunch['calorie'] 
        print(TocMachine.breakfast['calorie'],"breakfast")
        print(TocMachine.lunch['calorie'],"lunch")
        print(TocMachine.dinner['calorie'],"dinner")
        print(sum,"sum = ")

        if sum < TocMachine.Totalcalorie:
            self.go_starch(event,strback)
        else:
            self.go_calorie_deny(event,strback,sum)
        
    def on_enter_starch_check(self, event,strback):
        print("in starch check")
        sum = TocMachine.dinner['starch'] +TocMachine.breakfast['starch'] + TocMachine.lunch['starch'] 
        print(TocMachine.breakfast['starch'],"breakfast")
        print(TocMachine.lunch['starch'],"lunch")
        print(TocMachine.dinner['starch'],"dinner")
        print(sum,"sum = ")
        if sum < TocMachine.Totalstarch:
            self.go_protein(event,strback)
        else:
            self.go_starch_deny(event,strback,sum)

    def on_enter_protein_check(self, event,strback):
        print("in protein check")
        sum = TocMachine.dinner['protein'] +TocMachine.breakfast['protein'] + TocMachine.lunch['protein'] 
        print(TocMachine.breakfast['protein'],"breakfast")
        print(TocMachine.lunch['protein'],"lunch")
        print(TocMachine.dinner['protein'],"dinner")
        print(sum,"sum = ")
        if sum < TocMachine.Totalprotein:
            self.go_checknutrition(event)
        else:
            self.go_protein_deny(event,strback,sum)
    
    #deny
    def on_enter_money_deny(self, event, strback,sum):
        reply_token = event.reply_token
        msg0="餘額不足\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in money deny")
        
        if strback == "breakfast":
            sum -= TocMachine.breakfast['money']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['money']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['money']
            self.go_checknutrition(event)
        
    def on_enter_calorie_deny(self, event,strback,sum):
        reply_token = event.reply_token
        msg0="熱量太高\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in calorie deny")
        if strback == "breakfast":
            sum -= TocMachine.breakfast['calorie']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['calorie']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['calorie']
            self.go_checknutrition(event)
        
    def on_enter_starch_deny(self, event,strback,sum):
        reply_token = event.reply_token
        msg0="澱粉太多\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in starch deny")

        if strback == "breakfast":
            sum -= TocMachine.breakfast['starch']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['starch']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['starch']
            self.go_checknutrition(event)

    def on_enter_protein_deny(self, event,strback,sum):
        reply_token = event.reply_token
        msg0="蛋白質太多\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in protein deny")

        if strback == "breakfast":
            sum -= TocMachine.breakfast['protein']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['protein']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['protein']
            self.go_checknutrition(event)
 
    #showconsume
    def is_going_to_showconsume(self, event,indic=""):
        text = event.message.text
        return text.lower() == "show nutrition"
    def on_enter_showconsume(self, event ,indic=""):  
        msg0='早餐:\n'
        msg1='餐點:   %10s\n' % TocMachine.breakfast['meal']
        msg2='卡路里:      %d大卡\n'% TocMachine.breakfast['calorie'] 
        msg3='澱粉:          %d克\n'% TocMachine.breakfast['starch']
        msg4='蛋白質:      %d克\n'% TocMachine.breakfast['protein']
        msg5='金額:          %d元\n'% TocMachine.breakfast['money']
        
        msg6='\n午餐:\n'
        msg7='餐點:   %10s\n' % TocMachine.lunch['meal']
        msg8='卡路里:      %d大卡\n'% TocMachine.lunch['calorie'] 
        msg9='澱粉:          %d克\n'% TocMachine.lunch['starch']
        msg10='蛋白質:      %d克\n'% TocMachine.lunch['protein']
        msg11='金額:          %d元\n'% TocMachine.lunch['money']

        msg12='\n晚餐:\n'
        msg13='餐點:   %10s\n' % TocMachine.dinner['meal']
        msg14='卡路里:      %d大卡\n'% TocMachine.dinner['calorie'] 
        msg15='澱粉:          %d克\n'% TocMachine.dinner['starch']
        msg16='蛋白質:      %d克\n'% TocMachine.dinner['protein']
        msg17='金額:          %d元\n\n'% TocMachine.dinner['money']

        msg23='================\n'
        msg18='總卡路里:  %d大卡\n' % (TocMachine.breakfast['calorie']+TocMachine.lunch['calorie']+TocMachine.dinner['calorie'])
        msg19='總澱粉:      %d克\n'% (TocMachine.breakfast['starch']+TocMachine.lunch['starch']+TocMachine.dinner['starch'])
        msg20='總蛋白質:  %d克\n' % (TocMachine.breakfast['protein']+TocMachine.lunch['protein']+TocMachine.dinner['protein'])
        msg21='總金額:      %d元\n\n' % (TocMachine.breakfast['money']+TocMachine.lunch['money']+TocMachine.dinner['money'])

        msg22 = '返回請輸入return'
        reply_token = event.reply_token
        send_text_message(reply_token,msg0+msg1+msg2+msg3+msg4+msg5+msg6+msg7+msg8+msg9+msg10+msg11+msg12+msg13+msg14+msg15+msg16+msg17+msg23+msg18+msg19+msg20+msg21+msg22)
    #show back
    def is_going_to_showback(self, event,indic=""):
        text = event.message.text
        return text.lower() == "return"
    def on_enter_showback(self, event ,indic=""):  
        self.go_checknutrition(event)

    #showsuggest
    def is_going_to_showsuggest(self, event,indic=""):
        text = event.message.text
        return text.lower() == "show suggestion"
    def on_enter_showsuggest(self, event ,indic=""):
        print("in show suggest")  
        print(TocMachine.Totalmoney,"totalmoney")
        print(TocMachine.Totalcalorie,"Totalcalorie")
        print(TocMachine.Totalstarch,"Totalstarch")
        print(TocMachine.Totalprotein,"Totalprotein")
        
        #msg0 = '設定完身高體重即可換算\n\n'
        msg1 = '建議攝取熱量:%20d大卡\n' % (TocMachine.Totalcalorie)
        msg2 = '建議攝取澱粉:%20d公克\n' % (TocMachine.Totalstarch)
        msg3 = '建議攝取蛋白質:%15d公克\n' % (TocMachine.Totalprotein)
        msg4 = '每日金額:         %20d元\n\n' % (TocMachine.Totalmoney)
        msg5 = '返回請輸入return'
        reply_token = event.reply_token
        send_text_message(reply_token,msg1+msg2+msg3+msg4+msg5)
    
    #showfsm
    def is_going_to_showfsm(self, event,indic=""):
        text = event.message.text
        return text.lower() == "show fsm"

    def on_enter_showfsm(self, event ,indic=""):
        reply_token = event.reply_token
        send_fsm(reply_token)

    #checknutrition back to start
    def is_going_to_backtostart(self, event,indic=""):
        text = event.message.text
        reply_token = event.reply_token
        if text.lower() != "return":
            send_text_message(reply_token,"輸入return回到上一個階段")
        return text.lower() == "return"
    def on_enter_backtostart(self, event ,indic=""):  
        print(" go to start")
        self.go_backtostart(event)
    
    #breakfast
    def is_going_to_breakfast(self, event,indic=""):
        text = event.message.text
        return text.lower() == "breakfast"
    def on_enter_breakfast(self, event ,indic=""):
        btn_action=[
            MessageTemplateAction(
                label='三明治($15)',
                text='sandwitch'
            ),
            MessageTemplateAction(
                label='蛋餅($20)',
                text='chiomelet'
            ),
            MessageTemplateAction(
                label='飯糰($35)',
                text='riceball'
            ),
            MessageTemplateAction(
                label='漢堡($55)',
                text='hamburger'
            ),
        ]
        
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"早餐",indic)

    #next breakfast
    def is_going_to_nextbreakfast(self, event):
        text = event.message.text
        return True
    def on_enter_nextbreakfast(self, event):
        text = event.message.text
        input = text.split()
        #print(event.message.text)
        print(input)

        if event.message.text == 'sandwitch':
            TocMachine.breakfast['calorie'] = 270
            TocMachine.breakfast['starch']  = 20
            TocMachine.breakfast['protein'] = 13
            TocMachine.breakfast['money']   = 15
            TocMachine.breakfast['meal'] = '三明治'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in sandwitch")
            
        elif event.message.text == 'chiomelet':
            TocMachine.breakfast['calorie'] = 230
            TocMachine.breakfast['starch']  = 25
            TocMachine.breakfast['protein'] = 6
            TocMachine.breakfast['money']   = 20
            TocMachine.breakfast['meal'] = '蛋餅'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in chiomelet")

        elif event.message.text == 'riceball':
            TocMachine.breakfast['calorie'] = 220
            TocMachine.breakfast['starch']  = 40
            TocMachine.breakfast['protein'] = 5
            TocMachine.breakfast['money']   = 35
            TocMachine.breakfast['meal'] = '飯糰'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in riceball")

        elif event.message.text == 'hamburger':
            TocMachine.breakfast['calorie'] = 230
            TocMachine.breakfast['starch']  = 38
            TocMachine.breakfast['protein'] = 15
            TocMachine.breakfast['money']   = 55
            TocMachine.breakfast['meal'] = '漢堡'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in hamburger")

        self.go_money(event,"breakfast")

    #lunch
    def is_going_to_lunch(self, event):
        text = event.message.text
        return text.lower() == "lunch"
    def on_enter_lunch(self, event,indic=""):
        btn_action=[
            MessageTemplateAction(
                label='豬排丼飯($90)',
                text='Katsudon'
            ),
            MessageTemplateAction(
                label='炒飯($65)',
                text='friedrice'
            ),
            MessageTemplateAction(
                label='乾麵($40)',
                text='noodles'
            ),
            MessageTemplateAction(
                label='雞腿便當($65)',
                text='chicken boxedlunch'
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"午餐",indic)
    #next lunch
    def is_going_to_nextlunch(self, event):
        text = event.message.text
        return True
    def on_enter_nextlunch(self, event):
        text = event.message.text
        input = text.split()
        print(input)
        if event.message.text == 'Katsudon':
            TocMachine.lunch['calorie'] = 500
            TocMachine.lunch['starch']  = 55
            TocMachine.lunch['protein'] = 35
            TocMachine.lunch['money']   = 90
            TocMachine.lunch['meal'] = '豬排丼飯'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in Katsudon")
        elif event.message.text == 'friedrice':
            TocMachine.lunch['calorie'] = 600
            TocMachine.lunch['starch']  = 80
            TocMachine.lunch['protein'] = 10
            TocMachine.lunch['money'] = 65
            TocMachine.lunch['meal'] = '炒飯'
            
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in friedrice")

        elif event.message.text == 'noodles':
            TocMachine.lunch['calorie'] = 600
            TocMachine.lunch['starch']  = 60
            TocMachine.lunch['protein'] = 10
            TocMachine.lunch['money']   = 40
            TocMachine.lunch['meal'] = '乾麵'
            
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in noodles")
        elif event.message.text == 'chicken boxedlunch':
            TocMachine.lunch['calorie'] = 800
            TocMachine.lunch['starch']  = 80
            TocMachine.lunch['protein'] = 40
            TocMachine.lunch['money']   = 65
            TocMachine.lunch['meal'] = '雞腿便當'
            
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in chicken boxedlunch")
        self.go_money(event,"lunch")
    
    #dinner
    def is_going_to_dinner(self, event):
        text = event.message.text        
        return text.lower() == "dinner"
    def on_enter_dinner(self, event,indic=""):
        btn_action=[
            MessageTemplateAction(
                label='壽司餐盒($75)',
                text= 'sushi'
            ),
            MessageTemplateAction(
                label='關東煮($70)',
                text='oden'
            ),
            MessageTemplateAction(
                label='火鍋($100)',
                text='hot pot'
            ),
            MessageTemplateAction(
                label='咖哩飯($80)',
                text='Curry rice'
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"晚餐",indic)
    #next dinner
    def is_going_to_nextdinner(self, event):
        text = event.message.text
        return True
    def on_enter_nextdinner(self, event):
        text = event.message.text
        input = text.split()
        print(input)
        # print(text,"check the nextdinner")
        if event.message.text == 'sushi':
            TocMachine.dinner['calorie'] = 800
            TocMachine.dinner['starch']  = 80
            TocMachine.dinner['protein'] = 50

            TocMachine.dinner['money']   = 75
            TocMachine.dinner['meal'] = '壽司餐盒'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in sushi")
        elif event.message.text == 'oden':
            TocMachine.dinner['calorie'] = 800
            TocMachine.dinner['starch']  = 90
            TocMachine.dinner['protein'] = 30
            TocMachine.dinner['money']   = 70
            TocMachine.dinner['meal'] = '關東煮'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in oden")

        elif event.message.text == 'hot pot':
            TocMachine.dinner['calorie'] = 1000
            TocMachine.dinner['starch']  = 100
            TocMachine.dinner['protein'] = 75
            TocMachine.dinner['money']   = 100
            TocMachine.dinner['meal'] = '火鍋'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in hot pot")
        elif event.message.text == 'Curry rice':
            TocMachine.dinner['calorie'] = 600
            TocMachine.dinner['starch']  = 90
            TocMachine.dinner['protein'] = 30
            TocMachine.dinner['money']   = 80
            TocMachine.dinner['meal'] = '咖哩飯'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in Curry rice")
        self.go_money(event,"dinner")