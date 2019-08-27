import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters, BaseFilter
from logger import *
import os, re
import pytesseract as ocr

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import numpy as np
import cv2

from PIL import Image
import PIL.Image


logger.setLevel(logging.DEBUG)

updater = Updater('738462155:AAEE7qRqDnvW0GjQuF-la9GJXgd8t7Mc1oc')

def start(bot, update):
    update.message.reply_text(
        'Ola {}, bem-vindo ao bot Forex Lets! '.format(update.message.from_user.first_name))

updater.dispatcher.add_handler(CommandHandler('start', start))


def photo_handler(bot, update):

    file_name = (str(update.channel_post.photo[-1].file_id)+".jpg")
    file = bot.getFile(update.channel_post.photo[-1].file_id)
    print ("file_id: " + file_name)
    file.download("photo" + file_name)

    y=15
    x=15
    h=180
    w=310

    #image profx signal
    img = cv2.imread("photo" +file_name,0)
    height, width = img.shape
    phrase = ocr.image_to_string(Image.open("photo" +file_name))
    text = phrase.encode('UTF-8')
    if width < 500 and update.channel_post.caption == None and hasattr(update.channel_post.forward_from_chat, 'id') is False :

        crop_img = img[y:y+h, x:x+w]
        cv2.imwrite("photo" +file_name,crop_img)
        phrase = ocr.image_to_string(Image.open("photo" +file_name))
        text = phrase.encode('UTF-8')
        #canal ProfxSiganlChannelTranscritor
        bot.send_message(chat_id='-1001341954636', text=text)
        #canal lets call
        bot.send_message(chat_id='-1001281523650', text=text)
        os.remove("photo" +file_name)

    #imagem FXPROFIT 30pips numeros lado esquerdo na imagem
    #if do id do canal forwared original da img
    elif width > 800 and text.find('@@ FX PROM') != -1 and hasattr(update.channel_post.forward_from_chat, 'id') is True and  update.channel_post.forward_from_chat.id == -1001372654761 and update.channel_post.caption == None:
        y=15
        x=380
        h=564
        w=1000
        crop_img = img[y:y+h, x:x+w]
        cv2.imwrite("photo" +file_name,crop_img)
        phrase = ocr.image_to_string(Image.open("photo" +file_name))
        text = phrase.encode('UTF-8')
        text = text.replace('nll','')
        text = text.replace('[','')
        text = text.replace('SI','SL')
        text = text.replace('Si', 'SL')

        #canal 30pipsChannelTranscritor
        bot.send_message(chat_id='-1001433807742', text=text)
        #canal lets call
        bot.send_message(chat_id='-1001281523650', text=text)
        os.remove("photo" +file_name)

    #imagem com caption e da FXPROFIT 30pips com numero lado direito da img
    else:

        text = phrase.encode('UTF-8')
        text = text.replace('Si','SL')
        text = text.replace('1:','TP:')
        text = text.replace('@uil','')
        text = text.replace('@ul','')
        text = text.replace('@il','')
        text = text.replace('@@ FX PROM','')
        text = text.replace('oe mip.','')
        text = text.replace('S111 (Sb 5051','')
        text = text.replace('WZ','')
        text = text.replace('VAS','')
        text = text.replace('l','')
        text = text.replace('Mall','')
        text = text.replace('@in','')
        text = text.replace('@ai','')
        text = text.replace('@uin','')
        text = text.replace('Se','Sell')
        text = text.replace('None','')
        text = text.replace('Ores','')
        text = text.replace('S:','SL:')
        text = text.replace('"<1:','TP:')
        text = text.replace('<1:','TP:')
        text = re.sub("\@+", '',text)


        logger.info("file %s", str(update.channel_post.photo))
        #if do id do canal forwared original da img
        if update.channel_post.caption == None and hasattr(update.channel_post.forward_from_chat, 'id') is True and  update.channel_post.forward_from_chat.id == -1001372654761:
                #canal 30pipsCHannelTranscritor
                bot.send_message(chat_id='-1001433807742', text=text)
                #canal lets call
                bot.send_message(chat_id='-1001281523650', text=text)
                os.remove("photo" +file_name)
        if update.channel_post.caption != None and hasattr(update.channel_post.forward_from_chat, 'id') is True and update.channel_post.forward_from_chat.id == -1001222448337:
                text = text.replace('mz','')
                text = text.replace('i we','')
                #canal M15ChannelTranscritor
                bot.send_message(chat_id='-1001185996952', text=text+update.channel_post.caption)
                #canal lets call
                bot.send_message(chat_id='-1001281523650', text=text+update.channel_post.caption)

                os.remove("photo" +file_name)

updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

#def reply(bot, update):
#    update.message.reply_text(
#        '{}'.format(update.message.text))



#updater.dispatcher.add_handler(MessageHandler(Filters.forwarded, reply))

updater.start_polling()
updater.idle()
