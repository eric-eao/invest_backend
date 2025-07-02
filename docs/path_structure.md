## 🧩 Estrutura de Pastas

.
├── alembic
│   ├── README
│   ├── __pycache__
│   │   └── env.cpython-310.pyc
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 2544b0164b49_create_control_modules_table.py
│       ├── 45252f22e3fa_create_control_benchmarks_table.py
│       ├── 4b6e3b2a7842_create_control_benchmarks_table.py
│       ├── 7159431ae56f_rename_categories_to_private_credit_.py
│       ├── 80e47424908f_create_control_benchmarks_table.py
│       ├── 8ad0af392e0a_initial_clean_revision.py
│       ├── __pycache__
│       │   ├── 2544b0164b49_create_control_modules_table.cpython-310.pyc
│       │   ├── 45252f22e3fa_create_control_benchmarks_table.cpython-310.pyc
│       │   ├── 4b6e3b2a7842_create_control_benchmarks_table.cpython-310.pyc
│       │   ├── 7159431ae56f_rename_categories_to_private_credit_.cpython-310.pyc
│       │   ├── 80e47424908f_create_control_benchmarks_table.cpython-310.pyc
│       │   ├── 8ad0af392e0a_initial_clean_revision.cpython-310.pyc
│       │   ├── c61cea3d5a82_add_unique_constraint_to_categories.cpython-310.pyc
│       │   └── c96a6de3822f_create_control_portfolio_dates_table.cpython-310.pyc
│       ├── c61cea3d5a82_add_unique_constraint_to_categories.py
│       └── c96a6de3822f_create_control_portfolio_dates_table.py
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
│   │       └── private_credit
│   │           ├── categories
│   │           │   ├── __init__.py
│   │           │   ├── __pycache__
│   │           │   │   └── __init__.cpython-310.pyc
│   │           │   ├── handlers
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __pycache__
│   │           │   │   │   ├── __init__.cpython-310.pyc
│   │           │   │   │   └── category_handler.cpython-310.pyc
│   │           │   │   └── category_handler.py
│   │           │   ├── queries
│   │           │   │   └── __init__.py
│   │           │   ├── repositories
│   │           │   │   └── __init__.py
│   │           │   ├── utils
│   │           │   │   └── __init__.py
│   │           │   └── validators
│   │           │       └── __init__.py
│   │           └── movements
│   │               ├── __init__.py
│   │               ├── handlers
│   │               │   └── __init__.py
│   │               ├── queries
│   │               │   └── __init__.py
│   │               ├── repositories
│   │               │   └── __init__.py
│   │               ├── utils
│   │               │   └── __init__.py
│   │               └── validators
│   │                   └── __init__.py
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
│   │   │   └── private_credit_category.cpython-310.pyc
│   │   ├── control_benchmark.py
│   │   ├── control_module.py
│   │   ├── control_portfolio_date.py
│   │   ├── enums.py
│   │   └── private_credit_category.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── categories.cpython-310.pyc
│   │   ├── admin
│   │   │   ├── __pycache__
│   │   │   │   ├── benchmarks.cpython-310.pyc
│   │   │   │   ├── modules.cpython-310.pyc
│   │   │   │   └── portfolio_dates.cpython-310.pyc
│   │   │   ├── benchmarks.py
│   │   │   ├── modules.py
│   │   │   └── portfolio_dates.py
│   │   └── categories.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── benchmark.cpython-310.pyc
│   │   │   ├── category.cpython-310.pyc
│   │   │   ├── control_benchmark.cpython-310.pyc
│   │   │   ├── control_module.cpython-310.pyc
│   │   │   ├── control_portfolio_date.cpython-310.pyc
│   │   │   └── private_credit_category.cpython-310.pyc
│   │   ├── control_benchmark.py
│   │   ├── control_module.py
│   │   ├── control_portfolio_date.py
│   │   └── private_credit_category.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── conftest.cpython-310-pytest-8.4.1.pyc
│   │   │   ├── conftest.cpython-310.pyc
│   │   │   └── test_categories.cpython-310-pytest-8.4.1.pyc
│   │   ├── conftest.py
│   │   └── test_categories.py
│   └── utils
│       └── __init__.py
├── docker-compose.yml
├── docs
│   ├── comands.md
│   ├── development_tracker.md
│   ├── path_structure.md
│   └── technical.md
└── requirements.txt