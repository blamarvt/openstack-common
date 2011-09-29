from __future__ import absolute_import

import sqlalchemy


class Creator(object):
    """Allows for standard creation of SQLAlchemy engines and sessionmakers."""

    def __init__(self, connection_str, **kwargs):
        """Initialize a new SQLAlchemy creator.

        :param connection_str: The SQL connection string to use.
        :param echo: If True, all SQL will be echoed to the engine's logger.
        :param min_pool_size: The minimum number of db connections to use.
        :param max_pool_size: The maximum number of db connections to use.
        :param idle_timeout: Time (in seconds) to keep around idle connections.
        :param pool_timeout: Maximum time to wait for connection from pool.
        :param autocommit: If True, the session does not keep a persistent
                           transaction running.
        :param expire_on_commit: If True, all instances will expire after
                                 commit.
        :returns: None

        """
        self._connection_str = connection_str
        self._connection_dict = sqlalchemy.engine.url.make_url(connection_str)
        self._echo = kwargs.get("echo", False)
        self._min_pool_size = kwargs.get("min_pool_size", 1)
        self._max_pool_size = kwargs.get("max_pool_size", 2)
        self._idle_timeout = kwargs.get("idle_timeout", 30)
        self._pool_timeout = kwargs.get("pool_timeout", 30)
        self._autocommit = kwargs.get("autocommit", True)
        self._expire_on_commit = kwargs.get("expire_on_commit", False)
        self._engine = None
        self._maker = None

    @property
    def engine_args(self):
        """Return the arguments used to create this engine."""
        return {
            "echo": self._echo,
            "pool_recycle": self._idle_timeout,
        }

    @property
    def engine(self):
        """Return a SQLAlchemy engine."""
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(self._connection_str,
                                                    **self.engine_args)
        return self._engine

    @property
    def sessionmaker(self):
        """Return a SQLAlchemy sessionmaker."""
        if self._maker is None:
            self._maker = sqlalchemy.orm.sessionmaker(bind=self.engine,
                                       autocommit=self._autocommit,
                                       expire_on_commit=self._expire_on_commit)
        return self._maker
