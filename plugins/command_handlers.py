# (c) AlenPaulVarghese
# -*- coding: utf-8 -*-

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from pyrogram import (
    Client,
    filters
)
from plugins.logger import logging  # pylint:disable=import-error
import os

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(10)

BLACKLIST = ['drive.google.com', 'tor.checker.in', 'youtube.com', 'youtu.be']
HOME = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='صيغة - PDF', callback_data='format')],
            [InlineKeyboardButton(text='نوع الصفحة-كاملة', callback_data="page")],
            # [InlineKeyboardButton(text='Landscape', callback_data="orientation")],
            [InlineKeyboardButton(text='رؤية الإعدادات الإضافية ˅', callback_data="options")],
            [InlineKeyboardButton(text='▫️ يلاااا بلش شغل عموو😡▫️', callback_data="render")],
            [InlineKeyboardButton(text='غيرت رأيي  بدي الغي🙂', callback_data="cancel")]
                            ])


@Client.on_message(filters.command(["start"]))
async def start(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /start command >> @{message.from_user.username}")
    await message.reply_text(
        f"<b>هلووو {message.from_user.first_name} 👋\n"
        "أناا ابنو لهاد البوت الذكي @Sy404_bot 🙂🙂 فيني حولك أي رابط صفحة انترنت بتعطيني ياه لملف *كتاب إلكتروني PDF* أو لصورة 😌😌😌 .. معلش فوت واشكر المطور من هون @Mr00lucifer مع انو مابيستاهل</b>",
        quote=True,
        reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❓ مين نحن", callback_data="about_cb")
            ]
        ])
    )


@Client.on_message(filters.command(["about", 'feedback']))
async def feedback(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /about command >> @{message.from_user.username}")
    await message.reply_text(
        text="نحن منشتغل لحتى نكون مصدر معلومة مهمة الك او نساعدك سواء ع صفحتنا أو من خلال سكربتاتنا ع التيليجرام❤️",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👨🏻‍🦯 صفحتنا المفيدة", url="https://www.facebook.com/solu404tion/"),
                InlineKeyboardButton("حساب المطور فيسبوك🙈", url="https://www.facebook.com/mohammedsjnoube")],
            [InlineKeyboardButton(
                "🌃 البوت الرئيسي ل حلول 404",
                url="https://t.me/Sy404_bot")]
            ])
    )


@Client.on_message(filters.command(["delete"]) & filters.private)
async def delete(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /delete command >> @{message.from_user.username}")
    try:
        sudo_user = int(os.environ["SUDO_USER"])
    except Exception:
        LOGGER.debug('DEL__CMD --> status failed >> user not a sudo')
        return
    if message.from_user.id == sudo_user:
        random_message = await message.reply_text('Processing')
        LOGGER.debug('DEL__CMD --> status pending >> sudo user found processing')
        if os.path.isdir('./FILES/'):
            with open('walk.txt', 'w') as writer:
                for root, dirs, files in os.walk('./FILES/', topdown=False):
                    writer.write(str(root)+'\n\n'+str(dirs)+'\n\n'+str(files))
            if os.path.isfile('walk.txt'):
                LOGGER.debug('DEL__CMD --> status pending >> sending file')
                await message.reply_document(
                    document='walk.txt',
                )
                await random_message.delete()
                os.remove('walk.txt')
                LOGGER.debug('DEL__CMD --> status pending >> waiting for user confirmation')
                await message.reply_text(
                    text='متأكددد بدك احذف?',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text='أي', callback_data='deleteyes')],
                        [InlineKeyboardButton(text='لا', callback_data='deleteno')],
                    ])
                    )
    else:
        return


@Client.on_message(filters.command(['debug', 'log']) & filters.private)
async def send_log(_: Client, message: Message) -> None:
    LOGGER.debug(f"USED_CMD --> /debug command >> @{message.from_user.username}")
    try:
        sudo_user = int(os.environ["SUDO_USER"])
        if sudo_user != message.chat.id:
            raise Exception
    except Exception:
        LOGGER.debug('LOG__CMD --> status failed >> user not a sudo')
        return
    if os.path.exists('debug.log'):
        await message.reply_document(
            'debug.log'
        )
        LOGGER.debug('LOG__CMD --> status sucess >> log send to the sudo_user')
    else:
        await message.reply_text("خطأ الملف مو موجود")
