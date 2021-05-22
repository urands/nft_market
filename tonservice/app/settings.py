import os

TON_SERVICE_VERSION = '0.0.1'

DB_URL = 'sqlite:///db.sqlite3'
DB_UPDATE_SCHEMA = True

RMQ_URL =  os.getenv('RMQ_URL', 'amqp://guest:guest@localhost')
RMQ_MASTER_QUEUE = 'ton_watcher'
RMQ_REMOTE_QUEUE = 'ton'
RMQ_EVENT_QUEUE = 'ton_events'
RMQ_NAME = 'ton_watcher'

