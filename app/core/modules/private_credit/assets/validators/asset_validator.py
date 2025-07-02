def asset_validator(rate_type, indexer, fixed_rate, spread, index_percent):

    if rate_type == "PREFIXADO":
        if fixed_rate is None:
            raise ValueError("Ativos PREFIXADO devem ter fixed_rate obrigatório.")

    if rate_type == "POS-FIXADO":
        if indexer is None:
            raise ValueError("Ativos POS-FIXADO devem ter um indexer definido (ex: CDI, IPCA).")
        if indexer == "IPCA":
            if spread is None:
                raise ValueError("Ativos POS-FIXADO atrelados ao IPCA devem ter spread obrigatório.")
        elif indexer == "CDI":
            if (index_percent is None) and (spread is None):
                raise ValueError("Ativos POS-FIXADO atrelados ao CDI devem ter index_percent ou spread obrigatório.")
