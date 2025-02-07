# -*- coding: utf-8 -*-
#!/usr/bin/env python
""" Module for simple behaviors for the slack bot
"""

import re
import random
import traceback
import six

import slackbot.bot
# pylint: disable=protected-access

def user(msg):
    """ Return the user for a message

        :param msg: Slack message
    """
    return msg._client.users[msg._get_user_id()]['name']

SHENANISTRING = '''what's the name of that place you like with all the goofy\
 shit on the walls?'''
SHENANIGANS = [SHENANISTRING, re.IGNORECASE]
@slackbot.bot.respond_to(*SHENANIGANS)
def shenanigans(message):
    '''@mention with r'what's the name of that \
place you like with all the goofy shit on the walls?'
Example: @bot what's the name of that place you like with all the goofy shit \
on the walls?'''
    message.reply('You mean Shenanigans? You guys talkin\' \'bout\
 shenanigans?')

HI = re.compile(r'hi(|!)$', re.IGNORECASE)
@slackbot.bot.respond_to(HI)
def hi(message, groups):  # pylint: disable=unused-argument,invalid-name
    '''@mention with r'hi(|!)$'
Example: @bot hi!'''
    message.reply('Yo!')

TOWELSTRING = '''you're a towel'''
TOWEL = re.compile(TOWELSTRING, re.IGNORECASE)
@slackbot.bot.listen_to(TOWEL)
def towel(message):
    '''Use the string r'you\'re a towel'
Example: hey, you're a towel, guy!'''
    message.reply('''YOU'RE a towel!''')

PYTHONTOWELSTRING = '''you're a (bot|python|robot) towel'''
PYTHONTOWEL = re.compile(PYTHONTOWELSTRING, re.IGNORECASE)
@slackbot.bot.listen_to(PYTHONTOWEL)
def ura(message):
    '''Use the string r'you\'re a (bot|python|robot) towel'
Example: hey, you're a bot towel, buddy!'''
    message.reply('''What did you say?!''')

MARTINSTRING = '''martin'''
MARTIN = re.compile(MARTINSTRING, re.IGNORECASE)
@slackbot.bot.listen_to(MARTIN)
def martin(message):
    '''Use the string r'martin'
Example: Yesterday Martin did a thing.'''
    message.reply('''s/Martin/1950's newscast guy/g''')

GROUPSTRING = r'''^roll\sdice
                  $|\s
                  ((\s*[\d]+d[\d]+)+)
                  ($|\swith\s.*\smodifier(|s)\s((\s*[\+-]\d+)+))'''
GROUPS = re.compile(GROUPSTRING, re.IGNORECASE | re.VERBOSE)
@slackbot.bot.respond_to(GROUPS)
def roll_dice(message, *groups):
    r'''@mention with r'^roll\sdice
               $|\s
               ((\s*[\d]+d[\d]+)+)
               ($|\swith\s.*\smodifier(|s)\s((\s*[\+-]\d+)+))'
Example: roll dice 1d4 2d6 with butts modifier +1'''
    try:
        dice = groups[0]
        try:
            modifiers = groups[4].split()
            modifiers = [int(m) for m in modifiers]
        except AttributeError:
            modifiers = [0]
        if not dice:
            total = random.randint(1, 6)
            results = ['1d6: %d' % total]
        else:
            dice_sets = dice.split()
            total = 0
            results = []
            for dice_set in dice_sets:
                nums = dice_set.split('d')
                number = int(nums[0])
                size = int(nums[1])
                val = sum([random.randint(1, size) for i in range(number)])
                val += sum(modifiers)
                total += val
                results.append('%s: %d' % (dice_set, val))
        results = ', '.join(results)
        message.reply(f"Got dice sets: {results}\nTotal: {total}")
    except:  # pylint: disable=bare-except
        print(traceback.format_exc())

SPINSTRING = r'''spin\sthe\swheel'''
SPIN = re.compile(SPINSTRING, re.IGNORECASE | re.VERBOSE)
@slackbot.bot.respond_to(SPIN)
def spin_wheel(message):
    r'''@mention with r'spin\sthe\swheel.
Example: @bot spin the wheel'''
    values = range(5, 105, 5)
    message.reply(str(random.choice(values)))

