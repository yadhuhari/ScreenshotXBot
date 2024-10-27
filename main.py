import time
import asyncio
import datetime
import random
from pyrogram import client, filters, ForceReply
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
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

async def sample_fn(c, m):
    chat_id = m.from_user.id
    media_msg = m.message.reply_to_message
    if media_msg.empty:
        await edit_message_text(m, text='Why did you delete the file 😠, Now i cannot help you 😒.')
        c.CURRENT_PROCESSES[chat_id] -= 1
        return
    
    uid = str(uuid.uuid4())
    output_folder = SMPL_OP_FLDR.joinpath(uid)
    if not output_folder.exists():
        os.makedirs(output_folder)
    
    if TRACK_CHANNEL:
        tr_msg = await media_msg.forward(TRACK_CHANNEL)
        await tr_msg.reply_text(f"User id: `{chat_id}`")
    
    if media_msg.media:
        typ = 1
    else:
        typ = 2
    
    try:
        start_time = time.time()
        
        await edit_message_text(m, text='𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘆𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁, 𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁! 😴')
        
        if typ == 2:
            file_link = media_msg.text
        else:
            file_link = generate_stream_link(media_msg)
        
        await edit_message_text(m, text='😀 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴 𝗦𝗮𝗺𝗽𝗹𝗲 𝗩𝗶𝗱𝗲𝗼! 𝗧𝗵𝗶𝘀 𝗺𝗶𝗴𝗵𝘁 𝘁𝗮𝗸𝗲 𝘀𝗼𝗺𝗲 𝘁𝗶𝗺𝗲.')
        
        duration = await get_duration(file_link)
        if isinstance(duration, str):
            await edit_message_text(m, text="😟 Sorry! I cannot open the file.")
            l = await media_msg.forward(Config.LOG_CHANNEL)
            await l.reply_text(f'stream link : {file_link}\n\nSample video requested\n\n{duration}', True)
            c.CURRENT_PROCESSES[chat_id] -= 1
            return
        
        reduced_sec = duration - int(duration*10 / 100)
        print(f"Total seconds: {duration}, Reduced seconds: {reduced_sec}")
        sample_duration = await c.db.get_sample_duration(chat_id)
        
        start_at = get_random_start_at(reduced_sec, sample_duration)
        
        sample_file = output_folder.joinpath(f'sample_video.mkv')
        subtitle_option = await fix_subtitle_codec(file_link)
        
        ffmpeg_cmd = f"ffmpeg -hide_banner -ss {start_at} -i {shlex.quote(file_link)} -t {sample_duration} -map 0 -c copy {subtitle_option} {sample_file}"
        output = await run_subprocess(ffmpeg_cmd)
        #print(output[1].decode())
        
        if not sample_file.exists():
            await edit_message_text(m, text='😟 Sorry! Sample video generation failed possibly due to some infrastructure failure 😥.')
            
            l = await media_msg.forward(Config.LOG_CHANNEL)
            await l.reply_text(f'stream link : {file_link}\n\n duration {sample_duration} sample video generation failed\n\n{output[1].decode()}', True)
            c.CURRENT_PROCESSES[chat_id] -= 1
            return
        
        thumb = await generate_thumbnail_file(sample_file, uid)
        
        await edit_message_text(m, text=f'🤓 𝗦𝗮𝗺𝗽𝗹𝗲 𝘃𝗶𝗱𝗲𝗼 𝘄𝗮𝘀 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!, 𝗡𝗼𝘄 𝘀𝘁𝗮𝗿𝘁𝗶𝗻𝗴 𝘁𝗼 𝘂𝗽𝗹𝗼𝗮𝗱!')
        
        await media_msg.reply_chat_action("upload_video")
        
        await media_msg.reply_video(
                video=sample_file, 
                quote=True,
                caption=f"📸 𝗦𝗮𝗺𝗽𝗹𝗲 𝘃𝗶𝗱𝗲𝗼. {sample_duration}s 𝗳𝗿𝗼𝗺 {datetime.timedelta(seconds=start_at)}",
                duration=sample_duration,
                thumb=thumb,
                supports_streaming=True
            )
        
        await edit_message_text(m, text=f'𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝗶𝗻 {datetime.timedelta(seconds=int(time.time()-start_time))}\n\n\n\n©️ @RoboverseTG')
        c.CURRENT_PROCESSES[chat_id] -= 1
        
    except:
        traceback.print_exc()
        await edit_message_text(m, text='😟 Sorry! Sample video generation failed possibly due to some infrastructure failure 😥.')
        
        l = await media_msg.forward(Config.LOG_CHANNEL)
        await l.reply_text(f'sample video requested and some error occoured\n\n{traceback.format_exc()}', True)
        c.CURRENT_PROCESSES[chat_id] -= 1

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

@Robot.on_message(filters.private & filters.media)
async def _(c, m):
    chat_id = m.chat.id   
    if not await c.db.is_user_exist(chat_id):
        await c.db.add_user(chat_id)
        await c.send_message(
            1002413846805,
            f"New User [{m.from_user.first_name}](tg://user?id={chat_id}) started."
        )
    
    ban_status = await c.db.get_ban_status(chat_id)
    if ban_status['is_banned']:
        if (datetime.date.today() - datetime.date.fromisoformat(ban_status['banned_on'])).days > ban_status['ban_duration']:
            await c.db.remove_ban(chat_id)
        else:
            await m.reply_text(
                f"Sorry Dear, You misused me. So you are **Blocked!**.\n\nBlock Reason: __{ban_status['ban_reason']}__",
                quote=True
            )
            return
    
    if m.document:
        if "video" not in m.document.mime_type:
            await m.reply_text(f"**😟 Sorry! Only support Media Files.**\n**Your File type :** `{m.document.mime_type}.`", quote=True)

    if not is_valid_file(m):
        return
    
    snt = await m.reply_text("𝗛𝗶 𝘁𝗵𝗲𝗿𝗲, 𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁 𝘄𝗵𝗶𝗹𝗲 𝗜'𝗺 𝗴𝗲𝘁𝘁𝗶𝗻𝗴 𝗲𝘃𝗲𝗿𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗮𝗱𝘆 𝘁𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘆𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁!", quote=True)
    
    file_link = generate_stream_link(m)
    
    duration = await get_duration(file_link)
    if isinstance(duration, str):
        await snt.edit_text("😟 𝗦𝗼𝗿𝗿𝘆! 𝗜 𝗰𝗮𝗻𝗻𝗼𝘁 𝗼𝗽𝗲𝗻 𝘁𝗵𝗲 𝗳𝗶𝗹𝗲.")
        l = await m.forward(Config.LOG_CHANNEL)
        await l.reply_text(f'stream link : {file_link}\n\n {duration}', True)
        return
    
    btns = gen_ik_buttons()
    
    if duration >= 600:
        btns.append([InlineKeyboardButton('Generate Sample Video!', 'smpl')])
    
    await snt.edit_text(
        text=f"""𝗛𝗶, 𝗖𝗵𝗼𝗼𝘀𝗲 𝘁𝗵𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁𝘀 𝘆𝗼𝘂 𝗻𝗲𝗲𝗱.

𝗧𝗼𝘁𝗮𝗹 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻: {datetime.timedelta(seconds=duration)} ({duration}𝘀)""",
        reply_markup=InlineKeyboardMarkup(btns)
    )

@Robot.on_callback_query(filters.create(lambda _, query: query.data.startswith('smpl')))
async def _(c, m):
    asyncio.create_task(sample_fn(c, m))



print("Bot Started")
Robot.run()
