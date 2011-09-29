import eventlet.db_pool
import MySQLdb

import openstack.common.db.sqlalchemy.creator


class MySQLCreator(openstack.common.db.sqlalchemy.creator.Creator):

    def __init__(self, connection_str, **kwargs):
        """Initialize a new MySQL SQLAlchemy engine creator.

        If the MySQLdb module is present, this will use an eventlet db_pool
        connection pool to connect to MySQL.

        :param connection_str: The SQL connection string to use.
        :param idle_timeout: Time (in seconds) to keep around idle connections.
        :param echo: If True, all SQL will be echoed to the engine's logger.
        :param min_pool_size: The minimum number of db connections to use.
        :param max_pool_size: The maximum number of db connections to use.
        :param pool_timeout: Maximum time to wait for connection from pool.
        :param idle_timeout: Maximum time to keep around idle connection.
        :returns: None

        """
        super(MySQLCreator, self).__init__(connection_str, **kwargs)

    @property
    def pool_args(self):
        """Return the arguments used to create the db_pool connection pool."""
        return {
            "db": self._connection_dict.database,
            "passwd": self._connection_dict.password or "",
            "host": self._connection_dict.host,
            "user": self._connection_dict.username,
            "min_size": self._min_pool_size,
            "max_size": self._max_pool_size,
            "max_idle": self._idle_timeout,
        }

    @property
    def creator(self):
        """Generate and return a method which can create SQL connections."""
        return eventlet.db_pool.ConnectionPool(MySQLdb,
                                               **self.pool_args).create

    @property
    def engine_args(self):
        """Return the arguments used to create this engine."""
        return {
            "echo": self._echo,
            "pool_recycle": self._idle_timeout,
            "pool_size": self._max_pool_size,
            "pool_timeout": self._pool_timeout,
            "creator": self.creator,
        }
