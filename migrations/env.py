import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.config import settings

from app.db.base import Base 

from app.models import (user , organization , project , task , comment , attachment , project_member )

config = context.config # get alembic config object

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.config import settings
from app.db.base import Base 

# Import đầy đủ models
from app.models import (
    user, 
    organization, 
    project, 
    task, 
    comment, 
    attachment, 
    project_member
)
# Lấy cấu hình Alembic
config = context.config

# Cập nhật URL Database
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations (connection : Connection) -> None:
    context.configure(
        connection= connection,
        target_metadata= target_metadata,
        compare_type= True,
    )
    with context.begin_transaction():
        context.run_migrations()
async def run_migrations_online() -> None:
    # create async engine
    connectable = async_engine_from_config (
        config.get_section (config.config_ini_section ),
        prefix= "sqlalchemy.",
        poolclass= pool . NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()
if context.is_offline_mode():
    do_run_migrations (context . connection )
else:
    asyncio.run (run_migrations_online ())