PINGSTRING = r'''^([^\w\s]*|_*)
                  ([a-zA-Z-_]+)
                  ING(S?)
                  ([^\w\s]*|_*)
                  (\sME(\s.*)?)?$'''
PING = re.compile(PINGSTRING, re.IGNORECASE | re.VERBOSE)
@slackbot.bot.listen_to(PING)
def ping(message, *groups):
    '''Use a string with 'ing' in it.
Examples: fling, *ding*, ping me'''
    letter = groups[1]
    pre, suf = groups[0], groups[3]
    msg = 'ong' if letter[-1].islower() else 'ONG'
    msg += 's' if groups[2] and groups[2].islower() else 'S' if groups[2] else ''
    msg = pre+letter+msg+suf
    msg = 'Actually, it\'s "%s"' % msg
    message.reply(msg)

WHELPSTRING = '''whelps'''
WHELPS = re.compile(WHELPSTRING, re.IGNORECASE)
@slackbot.bot.listen_to(WHELPS)
def whelps(message):
    '''Use a string with 'whelps' in it.
Example: I fucked up. #whelps'''
    for i in ['WHELPS', 'LEFT SIDE', 'EVEN SIDE',
              'MANY WHELPS', 'NOW', 'HANDLE IT!']:
        message.reply(i)

FIXITSTRING = '''fixit'''
FIXIT = re.compile(FIXITSTRING, re.IGNORECASE)
@slackbot.bot.listen_to(FIXIT)
def fixit(message):
    '''Use a string with 'fixit' in it.
Example: You broked it. FIXIT'''
    message.reply('https://www.youtube.com/watch?v=8ZCysBT5Kec')

FINESTRING = r'''this\sis\sfine'''
FINE = re.compile(FINESTRING, re.IGNORECASE)
@slackbot.bot.listen_to(FINE)
def this_is_fine(message):
    '''Use a string with 'this is fine' in it.
Example: I fucked up. This is fine.'''
    message.reply('http://gunshowcomic.com/648')

GREATDAYSTRING = r'''(it's\sgonna\sbe\sa\s)*
                    great\sday'''
