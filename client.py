import main as m
import connection
import discord
import random
import api as a
from discord.ext import commands, tasks
import slash
import datetime
import keep_alive


@m.client.event
async def on_ready():
  print("Bot is ready")
  servers = len(m.client.guilds)
  nub = random.randint(0, 25)
  connection.connect()
  foo.start()
  jadwal_bola.start()

  await m.client.tree.sync()

  await m.client.change_presence(
    activity=discord.Activity(type=discord.ActivityType.watching,
                              name=f'{servers} Servers~ | {m.emot[nub]}'))


@m.client.event
async def on_message(message):
  num = random.randint(0, 25)
  pesan = message.content.split(" ")
  if pesan[0] == m.prefix + "hello" or pesan[0] == m.prefix + "Hello" or pesan[
      0] == m.prefix + "hi" or pesan[0] == m.prefix + "Hi":
    await message.channel.send("Hello {0.author.mention} {1}".format(
      message, m.emot[num]),
                               reference=message)

  # add user yt
  elif pesan[0] == m.prefix + "yt" or pesan[0] == m.prefix + "Yt" or pesan[
      0] == m.prefix + "YT":
    res = await message.channel.send(
      "Hello {0.author.mention} Please Wait... 📀 {1}".format(
        message, m.emot[num]),
      reference=message)
    username = pesan[1]
    # check username in database
    if (connection.cekusername_yt(username, message.guild.id) == False
        or connection.cekmax_yt(message.guild.id) == False):
      await res.edit(
        content=
        "Hello {0.author.mention} Username Already exist or Max Limit 🚨 {1}".
        format(message, m.emot[num - 1]))
    else:
      check_username = a.notfound(username)
      if check_username == True:
        link = a.api(username)
        data = {
          "username": username,
          "link": link,
          "link_live" : "",
          "link_short": "",
          "server_id": message.guild.id,
          "channel_id": message.channel.id,

        }
        if (connection.insert_yt(data) == True):
          await res.edit(
            content="Yey {0.author.mention} user added successfully 🙌🏼 {1}".
            format(message, m.emot[num - 1]))

      else:
        await res.edit(
          content=
          "Hello {0.author.mention} Username Not Found , Please Add Username Youtube (Without @) 🔴 {1}"
          .format(message, m.emot[num - 1]))

  # show user yt
  elif pesan[0] == m.prefix + "show":
    if (pesan[1].lower() == "yt" or pesan[1].lower() == "youtube"):

      res = await message.channel.send(
        "Hello {0.author.mention} Please Wait... 📀 {1}".format(
          message, m.emot[num]),
        reference=message)
      data = connection.getdata_yt()
      if len(data) == 0:
        await res.edit(content="Hello {0.author.mention} No Data 🚀 {1}".format(
          message, m.emot[num - 1]))
      else:
        list_user = ""
        no = 1
        for i in data:
          if(str(i['server_id']) == str(message.guild.id)):
            list_user += str(no) + ". " + i['username'] + "\n"
            no += 1

        await res.edit(
          content="Hello {0.author.mention} \n ```List Users Youtube: \n{1}```"
          .format(message, list_user))
    elif (pesan[1].lower() == "bola"):
      res = await message.channel.send(
        "Hello {0.author.mention} Please Wait... 📀 {1}".format(
          message, m.emot[num]),
        reference=message)
      data = connection.getdata_berita()
      # cek apakah channel dan server sudah ada di database
      if len(data) == 0:
        await res.edit(content="Hello {0.author.mention} No Data 🚀 {1}".format(
          message, m.emot[num - 1]))
      else:
        server = message.guild.id
        check_server = [str(i['channel_id']) for i in data if str(i['server_id']) == str(server)]
        # print(check_server)

        if len(check_server) == 0:
          await res.edit(
            content=
            "Hello {0.author.mention} your channel has not turned on the news schedule, please turn it on with the command ```!jadwal bola``` {1}"
            .format(message, m.emot[num - 1]))
        else:
          channel = m.client.get_channel(message.channel.id)
          channel1 = m.client.get_channel(int(check_server[0]))
          
          # make embed
          embed = discord.Embed(
            title="Announcement",
            description=
            f"Your channel has already turned on the news schedule, please check the channel: {channel1.mention}",
            color=0x00ff00)
          # delete message and res
          await message.delete()
          await res.delete()

          await channel.send(embed=embed)
  elif pesan[0].lower() == m.prefix + "invite":
    link = "https://discord.com/oauth2/authorize?client_id=796771650677899275&permissions=8&scope=bot"
    embed = discord.Embed(title="Invite Me",
                          description=f"[Click Here]({link})",
                          color=0x00ff00)
    await message.channel.send(embed=embed, reference=message)
  # delete user yt
  elif pesan[0].lower() == m.prefix + "delete":
    res = await message.channel.send(
      "Hello {0.author.mention} Please Wait... 📀 {1}".format(
        message, m.emot[num]),
      reference=message)
    if (pesan[1].lower() == "yt"):
      username = pesan[2]
      if (connection.cekusername_yt(username, message.guild.id) == True):
        await res.edit(
          content="Hello {0.author.mention} Username Not Found 🚀 {1}".format(
            message, m.emot[num - 1]))
      else:
        connection.delete_yt(username, message.guild.id)
        await res.edit(
          content="Hello {0.author.mention} user successfully deleted {1}".
          format(message, m.emot[num - 1]))
    elif (pesan[1].lower() == "bola"):
      server = message.guild.id
      data = connection.getdata_berita()
      check_server = [i['server_id'] for i in data if str(i['server_id']) == str(server)]
      if len(check_server) == 0:
        await res.edit(
          content=
          "Hello {0.author.mention} your channel has not turned on the news schedule, please turn it on with the command ```!jadwal bola``` {1}"
          .format(message, m.emot[num - 1]))
      else:
        connection.delete_berita(server)
        await res.edit(
          content=
          "Hello {0.author.mention} ball schedule has been successfully deleted {1}"
          .format(message, m.emot[num - 1]))
    else:
      await res.edit(
        content=
        "Hello {0.author.mention} ```Please Input Command \n!delete yt or !delete bola``` {1}"
        .format(message, m.emot[num - 1]))
    # jadwal bola
  elif pesan[0] == m.prefix + "jadwal":
    if (pesan[1] == "bola" or pesan[1] == "Bola" or pesan[1] == "BOLA"):
      res = await message.channel.send(
        "Hello {0.author.mention} Please Wait... 📀 {1}".format(
          message, m.emot[num]),
        reference=message)
      data = a.jadwalbola()
      if len(data) == 0:
        await res.edit(
          content=
          "Yo {0.author.mention} \nThere are no matches scheduled for today. {1}"
          .format(message, m.emot[num - 1]))
      else:
        #  mengambil tanggal hari ini + 1
        today = datetime.datetime.today() + datetime.timedelta(days=1)
        today = today.strftime("%Y-%m-%d")

        dataBerita = {
          'bola': "on",
          "server_id": message.guild.id,
          "channel_id": message.channel.id,
          "tanggal": today
        }
        insData = connection.insert_berita(dataBerita)
        if insData == True:
          await res.edit(
            content=
            "Hello {0.author.mention} \nBall schedule has been successfully added to the channel {1}"
            .format(message, m.emot[num - 1]))
          # data is a dictionary \
          for mtch in range(len(data)):
            # make embed with picture
            embed1 = discord.Embed(title="Football Match Schedule",
                                   color=0x04fa00)
            embed1.set_thumbnail(url=data[str(mtch + 1)]['home']['pict'])
            embed1.add_field(name="Team Home",
                             value=f"{data[str(mtch+1)]['home']['team']}",
                             inline=True)
            embed1.add_field(name="VS",
                             value=f"{data[str(mtch+1)]['jadwal']}",
                             inline=True)
            embed1.add_field(name="Team Away",
                             value=f"{data[str(mtch+1)]['away']['team']}",
                             inline=True)
            # pict team home
            embed1.set_image(url=data[str(mtch + 1)]['away']['pict'])
            await message.channel.send(embed=embed1)
        else:
          await res.edit(
            content=
            f"Hello {message.author.mention} \nThe ball schedule is already active on the channel {message.channel.mention} { m.emot[num - 1]}"
          )
  elif pesan[0].lower() == m.prefix + "help":
    embed = discord.Embed(title="🌼 List Commands 🌻",
                          description="```Hello```",
                          color=0x00ff00)
    embed.set_thumbnail(url=m.client.user.display_avatar.url)
    embed.add_field(name="Information About CocoPout",
                    value="```Since 2023 By ERHA ☯️```",
                    inline=False)
    embed.add_field(name="🌼 Prefix", value="```!```", inline=False)
    embed.add_field(name="🤖 help",
                    value="```diff\n+List Commands For CoCoPou 🤡```",
                    inline=False)
    embed.add_field(
      name="🎐 jadwal <option>",
      value=
      "```diff\n+Enable News,  available options : bola```\nexample : !jadwal bola",
      inline=False)
    embed.add_field(
      name="🔨 delete <option1> <option2>",
      value=
      "```diff\n+Disable News or delete channel youtube, available options1 : bola,yt || available <option2> for youtube channel```\nexample : !delete yt cicilalang or !delete bola",
      inline=False)
    embed.add_field(
      name="🔗 yt <usernameYoutubeChannel>",
      value=
      "```diff\n+Add Youtube Channel Notifications.```\nexample : !yt cicilalang",
      inline=False)
    embed.add_field(name="🎊 hi",
                    value="```diff\n+To Test CoCoPou 👀```",
                    inline=False)
    embed.set_footer(text="Cocopou Supports Commands Slash {/} 💖")
    await message.channel.send(embed=embed)


