from pyrogram import client, filters, ForceReply
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
import random
from pyrogram.errors import FloodWait

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

def is_valid_file(msg):
    if not msg.media:
        return False
    if msg.video:
        return True
    if (msg.document) and any(mime in msg.document.mime_type for mime in ['video', "application/octet-stream"]):
        return True
    return False

def is_url(text):
    return text.startswith('http')

async def get_duration(input_file_link):
    ffmpeg_dur_cmd = f"ffprobe -v error -show_entries format=duration -of csv=p=0:s=x -select_streams v:0 {shlex.quote(input_file_link)}"
    #print(ffmpeg_dur_cmd)
    out, err = await run_subprocess(ffmpeg_dur_cmd)
    out = out.decode().strip()
    if not out:
        return err.decode()
    duration = round(float(out))
    if duration:
        return duration
    return 'No duration!'

def generate_stream_link(media_msg):
    file_id = pack_id(media_msg)
    return f"{Config.HOST}/stream/{file_id}"

def gen_ik_buttons():
    btns = []
    i_keyboard = []
    for i in range(2, 11):
        i_keyboard.append(
            InlineKeyboardButton(
                f"{i}",
                f"scht+{i}"
            )
        )
        if (i>2) and (i%2) == 1:
            btns.append(i_keyboard)
            i_keyboard = []
        if i==10:
            btns.append(i_keyboard)
    btns.append([InlineKeyboardButton('Manual Screenshots!', 'mscht')])
    btns.append([InlineKeyboardButton('Trim Video!', 'trim')])
    return btns

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

𝗣𝗿𝗲𝘀𝘀 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻 𝘁𝗼 𝗰𝗵𝗮𝗻𝗴𝗲 𝘁𝗵𝗲 𝘀𝗲𝘁𝘁𝗶𝗻𝗴𝘀."""
    )

@Robot.on_callback_query(filters.create(lambda _, query: query.data.startswith('mscht')))
async def _(c, m):
    dur = m.message.text.markdown.split('\n')[-1]
    await m.message.delete(True)
    await c.send_message(
        m.from_user.id,
        f'#𝗺𝗮𝗻𝘂𝗮𝗹_𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁\n\n{dur}\n\n𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗹𝗶𝘀𝘁 𝗼𝗳 𝘀𝗲𝗰𝗼𝗻𝗱𝘀 𝘀𝗲𝗽𝗮𝗿𝗮𝘁𝗲𝗱 𝗯𝘆 ,(𝗰𝗼𝗺𝗺𝗮).\n𝗘𝗴: 𝟬,𝟭𝟬,𝟰𝟬,𝟲𝟬,𝟭𝟮𝟬.
𝗧𝗵𝗶𝘀 𝘄𝗶𝗹𝗹 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁𝘀 𝗮𝘁 𝟬, 𝟭𝟬, 𝟰𝟬, 𝟲𝟬, 𝗮𝗻𝗱 𝟭𝟮𝟬 𝘀𝗲𝗰𝗼𝗻𝗱𝘀. \n\n1. 𝟭. 𝗧𝗵𝗲 𝗹𝗶𝘀𝘁 𝗰𝗮𝗻 𝗵𝗮𝘃𝗲 𝗮 𝗺𝗮𝘅𝗶𝗺𝘂𝗺 𝗼𝗳 𝟭𝟬 𝘃𝗮𝗹𝗶𝗱 𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻𝘀.\n2. 𝟮. 𝗧𝗵𝗲 𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝗵𝗮𝘀 𝘁𝗼 𝗯𝗲 𝗴𝗿𝗲𝗮𝘁𝗲𝗿 𝘁𝗵𝗮𝗻 𝗼𝗿 𝗲𝗾𝘂𝗮𝗹 𝘁𝗼 𝟬, 𝗼𝗿 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 𝘁𝗵𝗲 𝘃𝗶𝗱𝗲𝗼 𝗹𝗲𝗻𝗴𝘁𝗵 𝗶𝗻 𝗼𝗿𝗱𝗲𝗿 𝘁𝗼 𝗯𝗲 𝘃𝗮𝗹𝗶𝗱.',
        reply_to_message_id=m.message.reply_to_message.message_id,
        reply_markup=ForceReply()
    )
