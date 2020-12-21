
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from antlr4 import *
import os
import sys
import inspect
current_dir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from cl.EvalVisitor import EvalVisitor
from cl.PolyBotParser import PolyBotParser
from cl.PolyBotLexer import PolyBotLexer
from polygons import Point, ConvexPolygon, WrongArgumentException



# defineix una funció que saluda i que s'executarà quan el bot rebi el
# missatge /start
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola! Soc un bot bàsic.")


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
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

# engega el bot
updater.start_polling()