# loop jadwal bola
@tasks.loop(seconds=1800)
async def jadwal_bola():
  num = random.randint(1, 25)
  try:
    all_server = connection.getdata_berita()
    if (len(all_server) == 0):
      return False
    else:
      for server in all_server:        
        today = datetime.datetime.today() + datetime.timedelta(days=1)
        today = today.strftime("%Y-%m-%d")
        
        if (server['tanggal'] != today):
          data = a.jadwalbola()
          # update tanggal
          connection.update_berita(server['_id'], today)
          if len(data) == 0:
            channel = m.client.get_channel(server['channel_id'])
            await channel.send(
              content="Yo \nThere are no matches scheduled for today. {0}".
              format(m.emot[num - 1]))
          else:
            for mtch in range(len(data)):
              # make embed with picture
              embed1 = discord.Embed(title="Football Match Schedule",
                                     color=0x04fa00)
              # images on embed
              embed1.set_thumbnail(url=data[str(mtch + 1)]['home']['pict'])
              embed1.add_field(name="Team Home",
                               value=f"{data[str(mtch+1)]['home']['team']}",
                               inline=True)
              embed1.add_field(name="VS",
                               value=f"{data[str(mtch+1)]['jadwal']}",
                               inline=True)
              embed1.add_field(name="Team Away",
                               value=f"{data[str(mtch+1)]['away']['team']}",
                               inline=True)
              # pict team home
              embed1.set_image(url=data[str(mtch + 1)]['away']['pict'])
              channel = m.client.get_channel(int(server['channel_id']))
              await channel.send(embed=embed1)
        else:
          pass
  except Exception as e:
    print(e)


