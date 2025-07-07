.
├── alembic
│   ├── README
│   ├── __pycache__
│   │   └── env.cpython-310.pyc
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 2544b0164b49_create_control_modules_table.py
│       ├── 2ab8511a7185_create_movements_table.py
│       ├── 45252f22e3fa_create_control_benchmarks_table.py
│       ├── 4b6e3b2a7842_create_control_benchmarks_table.py
│       ├── 5651f72b2c30_create_private_credit_assets_table.py
│       ├── 624e07476f97_change_module_to_module_id_with_fk.py
│       ├── 7159431ae56f_rename_categories_to_private_credit_.py
│       ├── 771d17d6965d_add_fields_to_private_credit_assets_for_.py
│       ├── 7bf9db417aa6_create_snapshot_benchmarks_table.py
│       ├── 80e47424908f_create_control_benchmarks_table.py
│       ├── 8a0d08c0fe2a_add_module_id_to_category_with_foreign_.py
│       ├── 8ad0af392e0a_initial_clean_revision.py
│       ├── __pycache__
│       │   ├── 2544b0164b49_create_control_modules_table.cpython-310.pyc
│       │   ├── 2ab8511a7185_create_movements_table.cpython-310.pyc
│       │   ├── 45252f22e3fa_create_control_benchmarks_table.cpython-310.pyc
│       │   ├── 4b6e3b2a7842_create_control_benchmarks_table.cpython-310.pyc
│       │   ├── 5651f72b2c30_create_private_credit_assets_table.cpython-310.pyc
│       │   ├── 624e07476f97_change_module_to_module_id_with_fk.cpython-310.pyc
│       │   ├── 7159431ae56f_rename_categories_to_private_credit_.cpython-310.pyc
│       │   ├── 771d17d6965d_add_fields_to_private_credit_assets_for_.cpython-310.pyc
│       │   ├── 7bf9db417aa6_create_snapshot_benchmarks_table.cpython-310.pyc
│       │   ├── 80e47424908f_create_control_benchmarks_table.cpython-310.pyc
│       │   ├── 8a0d08c0fe2a_add_module_id_to_category_with_foreign_.cpython-310.pyc
│       │   ├── 8ad0af392e0a_initial_clean_revision.cpython-310.pyc
│       │   ├── c288c3ec2137_change_movement_type_enum_to_english.cpython-310.pyc
│       │   ├── c61cea3d5a82_add_unique_constraint_to_categories.cpython-310.pyc
│       │   ├── c96a6de3822f_create_control_portfolio_dates_table.cpython-310.pyc
│       │   └── f5d0d64e9001_rename_columns_first_investiment_and_.cpython-310.pyc
│       ├── c288c3ec2137_change_movement_type_enum_to_english.py
│       ├── c61cea3d5a82_add_unique_constraint_to_categories.py
│       ├── c96a6de3822f_create_control_portfolio_dates_table.py
│       └── f5d0d64e9001_rename_columns_first_investiment_and_.py
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── database.cpython-310.pyc
│   │   └── main.cpython-310.pyc
│   ├── config.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-310.pyc
│   │   ├── db
│   │   │   ├── __pycache__
│   │   │   │   └── session.cpython-310.pyc
│   │   │   └── session.py
│   │   └── modules
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   └── __init__.cpython-310.pyc
│   │       ├── control
│   │       │   ├── handlers
│   │       │   │   ├── __init__.py
│   │       │   │   ├── __pycache__
│   │       │   │   │   ├── __init__.cpython-310.pyc
│   │       │   │   │   ├── benchmark_handler.cpython-310.pyc
│   │       │   │   │   ├── module_handler.cpython-310.pyc
│   │       │   │   │   └── portfolio_date_handler.cpython-310.pyc
│   │       │   │   ├── benchmark_handler.py
│   │       │   │   ├── module_handler.py
│   │       │   │   └── portfolio_date_handler.py
│   │       │   ├── queries
│   │       │   │   └── __init__.py
│   │       │   ├── repositories
│   │       │   │   └── __init__.py
│   │       │   ├── utils
│   │       │   │   └── __init__.py
│   │       │   └── validators
│   │       │       └── __init__.py
│   │       ├── movements
│   │       │   ├── handlers
│   │       │   │   ├── __init__.py
│   │       │   │   ├── __pycache__
│   │       │   │   │   ├── __init__.cpython-310.pyc
│   │       │   │   │   ├── benchmark_handler.cpython-310.pyc
│   │       │   │   │   ├── module_handler.cpython-310.pyc
│   │       │   │   │   ├── movement_handler.cpython-310.pyc
│   │       │   │   │   └── portfolio_date_handler.cpython-310.pyc
│   │       │   │   └── movement_handler.py
│   │       │   └── services
│   │       │       ├── __pycache__
│   │       │       │   └── create_initial_movement_asset_service.cpython-310.pyc
│   │       │       └── create_initial_movement_asset_service.py
│   │       ├── private_credit
│   │       │   ├── assets
│   │       │   │   ├── handlers
│   │       │   │   │   ├── __init__.py
│   │       │   │   │   ├── __pycache__
│   │       │   │   │   │   ├── __init__.cpython-310.pyc
│   │       │   │   │   │   └── asset_handler.cpython-310.pyc
│   │       │   │   │   └── asset_handler.py
│   │       │   │   ├── services
│   │       │   │   │   ├── __pycache__
│   │       │   │   │   │   └── update_asset_position_service.cpython-310.pyc
│   │       │   │   │   └── update_asset_position_service.py
│   │       │   │   └── validators
│   │       │   │       ├── __init__.py
│   │       │   │       ├── __pycache__
│   │       │   │       │   ├── __init__.cpython-310.pyc
│   │       │   │       │   └── asset_validator.cpython-310.pyc
│   │       │   │       └── asset_validator.py
│   │       │   └── categories
│   │       │       ├── __init__.py
│   │       │       ├── __pycache__
│   │       │       │   └── __init__.cpython-310.pyc
│   │       │       └── handlers
│   │       │           ├── __init__.py
│   │       │           ├── __pycache__
│   │       │           │   ├── __init__.cpython-310.pyc
│   │       │           │   └── category_handler.cpython-310.pyc
│   │       │           └── category_handler.py
│   │       └── snapshot
│   ├── database.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── category.cpython-310.pyc
│   │   │   ├── control_benchmark.cpython-310.pyc
│   │   │   ├── control_module.cpython-310.pyc
│   │   │   ├── control_portfolio_date.cpython-310.pyc
│   │   │   ├── enums.cpython-310.pyc
│   │   │   ├── movement.cpython-310.pyc
│   │   │   ├── movements.cpython-310.pyc
│   │   │   ├── private_credit_asset.cpython-310.pyc
│   │   │   └── private_credit_category.cpython-310.pyc
│   │   ├── control
│   │   │   ├── __pycache__
│   │   │   │   ├── control_benchmark.cpython-310.pyc
│   │   │   │   ├── control_module.cpython-310.pyc
│   │   │   │   └── control_portfolio_date.cpython-310.pyc
│   │   │   ├── control_benchmark.py
│   │   │   ├── control_module.py
│   │   │   └── control_portfolio_date.py
│   │   ├── enums.py
│   │   ├── movements.py
│   │   ├── private_credit
│   │   │   ├── __pycache__
│   │   │   │   ├── private_credit_asset.cpython-310.pyc
│   │   │   │   └── private_credit_category.cpython-310.pyc
│   │   │   ├── private_credit_asset.py
│   │   │   └── private_credit_category.py
│   │   └── snapshot
│   │       └── snapshot_benchmark.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── categories.cpython-310.pyc
│   │   │   └── movements.cpython-310.pyc
│   │   ├── admin
│   │   │   ├── __pycache__
│   │   │   │   ├── benchmarks.cpython-310.pyc
│   │   │   │   ├── modules.cpython-310.pyc
│   │   │   │   └── portfolio_dates.cpython-310.pyc
│   │   │   ├── benchmarks.py
│   │   │   └── modules.py
│   │   ├── movements.py
│   │   ├── private_credit
│   │   │   ├── __pycache__
│   │   │   │   ├── assets.cpython-310.pyc
│   │   │   │   └── categories.cpython-310.pyc
│   │   │   ├── assets.py
│   │   │   └── categories.py
│   │   └── snapshot
│   │       └── snapshot_benchmarks.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── benchmark.cpython-310.pyc
│   │   │   ├── category.cpython-310.pyc
│   │   │   ├── control_benchmark.cpython-310.pyc
│   │   │   ├── control_module.cpython-310.pyc
│   │   │   ├── control_portfolio_date.cpython-310.pyc
│   │   │   ├── movement.cpython-310.pyc
│   │   │   ├── private_credit_asset.cpython-310.pyc
│   │   │   └── private_credit_category.cpython-310.pyc
│   │   ├── control_benchmark.py
│   │   ├── control_module.py
│   │   ├── control_portfolio_date.py
│   │   ├── movement.py
│   │   ├── private_credit_asset.py
│   │   ├── private_credit_category.py
│   │   └── snapshot_benchmark.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── conftest.cpython-310-pytest-8.4.1.pyc
│   │   │   ├── conftest.cpython-310.pyc
│   │   │   └── test_categories.cpython-310-pytest-8.4.1.pyc
│   │   ├── conftest.py
│   │   ├── control
│   │   │   ├── __pycache__
│   │   │   │   ├── test_benchmarks.cpython-310-pytest-8.4.1.pyc
│   │   │   │   ├── test_benchmarks_duplicate.cpython-310-pytest-8.4.1.pyc
│   │   │   │   ├── test_benchmarks_update_delete.cpython-310-pytest-8.4.1.pyc
│   │   │   │   ├── test_benchmarks_validation.cpython-310-pytest-8.4.1.pyc
│   │   │   │   └── test_modules.cpython-310-pytest-8.4.1.pyc
│   │   │   ├── test_benchmarks.py
│   │   │   └── test_modules.py
│   │   ├── movements
│   │   │   ├── __pycache__
│   │   │   │   └── test_movements.cpython-310-pytest-8.4.1.pyc
│   │   │   └── test_movements.py
│   │   └── private_credit
│   │       ├── __pycache__
│   │       │   ├── test_assets.cpython-310-pytest-8.4.1.pyc
│   │       │   └── test_categories.cpython-310-pytest-8.4.1.pyc
│   │       ├── test_assets.py
│   │       └── test_categories.py
│   └── utils
│       └── __init__.py
├── docker-compose.yml
├── docs
│   ├── bechmark.md
│   ├── comands.md
│   ├── development_tracker.md
│   ├── path_structure.md
│   └── technical.md
└── requirements.txt