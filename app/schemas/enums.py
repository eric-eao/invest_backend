from enum import Enum

class CurrencyEnum(str, Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"

# ======================================================
# Rate Periods
# ======================================================
class RatePeriod(str, Enum):
    daily = "daily"
    monthly = "monthly"
    annual = "annual"

# ======================================================
# Rate Types
# ======================================================
class RateType(str, Enum):
    PREFIXADO = "PREFIXADO"
    POS_FIXADO = "POS_FIXADO"

# ======================================================
# Indexers
# ======================================================
class Indexer(str, Enum):
    CDI = "CDI"
    IPCA = "IPCA"

# ======================================================
# Movement Types
# ======================================================
class MovementType(str, Enum):
    DEPOSIT = "DEPOSIT"                         # aporte
    FULL_REDEMPTION = "FULL_REDEMPTION"         # resgate total
    PARTIAL_REDEMPTION = "PARTIAL_REDEMPTION"   # resgate parcial

# ======================================================
# Movement Statuses
# ======================================================
class MovementStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
