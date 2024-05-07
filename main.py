import asyncio
import Parser
import bot
import logging
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(bot.botStart())
    except KeyboardInterrupt:
        print('Exit')