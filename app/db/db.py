from app.db.base import Base, engine
from app.models import user_model, rate_limit, analysis_model

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")