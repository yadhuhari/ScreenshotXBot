from pyrogram import client, filters
from pyrogram.typed import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random

Robot = Client(
  name="ScreenshotGenRobot",
  api_id="23050566",
  api_hash="25e954ccd4afb778eea69bd6754275ff",
  bot_token="7631983304:AAFiHXuNJph3qxu_5GEKZm8W6RlT71V_Ch8"
)

PICS = [
 "http://ibb.co/zbSz1yt",
 "http://ibb.co/NjH1Lsc",
 "http://ibb.co/ydCJ9B2",
 "http://ibb.co/B4Cp2yz"
]

@Robot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""𝗛𝗲𝘆 {message.from_user.mention},
        
𝗜 𝗮𝗺 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗼𝗿 𝗕𝗼𝘁. 𝗜 𝗰𝗮𝗻 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁𝘀 𝗼𝗿 𝘀𝗮𝗺𝗽𝗹𝗲 𝗰𝗹𝗶𝗽𝘀 𝗳𝗿𝗼𝗺 𝘆𝗼𝘂𝗿 𝘃𝗶𝗱𝗲𝗼 𝗳𝗶𝗹𝗲𝘀 😍
𝗙𝗼𝗿 𝗺𝗼𝗿𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 𝗽𝗿𝗲𝘀𝘀 /help.""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url="t.me/RoboverseTG"),
            ],[
            InlineKeyboardButton("🛠 𝗛𝗲𝗹𝗽", callback_data="help"),
            InlineKeyboardButton("💀 𝗔𝗯𝗼𝘂𝘁 𝗠𝗲", callback_data="about")
            ]]
            )
        )

@Robot.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""𝗛𝗲𝘆 {message.from_user.mention},

𝗬𝗼𝘂 𝗰𝗮𝗻 𝘂𝘀𝗲 𝗺𝗲 𝘁𝗼 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲:

    🔹 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁𝘀
    🔹 𝗦𝗮𝗺𝗽𝗹𝗲 𝘃𝗶𝗱𝗲𝗼 𝗰𝗹𝗶𝗽𝘀
    🔹 𝗧𝗿𝗶𝗺 𝗩𝗶𝗱𝗲𝗼

▪️ 𝗜 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗮𝗻𝘆 𝗸𝗶𝗻𝗱 𝗼𝗳 𝘁𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝘃𝗶𝗱𝗲𝗼 𝗳𝗶𝗹𝗲𝘀, 𝗽𝗿𝗼𝘃𝗶𝗱𝗲𝗱 𝗶𝘁 𝗶𝘀 𝗻𝗼𝘁 𝗰𝗼𝗿𝗿𝘂𝗽𝘁𝗲𝗱.

𝗧𝗼 𝗴𝗲𝘁 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 𝗼𝗿 𝘀𝗮𝗺𝗽𝗹𝗲 𝗰𝗹𝗶𝗽, 𝗷𝘂𝘀𝘁 𝘀𝗲𝗻𝗱 𝗺𝗲 𝘁𝗵𝗲 𝘁𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗳𝗶𝗹𝗲 𝗼𝗿 𝘁𝗵𝗲 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗨𝗥𝗟.


𝗦𝗲𝗲 /settings 𝘁𝗼 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗲 𝗯𝗼𝘁'𝘀 𝗯𝗲𝗵𝗮𝘃𝗶𝗼𝗿.
𝗨𝘀𝗲 /set_watermark 𝘁𝗼 𝘀𝗲𝘁 𝗰𝘂𝘀𝘁𝗼𝗺 𝘄𝗮𝘁𝗲𝗿𝗺𝗮𝗿𝗸𝘀 𝘁𝗼 𝘆𝗼𝘂𝗿 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁𝘀 𝗮𝗻𝗱 𝘀𝗮𝗺𝗽𝗹𝗲 𝗰𝗹𝗶𝗽𝘀.""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="start")
            ]]
            )
        )

@Robot.on_message(filters.command("about"))
async def about(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""🤖 𝗠𝘆 𝗡𝗮𝗺𝗲 : [𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗼𝗿 𝗕𝗼𝘁 ✨](t.me/ScreenshotGenRobot)
📝 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲 : [𝗣𝘆𝘁𝗵𝗼𝗻 𝟯.𝟭𝟯.𝟬](www.python.org)

📚 𝗙𝗿𝗮𝗺𝗲𝘄𝗼𝗿𝗸 : [𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺](https://docs.pyrogram.org/)

📡 𝗛𝗼𝘀𝘁𝗲𝗱 𝗼𝗻 : [𝗥𝗲𝗻𝗱𝗲𝗿](www.render.com)

👨‍💻 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 : [𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 @𝗥𝗼𝗯𝗼𝘃𝗲𝗿𝘀𝗲𝗧𝗚 ✨](t.me/TGDeveloperRobot)

📣 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 : [𝗥𝗼𝗯𝗼𝘃𝗲𝗿𝘀𝗲𝗧𝗚](t.me/RoboverseTG)""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="help"),
            InlineKeyboardButton("🏡 𝗛𝗼𝗺𝗲", callback_data="start")
            ]]
            )
        )
                                     
@Robot.on_message(filters.command("settings"))
async def settings(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption="""𝗛𝗲𝗿𝗲 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗲 𝗺𝘆 𝗯𝗲𝗵𝗮𝘃𝗶𝗼𝗿.

𝗣𝗿𝗲𝘀𝘀 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻 𝘁𝗼 𝗰𝗵𝗮𝗻𝗴𝗲 𝘁𝗵𝗲 𝘀𝗲𝘁𝘁𝗶𝗻𝗴𝘀.""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("
