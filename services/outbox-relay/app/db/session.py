from decision_db.session_factory import create_session_factory
from app.configurations.settings_config import settings

SessionLocal = create_session_factory(settings.database_url)

