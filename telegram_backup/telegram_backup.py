# !/usr/bin/env python3
import logging
from telethon import TelegramClient

api_id = 1234567  # your telegram api id
api_hash = '123abc'  # your telegram api hash

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('tg_backup', api_id, api_hash)


async def main():
    with open('tg_backup.log', 'w+', encoding='utf-8') as f:
        async for dialog in client.iter_dialogs():
            if dialog.is_user:
                dialog_type = '用户/机器人'
            elif dialog.is_group:
                dialog_type = '群组'
            elif dialog.is_channel:
                dialog_type = '频道'
            logger.info(f'联系人ID：{dialog.id}------联系人昵称：{dialog.title}------联系人类型：{dialog_type}')
            f.write(f'{dialog.id}------{dialog.title}------联系人类型：{dialog_type}\n')


with client:
    client.loop.run_until_complete(main())
