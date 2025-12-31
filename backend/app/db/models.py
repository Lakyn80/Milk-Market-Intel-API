# Central model registry
# Importing models here ensures SQLAlchemy metadata is aware of them

from app.modules.companies.models import Company  # noqa
from app.modules.companies.brand_models import Brand  # noqa
from app.modules.companies.product_models import Product  # noqa
from app.modules.companies.price_models import Price  # noqa
