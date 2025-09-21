import os

# Global toggle for developer diagnostics (Author Mode).
# Set to True during development, and set to False for production.
# Environment override: APP_AUTHOR_MODE=1 enables author mode.

AUTHOR_MODE = False

env_val = os.getenv("APP_AUTHOR_MODE")
if env_val is not None:
    AUTHOR_MODE = env_val.strip() in {"1", "true", "True", "YES", "yes"}

