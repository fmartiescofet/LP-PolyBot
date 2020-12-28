
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import sys
from antlr4 import *

try:
    from ..polygons import *
except:
    sys.path.append('..')
    from polygons import Point, ConvexPolygon, WrongArgumentException
    from cl.EvalVisitor import EvalVisitor
    from cl.PolyBotParser import PolyBotParser
    from cl.PolyBotLexer import PolyBotLexer


def lst(update,context):
    if 'symbols' not in context.user_data or not context.user_data['symbols']:
        lst_text = "There are no defined polygons"
    else:
        lst_text = ""
        for polygon in context.user_data['symbols'].items():
            lst_text += polygon[0] + " := [" + ' '.join(map(str,polygon[1].points)) + "]\n"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=lst_text)

def clean(update,context):
    context.user_data['symbols'] = {}
    context.bot.send_message(chat_id=update.effective_chat.id, text="Deleted all identifiers")


def start(update, context):
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi " + name + "! Welcome to PolyBot!")

def author(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text="PolyBot\nFrancesc Martí Escofet, 2020\nfrancesc.marti.escofet@estudiantat.upc.edu")

def help(update,context):
    help_text = """
*Commands*
`/start` - Welcome message
`/author` - Information about the author
`/help` - Shows list of commands
`/lst` - Display list of defined polygons
`/clean` - Delete all defined polygons
Any possible command line defined in the README file
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode=telegram.ParseMode.MARKDOWN)


    

def message_handler(update, context):
    try:
        input_stream = InputStream(update.message.text)
        lexer = PolyBotLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = PolyBotParser(token_stream)
        tree = parser.root()
        if 'symbols' not in context.user_data:
            context.user_data['symbols'] = {}
        evalV = EvalVisitor(context.user_data['symbols'])
        context.user_data['symbols'], text, files = evalV.visit(tree)

        for img in files:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=open(
                    img,
                    'rb'))
            os.remove(img)
        if text != '':
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=text)
    except WrongArgumentException as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error: " + str(e))


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('lst', lst))
dispatcher.add_handler(CommandHandler('clean', clean))


dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

# engega el bot
updater.start_polling()
