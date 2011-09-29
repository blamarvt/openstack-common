import openstack.common.db.sqlalchemy.creator as common_creator
import openstack.common.db.sqlalchemy.creators.mysql as mysql_creator
import openstack.common.db.sqlalchemy.creators.sqlite as sqlite_creator


def get_creator(connection_str, **kwargs):
    """Create the appropriate 'creator' using a connection string."""
    if connection_str.startswith("mysql"):
        return mysql_creator.MySQLCreator(connection_str, **kwargs)
    elif connection_str.startswith("sqlite"):
        return sqlite_creator.SQLiteCreator(connection_str, **kwargs)
    else:
        return common_creator.Creator(connection_str, **kwargs)
