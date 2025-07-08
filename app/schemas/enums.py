# app/schemas/enums.py

from enum import Enum


class RateType(str, Enum):
    PREFIXADO = "PREFIXADO"
    POS_FIXADO = "POS_FIXADO"


class Indexer(str, Enum):
    CDI = "CDI"
    IPCA = "IPCA"
