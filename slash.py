import main as m
import discord
import connection
import api as a
import random


@m.client.tree.command(name="hi" , description="hi")
async def hi(interaction : discord.Interaction):
    await interaction.response.send_message(f"hi {interaction.user.mention}" , ephemeral=True)


# yt command
@m.client.tree.command(name="yt" , description="Add youtube channel to show new video")
async def yt(interaction : discord.Interaction , channel : str):
    username = channel
    # check username in database
    if (connection.cekusername_yt(username, interaction.guild.id) == False
        or connection.cekmax_yt(interaction.guild.id) == False):
      embed = discord.Embed(title="Announcement",description=f"Hello {interaction.user.mention} Username Already exist or Max Limit 🚨 {m.emot[9]}")
      await interaction.response.send_message(embed=embed)
    else:
      check_username = a.notfound(username)
      if check_username == True:
        link = a.api(username)
        data = {
          "username": username,
          "link": link,
          "server_id": interaction.guild.id,
          "channel_id": interaction.channel.id
        }
        if (connection.insert_yt(data) == True):         
          embed = discord.Embed(title="Announcement",description=f"Yey {interaction.user.mention} user added successfully 🙌🏼 {m.emot[19]}")
          await interaction.response.send_message(embed=embed)

      else:       
        embed = discord.Embed(title="Announcement",description=f"Hello {interaction.user.mention} Username Not Found , Please Add Username Youtube (Without @) 🔴 {m.emot[19]}")
        await interaction.response.send_message(embed=embed)

# show yt command
@m.client.tree.command(name="show" , description="Show All Youtube Channel or Show News About Football")
@discord.app_commands.choices( choices=[
  discord.app_commands.Choice(name="yt" , value="yt") , 
  discord.app_commands.Choice(name="bola" , value="bola")
  ])

async def show(interaction : discord.Interaction, choices : discord.app_commands.Choice[str]):
    num = random.randint(0, 25)
    # check choices
    if choices.name == "yt":
        data = connection.getdata_yt()
        if len(data) == 0:
          embed  = discord.Embed(title="Announcement", description=f"```fix\nNo User Youtube {m.emot[23-3]}```", color=0x00ff00)
          await interaction.response.send_message(embed=embed)
        else:
          list_user = ""
          no = 1
          for i in data:
            list_user += str(no) + ". " + i[1] + "\n"
            no += 1
          embed  = discord.Embed(title="Announcement", description=f"```fix\nList Users Youtube:\n{list_user}```", color=0x00ff00)
          await interaction.response.send_message(embed=embed)

    elif choices.name == "bola":
      data = connection.getdata_berita()
      # cek apakah channel dan server sudah ada di database
      if len(data) == 0:
        await interaction.response.send_message(content="Hello {0.user.mention} No Data 🚀 {1}".format(interaction, m.emot[num - 1]))
      else:
          server = interaction.guild.id
          check_server = [i[3] for i in data if i[2] == str(server)]
          if len(check_server) == 0:
            embed  = discord.Embed(title="Announcement", description=f"```fix\nyour channel has not turned on the news schedule, please turn it on with the command !jadwal bola {m.emot[num - 1]}```", color=0x00ff00)
            await interaction.response.send_message(embed=embed)
          else:
            channel = m.client.get_channel(int(check_server[0]))
            # make embed
            embed = discord.Embed(title="Announcement", description=f"Your channel has already turned on the news schedule, please check the channel: {channel.mention}", color=0x00ff00)
            await interaction.response.send_message(embed=embed)
    else:
       embed  = discord.Embed(title="Announcement", description="```fix\nPlease Enter yt or bola```", color=0x00ff00)
       await interaction.response.send_message(embed=embed)

# show delete command
@m.client.tree.command(name="delete" , description="Delete  Youtube Channel or Delete News About Football From This Server")
@discord.app_commands.choices( choices=[
  discord.app_commands.Choice(name="yt" , value="yt") , 
  discord.app_commands.Choice(name="bola" , value="bola")
  ])
      #   make async def if yt get str input but if bola dont get str input
