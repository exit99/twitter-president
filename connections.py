import redis


from flask import current_app


def redis_connection(db=0):
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],
                                port=6379, db=db)
    return redis.Redis(connection_pool=pool)
