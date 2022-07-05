from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from tg_response import response
from uuid import uuid4
import logging

# api
API_KEY = ''

start_text = '''سلام 👋 من یک ربات برای دریافت لیست کلاس ها هستم که به صورت آزمایشی ساخته شدم.برای ادامه کد درس را ارسال کنید.
برای دیدن راهنما /help را ارسال کنید.'''

help_text = '''کد درس یک عدد ۷ رقمی می باشد ، برای دریافت اطلاعات مربوط به کلاس لازم است کد درس را به صورت صحیح ارسال کنید.
توجه داشته باشید که دیتای این ربات به صورت افلاین و با استفاده از web scarping از سایت اصلی در بازه های زمانی متفاوت جمع آوری شده است بنابراین ممکن است برنامه زمانی کلاس ها متغییر باشد.
مشارکت در توسعه : https://github.com/MeysamNaghavi/orsun
@Meysam_ngv'''

# log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot ... ')


def start_command(update, context):
    update.message.reply_text(start_text)


def help_command(update, context):
    update.message.reply_text(help_text)


def handle_message(update, context):
    text = update.message.text
    logging.info(f'user ({update.message.chat.id}) says : {text}')
    # bot response
    meetings = response.get_response(text)
    if meetings is False:
        update.message.reply_text('خطا: کد درس یا فرمت وارد شده صحیح نمی باشد')
    elif meetings is None:
        update.message.reply_text('موردی یافت نشد')
    else:
        for item in meetings:
            print('test')
            meetings_text = ''
            meetings_text += f"✅ درس : {item.get('classroom_name')}\n"
            meetings_text += f"🧑‍🏫 استاد : {item.get('teacher')}\n"
            meetings_text += f"🔄 تعداد جلسات : {len(item.get('meetings'))}\n"
            for j in item['meetings']:
                meetings_text += f"{j[0]} در ساعت {j[1]}\n"
            update.message.reply_text(meetings_text)


# def inlinequery(update, context: CallbackContext):
#     query = update.inline_query.query
#     meetings = response.get_response(query)
#     if meetings is False:
#         update.inline_query.answer('خطا: کد درس یا فرمت وارد شده صحیح نمی باشد')
#     elif meetings is None:
#         update.inline_query.answer('موردی یافت نشد')
#     else:
#         for item in meetings:
#             meetings_text = ''
#             meetings_text += f"✅ درس : {item.get('classroom_name')}\n"
#             meetings_text += f"🧑‍🏫 استاد : {item.get('teacher')}\n"
#             meetings_text += f"🔄 تعداد جلسات : {len(item.get('meetings'))}\n"
#             for j in item['meetings']:
#                 meetings_text += f"{j[0]} در ساعت {j[1]}\n"
#             results = [
#                 InlineQueryResultArticle(
#                     id=str(uuid4()),
#                     title="🔍 جستوجوی جلسات برای این درس",
#                     # description='example 1322008',
#                     input_message_content=InputTextMessageContent(meetings_text))
#             ]
#             update.inline_query.answer(results)


def error(update, context):
    # error Logs
    logging.error(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # comments
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    # messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all error
    dp.add_error_handler(error)

    # for inline message
    # dp.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling(drop_pending_updates=True)
    updater.idle()