GREATDAY = re.compile(GREATDAYSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.listen_to(GREATDAY)
def great_day(message, *groups):  # pylint: disable=unused-argument
    '''Use a string with '(it\'s gonna be a )great day'
Examples: You had a great day!
          It's gonna be a great day.'''
    message.reply('https://www.youtube.com/watch?v=WRu_-9MBpd4')

SPENDSTRING = r'''can\s
                     (.*)\s
                     spend\s
                     (this|that|the)\s
                     money'''
SPEND = re.compile(SPENDSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.listen_to(SPEND)
def can_spend(message, *groups):  # pylint: disable=unused-argument
    '''Use a string containing the format:
r'can .* spend (this|that|the) money'
Example: Hey, can Brian spend that money?'''
    message.reply('http://brianauron.info/CanBobiSpendThisMoney')

HADDAWAYSTRING = r'''(|,)\s
                     what\sis\slove\?*$'''
HADDAWAY = re.compile(HADDAWAYSTRING, re.IGNORECASE|re.VERBOSE)
@slackbot.bot.listen_to(HADDAWAY)
def what_is_love(message, *groups):  # pylint: disable=unused-argument
    '''Use a string containing the format:
r'(|,) what is love?*$
Example: Hey, what is love?'''
    message.reply('Baby don\'t hurt me!  https://www.youtube.com/watch?v=JRVfysTXhNA')

MANATEESTRING = '''[A-Z]{3}'''
MANATEE = re.compile(MANATEESTRING)
@slackbot.bot.listen_to(MANATEE)
def manatee_maybe(message):
    '''Voice your anger.'''
    msg = message.body['text']
    nicks = [j['name'] for i, j in message._client.users.items()]
    if msg == msg.upper() and len(msg) > 4 and msg.lower() not in nicks:
        manatee = random.randint(1, 34)
        reply = 'http://brianauron.info.s3-website.us-west-2.amazonaws.com/img/manatees/manatee%s.jpg' % manatee
    else:
        return
    message.reply(reply)

PORTLANDSTRING = r'''tell\s(.+)\sto\scome\sto\sPortland'''
PORTLAND = re.compile(PORTLANDSTRING, re.I)
@slackbot.bot.respond_to(PORTLAND)
def come_to_portland(message, *groups):
    '''@mention to tell the bot to tell somebody to come to Portland
Example: @bot tell @user1234 to come to Portland'''
    who = groups[0]
    message.send('@'+who+': http://i.imgur.com/29hMr0h.jpg')

SEATTLESTRING = r'''tell\s(.+)\sto\scome\sto\sSeattle'''
SEATTLE = re.compile(SEATTLESTRING, re.I)
@slackbot.bot.respond_to(SEATTLE)
def come_to_seattle(message, *groups):
    '''@mention to tell the bot to tell somebody to come to Seattle
Example: @bot tell @user1234 to come to Seattle'''
    who = groups[0]
    message.send('@'+who+': http://i.imgur.com/Lwo0CTF.gif')

CLEVELANDSTRING = r'''tell\s(.+)\sto\scome\sto\sCleveland'''
CLEVELAND = re.compile(CLEVELANDSTRING, re.I)
@slackbot.bot.respond_to(CLEVELAND)
def come_to_cleveland(message, *groups):
    '''@mention to tell the bot to tell somebody to come to Cleveland
Example: @bot tell @user1234 to come to Cleveland'''
    who = groups[0]
    message.send('@'+who+': https://www.youtube.com/watch?v=ysmLA5TqbIY')

ENHANCESTRING = r'''enhance'''
ENHANCE = re.compile(ENHANCESTRING, re.I)
@slackbot.bot.listen_to(ENHANCE)
def enhance(message):
    '''Enhance!'''
    message.send('/me types furiously. "Enhance."')

FLARESTRING = r'''flare(\s(that|it)\sfor\s(me|us))?'''
FLARE = re.compile(FLARESTRING, re.I)
@slackbot.bot.listen_to(FLARE)
def flare_that_for_you(message, *groups):
    '''Deep Rock Galactic flares requested. Toss flares!'''
    message.send('`FFFF` :sparkler::sparkler::sparkler::sparkler:')

BADGERSTRING = r'''.*'''
BADGER = re.compile(BADGERSTRING, re.I)
@slackbot.bot.listen_to(BADGER)
def flare_that_for_you(message, *groups):
    '''Reply to every message from Badger in a thread'''
    udi = message._get_user_id()  # pylint: disable=protected-access
    try:
        name = message._client.users[udi]['name']
    except KeyError:
        return
    if name == 'fishmanpet' and random.randint(1,10) == 4: # chosen by fair dice roll
        message.reply('FFFFBPBBTHPFBPTHPBFTHPPP! :tongue:', in_thread=True)

@slackbot.bot.respond_to(re.compile('h[ae]lp', re.I))
def explore(message, *groups):  # pylint: disable=unused-argument
    '''@mention the bot with 'help' for this message.'''
    udi = message._get_user_id()  # pylint: disable=protected-access
    name = message._client.users[udi]['name']
    (message  # pylint: disable=protected-access
     ._client
     .send_message(f'@{name}',
                   'Respond to:'))
    (message  # pylint: disable=protected-access
     ._client
     .send_message(f'@{name}',
                   message.docs_reply()))
    (message  # pylint: disable=protected-access
     ._client
     .send_message(f'@{name}',
                   'Listen to:'))
    reply = [f"    • `{v.__name__}` {v.__doc__ or ''}"
             for _, v in six.iteritems(message._plugins.commands['listen_to'])]  # pylint: disable=protected-access
    (message  # pylint: disable=protected-access
     ._client
     .send_message(f"@{name}", "\n".join(reply)))
