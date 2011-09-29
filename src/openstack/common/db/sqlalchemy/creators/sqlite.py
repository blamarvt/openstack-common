import sqlalchemy

import openstack.common.db.sqlalchemy.creator


class SQLiteCreator(openstack.common.db.sqlalchemy.creator.Creator):

    def __init__(self, connection_str, **kwargs):
        """Initialize a new SQLite SQLAlchemy engine creator.

        :param connection_str: The SQL connection string to use.
        :param idle_timeout: Time (in seconds) to keep around idle connections.
        :param echo: If True, all SQL will be echoed to the engine's logger.
        :returns: None

        """
        super(SQLiteCreator, self).__init__(connection_str, **kwargs)
        self._pool_class = sqlalchemy.pool.NullPool

    @property
    def engine_args(self):
        """Return the arguments used to create this engine."""
        return {
            "echo": self._echo,
            "poolclass": self._pool_class,
            "pool_recycle": self._idle_timeout,
        }
