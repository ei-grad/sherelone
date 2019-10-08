import redis

CLIENT_ID = '...'
CLIENT_SECRET = '...'
SESSION_TYPE = 'redis'
SESSION_REDIS = redis.Redis(host='redis')
