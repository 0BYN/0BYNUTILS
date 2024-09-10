from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pkg_resources
import importlib
import logging

# Create a base class for all models to inherit from
Base = declarative_base()

async def setup_database(bot):
    """Set up the database connection and import models from all plugins."""
    database_url = f"postgresql+asyncpg://{bot.config['database']['user']}:" \
                   f"{bot.config['database']['password']}@{bot.config['database']['host']}" \
                   f":{bot.config['database']['port']}/{bot.config['database']['database']}"

    # Create the async database engine
    engine = create_async_engine(database_url, echo=True)

    # Create a session
    bot.db_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )()

    # Discover and import all models from installed plugins
    _discover_and_import_models()

    # Create all tables in the database (if they don't already exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def _discover_and_import_models():
    """Automatically discover and import models from all installed plugins."""
    logger = logging.getLogger("database")
    logger.info("Discovering and importing models from installed plugins...")

    for dist in pkg_resources.working_set:
        if dist.project_name.startswith("obyn"):  # Assuming plugin naming convention
            plugin_name = dist.project_name.replace("obyn-", "")
            try:
                # Dynamically import the models.py file from each plugin
                models_module = importlib.import_module(f"plugins.{plugin_name}.models")

                # Register the models (they should already inherit from `Base`)
                logger.info(f"Imported models from {plugin_name}")
            except ModuleNotFoundError:
                logger.warning(f"No models found for plugin {plugin_name}")
            except Exception as e:
                logger.error(f"Failed to import models from plugin {plugin_name}: {e}")
