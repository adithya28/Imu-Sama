import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import json
from itertools import cycle
import youtube_dl

status_message= ['8', '16' , '24' , '50']
game_data=open('gamedata.json','r')
data=json.load(game_data)
game_data.close()
write_data=open('gamedata.json','w+')
list1=data["Admin"]
total_power=list1["Total Power"]
level_divisor=1+(10000*list1["Level"]+1000*list1["Level"])/2
current_level=(int)(total_power/level_divisor)
char_list=list1["Characters"]
TOKEN = 'NDc1MDA1NjMzMjA5MzAzMDY0.DkY2fg.8nW35LjpwcF8rEuSGYfd_hT_Z-c'
client=commands.Bot(command_prefix='?')
current_status=0


##background method

async def change_status():
    await client.wait_until_ready()
    msgs=cycle(status_message)
    while not client.is_closed :
        current_status=int(next(msgs))
        await client.change_presence(game=discord.Game(name=('level required :'+str(current_status))))
        await asyncio.sleep(4)

@client.event
async def on_message(message):
    if(data["Erased"]=="No"):
        print('Command processing enabled')
        client.process_commands(message.content)
    else:
        pass


@client.command()
async def rchars():
    await client.say(char_list)


@client.event
async def on_ready():
    print("bot is ready")
    
@client.command(pass_context=True)
async def clear(ctx,amount=2):
    channel=ctx.message.channel    
    messages=list()
    async for message in client.logs_from(channel,limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say("messages deleted")

## embed test

@client.command(pass_context=True)
async def displayembed():
    char_name="Goku"
    if(char_name in char_list):
        await client.say("you have already recruited " + char_name + "!!!! try someone else ")
        
    else:
        char_stats=data[char_name]
        list1["Total Power"]+=char_stats["Power"]
        embed=discord.Embed(title=char_name)
        embed.set_image(url='https://media.comicbook.com/2018/02/uigoku-1084889-1280x0.jpeg')
        embed.add_field(name='power level',value=9001,inline=True)
        embed.add_field(name= ('You have recruited '+ char_name),value=('Congragulations!!!! you have recruited ' + char_name),inline=False)
        char_list.append(char_name)
        write_data.write(json.dumps(data))
        await client.say(embed=embed)

## command to display all the roles in the server        

@client.command(pass_context=True)
async def getrole(ctx):
    author = ctx.message.author
    roles=author.roles
    server=ctx.message.server
    await client.say(roles[1])
    await client.say (server.roles)


## command to display every character recqruited along with the total team power

@client.command()
async def status():
    embed=discord.Embed(title="Status report")
    embed.set_image(url='https://res.cloudinary.com/teepublic/image/private/s--sKA1PPYS--/t_Preview/b_rgb:191919,c_limit,f_jpg,h_630,q_90,w_630/v1524486013/production/designs/2620176_0.jpg')
    embed.add_field(name='Current Level', value=current_level,inline=True)
    embed.add_field(name='Required level',value= current_status, inline=True)
    embed.add_field(name='Power Level',value=list1["Total Power"],inline=False)
    embed.add_field(name='Characters recruited',value=char_list,inline=False)
    await client.say(embed=embed)

## echo command

@client.command()
async def echo(*args):
    output=''

    if str(args[0]) == 'Admin':
        await client.say(list1)
    else:
        for word in args:
         output+=word
         output+=' '

    print(args[0])
    await client.say(output)

## reset the status of the server
@client.command()
async def reset_924275():
    backupdata=open('backupdata.json','r+')
    backup_data=json.load(backupdata)
    backupdata.close()
    write_data.write(json.dumps(backup_data))
    await client.say("Reset complete")

## play command for audio (test only)
@client.command(pass_context=True)
async def play(ctx,url='https://www.youtube.com/watch?v=RrkzIN2eP0U'):
    server=ctx.message.server
    voice_client=client.voice_client_in(server)
    player= await voice_client.create_ytdl_player(url)
    player.start()
    
if(__name__=='__main__'):
    client.loop.create_task(change_status())    
    client.run(TOKEN)
    print(data)




