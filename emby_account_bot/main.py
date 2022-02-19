#coding:utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,ConversationHandler
import requests
from urllib import parse
import logging
import random,string
import time

eemm=0





CHOOSING, COMFIRM_STOCK, TYPING_CHOICE = range(3)
def start(update, context):
    update.message.reply_text('Hi!')
    

def help(update, context):
	update.message.reply_text('请输入要设置账号！')
	return CHOOSING
	
def emby(update, context):
    global eemm
    tg = False
    with open('./tgid.txt', 'r', encoding="utf-8") as f:
        for line in f:
            if str(update.message.chat_id) in line:
                tg = True

    if tg:
        update.message.reply_text("请不要重复注册！")
    else:
        url = "http://***.***.***:8080/emby/Users/New?X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=b0bfda68-da22-429b-8d72-0133af546121&X-Emby-Client-Version=4.6.4.0&X-Emby-Token=1cd77e46280247b799319fc3e9209619"
        data = {
            "Name": str(update.message.text)
        }
        res = requests.post(url, data)

        if "already" in res.text:
            update.message.reply_text('注册失败请联系管理员！')
        elif eemm >= 20:
            update.message.reply_text('本次注册已结束！')
        else:
            update.message.reply_text(
                '注册成功!\n账号：{0}\n密码：没有密码请自行设置密码\n服务器地址：\nhttp://***.***.***:8080\ncf中转地址：\nhttp://***.***.***:8080\n请注意不要分享账号与服务器地址！'.format(
                    update.message.text))
            file = open("./tgid.txt", "a")
            file.write(str(update.message.chat_id) + '\n')
            file.close()
            eemm += 1

    return ConversationHandler.END

def echo(update, context):
    print(update.message.text)
    update.message.reply_text(update.message.text)

def error(update, context):
    logging.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == '__main__':
    updater = Updater('TGBOTTOKEN', use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('emby', help)],
        states={
            CHOOSING:[
            	MessageHandler(Filters.text & ~Filters.command, emby)
            	
            	]
        },
        fallbacks = [CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
