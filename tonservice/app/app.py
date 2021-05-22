import time
import asyncio
import rpcgrid.aio as rpcg
#from logger import get_logger
from logging import getLogger
from provider import MicroserviceProvider
import sys
import os
import pandas as pd
log = getLogger(__name__)
dburl = os.getenv('DB_URL', 'mysql://root@localhost:3306/market')

from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Files(Model):
    id = fields.IntField(pk=True)
    token_id = fields.IntField()
    user_id = fields.IntField()
    name = fields.TextField()
    filename = fields.TextField()
    filename_norm = fields.TextField()
    status = fields.TextField()
    processed = fields.IntField()
    failed = fields.IntField()
    created_date = fields.DatetimeField(null=True)
    finish_date = fields.DatetimeField(null=True)

    class Meta:
        table = "files"

    def __str__(self):
        return self.name

@rpcg.register
async def processing(func_name, parametrs):
    # TODO: call ton functions
    pass

async def create_microservice(loop):
    while True:

        await Tortoise.init(db_url=dburl, modules={"models": ["app"]})
        await Tortoise.generate_schemas()

        try:
            return await rpcg.create(
                provider=MicroserviceProvider(loop), loop=loop
            )
        except ConnectionError as rmq_err:
            log.warning(rmq_err)
        await asyncio.sleep(10)

async def pooling_expire(server):
    log.info('Initialize pool...')
    await asyncio.sleep(15)
    await Tortoise.init(
        db_url=dburl,
        modules={'models': ['app','__main__']}
    )
    while 1:
        try:
            await asyncio.sleep(2)
            #file = await Files.filter(id=int(4)).first()
            file = await Files.filter(status='prepare').first()
            if file is not None:
                log.info(file)
                file.status = 'proceed'
                await file.save()
                #await procceed_file_1(file.id)
        except Exception as e:
            log.error(e)
    log.info('Initialize pool done...')




def main(loop):
    server = None
    try:
        log.info('Initialize ...')
        log.info('Initialize rabbit...')
        server = loop.run_until_complete(create_microservice(loop))
        log.info('Initialize completed!')
        asyncio.gather(
            pooling_expire(server),
        )
        loop.run_until_complete(server.run())
        # loop.run_forever()
    except KeyboardInterrupt:
        log.info('Microservice stopped by user . . .')
        if server is not None:
            loop.run_until_complete(server.close())


def sigterm_handler(signum, frame):
    log.info('Terminate application')
    sys.exit(1)


if __name__ == '__main__':
    log.info(f'microservice {0.1}')
    main(asyncio.get_event_loop())