# loop berita youtube
@tasks.loop(seconds=100)
async def foo():
  # auto update yt
  nub = random.randint(0, 25)

  alldata_yt = connection.getdata_yt()
  for data in alldata_yt:
    # get link videos from api and compare with database
    user = data['username']
    if(len(alldata_yt) == 0):
      return False
    else:
      link_new = a.api(user)
      if link_new != data['link']:
        title = a.gettitle(user)
        # update database
        connection.checkupdate_yt(link_new, data['_id'])
        # send message
        channel = m.client.get_channel(int(data['channel_id']))
        await channel.send(
          f"Hello {channel.guild.default_role.mention} {m.emot[nub]} ```New Video! \n{title}``` {link_new}"
        )
    try:
      link_stream = a.getstream(user)
      # get link stream from api and compare with database
      if link_stream[0] != data['link_live']:
        # update database
        connection.checkupdate_ytlive(link_stream[0], data['_id'])
        # send message
        channel = m.client.get_channel(int(data['channel_id']))
        await channel.send(
          f"Hello {channel.guild.default_role.mention} {m.emot[nub]} ```Live Stream Video! \n{link_stream[1]}``` {link_stream[0]}"
        )
      # get short link from api and compare with database
      link_short = a.getshort(user)
      if link_short[0] != data['link_short']:
        # update database
        connection.checkupdate_ytsr(link_short[0], data['_id'])
        # send message
        channel = m.client.get_channel(int(data['channel_id']))
        await channel.send(
          f"Hello {channel.guild.default_role.mention} {m.emot[nub]} ```New Shorts! \n{link_short[1]}``` {link_short[0]}"
        )
    except:
      pass


# # get token from .env file in same directory
# keep_alive.keep_alive()
m.client.run(
  "Nzk2NzcxNjUwNjc3ODk5Mjc1.GqqSHE.OrAR08Se6pumzvIadSX360MxXyM3EFG_qpQ2Ug")
