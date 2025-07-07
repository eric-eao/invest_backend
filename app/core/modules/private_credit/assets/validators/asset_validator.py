def asset_validator(rate_type, indexer, fixed_rate, spread, index_percent):
    """
    Valida os parâmetros de um ativo conforme o tipo de rentabilidade
    """

    if rate_type == "PREFIXADO":
        if fixed_rate is None:
            raise ValueError("Ativos PREFIXADO devem ter fixed_rate obrigatório.")

    elif rate_type == "POS-FIXADO":
        if indexer is None:
            raise ValueError("Ativos POS-FIXADO devem ter um indexer definido (ex: CDI, IPCA).")
        if indexer == "IPCA":
            if spread is None:
                raise ValueError("Ativos POS-FIXADO atrelados ao IPCA devem ter spread obrigatório.")
        elif indexer == "CDI":
            if (index_percent is None) and (spread is None):
                raise ValueError("Ativos POS-FIXADO atrelados ao CDI devem ter index_percent ou spread obrigatório.")
        else:
            raise ValueError(f"Indexer inválido para POS-FIXADO: {indexer}")

    else:
        raise ValueError(f"Tipo de rentabilidade inválido: {rate_type}")
