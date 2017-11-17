import pymongo
import logging


class Utils(object):
    """
    Class providing external services instances
    """

    def __init__(self, config):
        self.config = config

    def get_db(self, db_name=None):
        """ Simple function to wrap getting a database connection from the connection pool.
        Args:
            db_name: The database name from where we want a connection.
        Returns:
            A database instance, if existing.
        """
        db = None
        if db_name is not None:
            db = db_name
        else:
            db = self.config.get('mongo','MONGO_TEST_DB')
        host = self.config.get('mongo','MONGO_HOST')
        port = int(self.config.get('mongo','MONGO_PORT'))

        return pymongo.MongoClient(host=host,port=port)[db]
