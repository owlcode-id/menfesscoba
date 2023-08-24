try:
    import telebot
    import time
    import os
    import json
    from dotenv import load_dotenv
    from telebot import types
except:
    print("error! install pytelegrambotapi first by running 'pip install pytelegrambotapi'")

load_dotenv()

token = os.getenv("BOT_TOKEN")
ch = os.getenv("CHANNEL")
link = os.getenv("LINK")
admin = json.loads(os.getenv("ADMIN"))
trigger = json.loads(os.getenv("TAG"))
delay = os.getenv("DELAY")
gc = os.getenv("GROUP_ID")
mulai = '''
Selamat Datang Di *Garz Menfess*

kamu bebas mengirim menfess pada channel garzmenfess, jika ingin memposting menfess silahkan kirim pesan teks beserta tag dibawah ini :
	
*{}*

'''

bot = telebot.TeleBot(token)
kirim = bot.send_message
kopi = bot.copy_message
lanjut = bot.register_next_step_handler
ma = types.InlineKeyboardMarkup
bb = types.InlineKeyboardButton

apaantuh = []

def diam(id):
    data = int(id)
    apaantuh.append(data)
    time.sleep(delay)
    apaantuh.remove(data)

@bot.message_handler(commands=["start", "broadcast", "ping"], chat_types=["private"])
def garz(message):
    id = message.chat.id
    teks = message.text
    
    is_joined_channel = bot.get_chat_member(ch, id).status == "member"
    is_joined_group = bot.get_chat_member(gc, id).status == "member"
    
    if not is_joined_channel or not is_joined_group:
        yamete = ma(row_width=1)
        
        if not is_joined_channel:
            rawr = bb(text="Join Channel", url=link)
            yamete.add(rawr)
        
        if not is_joined_group:
            rawr_gc = bb(text="Join Group", url=f"https://t.me/{get_group_username()}")
            yamete.add(rawr_gc)
            
        kirim(id, "To use this bot, you must first join our channel and group.", reply_markup=yamete)
        return
    
    nggih = '\n'.join(map(str, trigger))
    yamete = ma(row_width=2)
    rawr = bb(text="Channel Menfess", url=link)
    
    try:
        group_invite_link = bot.export_chat_invite_link(gc)
        rawr_gc = bb(text="Group Menfess", url=group_invite_link)
    except Exception as e:
        print(f"Error getting group invite link: {e}")
        rawr_gc = bb(text="Group Menfess", url=f"https://t.me/{get_group_username()}")
        
    yamete.add(rawr, rawr_gc)
    kirim(id, mulai.format(nggih), parse_mode="markdown", reply_markup=yamete)
    return

def get_group_username():
    try:
        group_info = bot.get_chat(gc)
        group_username = group_info.username
        return group_username
    except Exception as e:
        print(f"Error getting group username: {e}")
        return ""

@bot.message_handler(content_types=["text"])
def menfessin(message):
    id = message.chat.id
    teks = message.text
    ah = tegar(teks)
    ih = len(teks.split(" "))
    
    is_joined_channel = bot.get_chat_member(ch, id).status == "member"
    is_joined_group = bot.get_chat_member(gc, id).status == "member"
    
    if not is_joined_channel or not is_joined_group:
        yamete = ma(row_width=1)
        
        if not is_joined_channel:
            rawr = bb(text="Join Channel", url=link)
            yamete.add(rawr)
        
        if not is_joined_group:
            rawr_gc = bb(text="Join Group", url=f"https://t.me/joinchat/{gc}")
            yamete.add(rawr_gc)
            
        kirim(id, "You must first join our channel and group before sending a menfess message.", reply_markup=yamete)
        return
    
    if id in apaantuh:
        kirim(id, f"Failed to send!!\n\nYou just sent a menfess, wait {delay} seconds before posting again!")
        return
    elif ih < 3:
        kirim(id, "Failed to send!!\n\nMessage must be at least 3 words long!!")
        return
    elif ah == False:
        tag = '\n'.join(map(str, trigger))
        kirim(id, f"Failed to send!!\n\nPlease use the tags below:\n{tag}")
        return
    elif ah == True:
        pesan = kirim(ch, teks)
        links = link + "/" + str(pesan.id)
        linksk = links + "?comment=" + str(pesan.id)
        kirim(id, f"*Menfess Sent Successfully!!*", parse_mode="markdown", reply_markup=awikwokbanget(links, linksk))
        diam(id)
        return

def tegar(data):
    for x in data.split(" "):
        yow = x
        for i in trigger:
            yaw = i
            if yaw in yow:
                data = 1
    if data == 1:
        return True
    else:
        return False

def broadcast(message):
    id = message.chat.id
    pesans = message.message_id
    with open("member.db", "r") as file:
        lines = file.read().splitlines()
        for x in lines:
            try:
                yy = int(x)
                kopi(yy, id, pesans)
            except:
                print(f"Failed to send a message to user *{x}*\nMaybe the bot has been blocked.")
    kirim(id, "Broadcast message sent successfully.")

def awikwokbanget(cek, cekin):
    miaw = ma(row_width=2)
    b1 = bb(text="Check Post", url=cek)
    b2 = bb(text="Check Comment", url=cekin)
    miaw.add(b1, b2)
    return miaw

print("\n\nBOT IS ACTIVE!!! @GARZPROJECT")
bot.infinity_polling()