async def delete(interaction:discord.Interaction, choices:discord.app_commands.Choice[str], channel:str = None):
    num = random.randint(0, 25)
    if(choices.name == "yt"):
          if(channel == None): 
            embed = discord.Embed(title="Delete Youtube Channel", description="```diff\n-Please Enter Channel Youtube (Without @)```", color=0x00ff00)
            await interaction.response.send_message(embed=embed)
          else:
            username = channel
            if (connection.cekusername_yt(username, interaction.guild.id) == True):              
              embed = discord.Embed(title="Delete Youtube Channel", description=f"```diff\n-Username Not Found 🔴 {m.emot[num]}```", color=0x00ff00)
              await interaction.response.send_message(embed=embed)
            else:
              connection.delete_yt(username, interaction.guild.id)              
              embed = discord.Embed(title="Delete Youtube Channel", description=f"```CSS\nuser successfully deleted {m.emot[num]}```", color=0x00ff00)
              await interaction.response.send_message(embed=embed)            
    elif(choices.name == "bola"):
          server = interaction.guild.id
          data = connection.getdata_berita()
          check_server = [i[2] for i in data if i[2] == str(server)]
          if len(check_server) == 0:
            embed = discord.Embed(title="Delete Soccer Schedule", description=f"```yaml\nYour channel has not turned on the news schedule, please turn it on with the command !jadwal bola {m.emot[num]}```", color=0x00ff00)
            await interaction.response.send_message(embed=embed)                    
          else:
            connection.delete_berita(server)
            embed = discord.Embed(title="Delete Soccer Schedule", description=f"```CSS\nBall schedule has been successfully deleted {m.emot[num]}```", color=0x00ff00)
            await interaction.response.send_message(embed=embed)    

# show help command
@m.client.tree.command(name="help" , description="Show All Command")
async def help(interaction:discord.Interaction):
    embed = discord.Embed(title="🌼 List Commands 🌻", description="```Hello```", color=0x00ff00)
    embed.set_thumbnail(url=m.client.user.display_avatar.url)
    embed.add_field(name="Information About CocoPout", value="```Since 2023 By ERHA ☯️```", inline=False)
    embed.add_field(name="🌼 Prefix", value="```!```", inline=False)
    embed.add_field(name="🤖 help", value="```diff\n+List Commands For CoCoPou 🤡```", inline=False)
    embed.add_field(name="🎐 jadwal <option>", value="```diff\n+Enable News,  available options : bola```\nexample : !jadwal bola", inline=False)
    embed.add_field(name="🔨 delete <option1> <option2>", value="```diff\n+Disable News or delete channel youtube, available options1 : bola,yt || available <option2> for youtube channel```\nexample : !delete yt cicilalang or !delete bola", inline=False)  
    embed.add_field(name="🔗 yt <usernameYoutubeChannel>", value="```diff\n+Add Youtube Channel Notifications.```\nexample : !yt cicilalang", inline=False)
    embed.add_field(name="🎊 hi", value="```diff\n+To Test CoCoPou 👀```", inline=False)
    embed.set_footer(text="Cocopou Supports Commands Slash {/} 💖")
    await interaction.response.send_message(embed=embed)

# show jadwal command
@m.client.tree.command(name="jadwal" , description="Show News About Football")
@discord.app_commands.choices( choices=[
    discord.app_commands.Choice(name="bola" , value="bola")
])
async def jadwal(interaction:discord.Interaction, choices:discord.app_commands.Choice[str]):
      num = random.randint(0, 25)
      await interaction.response.defer()         
      if(choices.name == "bola"):
         data = a.jadwalbola()
         if len(data) == 0:
           embed = discord.Embed(title="Enable Soccer Schedule", description=f"```CSS\nThere are no matches scheduled for today. {m.emot[num]}```", color=0x00ff00)
           await interaction.followup.send(embed=embed)
         else:
           today = a.datetime.date.today() + a.datetime.timedelta(days=1)
           dataBerita = {
             'bola' : "on",
             "server_id" : interaction.guild_id,
             "channel_id" : interaction.channel_id,
             'tanggal' : today
           }
           insData = connection.insert_berita(dataBerita)
           if insData == True:             
             for mtch in range(len(data)):
               # make embed with picture
               embed1 = discord.Embed(title="Football Match Schedule", color=0x04fa00)
               embed1.set_thumbnail(url=data[str(mtch+1)]['home']['pict'])
               embed1.add_field(name="Team Home", value=f"{data[str(mtch+1)]['home']['team']}", inline=True)
               embed1.add_field(name="VS", value=f"{data[str(mtch+1)]['jadwal']}", inline=True)
               embed1.add_field(name="Team Away", value=f"{data[str(mtch+1)]['away']['team']}", inline=True)
               # pict team home
               embed1.set_image(url=data[str(mtch+1)]['away']['pict'])
               await interaction.followup.send(embed=embed1)
             embed = discord.Embed(title="Enable Soccer Schedule", description=f"```diff\n+The ball schedule is Success active on the channel!```\n{interaction.channel.mention} {m.emot[num]}", color=0x00ff00)
             await interaction.followup.send(embed=embed)                                   
           else:
             embed = discord.Embed(title="Enable Soccer Schedule", description=f"The ball schedule is already active on the channel {interaction.channel.mention} {m.emot[num]}", color=0x00ff00)
             await interaction.followup.send(embed=embed)               
