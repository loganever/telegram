import configparser
import time
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import PeerChannel
import xlwt


if __name__ == '__main__':
    # read config
    con = configparser.ConfigParser()
    con.read("config.ini", encoding='utf-8')
    telegram = dict(con.items('telegram'))
    channel = dict(con.items('channel'))
    save = dict(con.items('save'))

    api_id = int(telegram['api_id'])
    api_hash = telegram['api_hash']
    username = telegram['username']

    # create client
    client = TelegramClient(username, api_id, api_hash)
    client.start()

    # create channel
    if channel['channel'].isdigit():
        entity = PeerChannel(int(channel['channel']))
    else:
        entity = channel['channel']
    my_channel = client.get_entity(entity)

    # get history chat
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = int(channel['max_message'])

    while True:
        history = client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        time.sleep(0.5)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    filter_messages = []
    for message in all_messages:
        filter_messages.append({"id":message["id"], "channel_id":message["peer_id"]["channel_id"], "date":message["date"], "content":message["message"], "from":{"id":message["from_id"]["user_id"], "_":message["from_id"]["_"]}})

    # save
    wb = xlwt.Workbook()
    ws = wb.add_sheet('result', cell_overwrite_ok=True)
    ws.write(0, 0, "messge_id")
    ws.write(0, 1, "channel_id")
    ws.write(0, 2, "date")
    ws.write(0, 3, "content")
    ws.write(0, 4, "from")
    for i in range(len(filter_messages)):
        ws.write(i + 1, 0, filter_messages[i]['id'])
        ws.write(i + 1, 1, filter_messages[i]['channel_id'])
        ws.write(i + 1, 2, str(filter_messages[i]['date']))
        ws.write(i + 1, 3, filter_messages[i]['content'])
        ws.write(i + 1, 4, filter_messages[i]['from']['id'])
    wb.save(save['filepath'])
