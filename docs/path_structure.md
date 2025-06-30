## 🧩 Estrutura de Pastas

.
├── alembic
│   ├── README
│   ├── __pycache__
│   │   └── env.cpython-310.pyc
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 5408f267740b_create_categories_table.py
│       └── __pycache__
│           └── 5408f267740b_create_categories_table.cpython-310.pyc
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
│   │   ├── categories
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   └── __init__.cpython-310.pyc
│   │   │   ├── handlers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   │   └── category_handler.cpython-310.pyc
│   │   │   │   └── category_handler.py
│   │   │   ├── queries
│   │   │   │   └── __init__.py
│   │   │   ├── repositories
│   │   │   │   └── __init__.py
│   │   │   ├── utils
│   │   │   │   └── __init__.py
│   │   │   └── validators
│   │   │       └── __init__.py
│   │   ├── db
│   │   │   ├── __pycache__
│   │   │   │   └── session.cpython-310.pyc
│   │   │   └── session.py
│   │   └── movements
│   │       ├── __init__.py
│   │       ├── handlers
│   │       │   └── __init__.py
│   │       ├── queries
│   │       │   └── __init__.py
│   │       ├── repositories
│   │       │   └── __init__.py
│   │       ├── utils
│   │       │   └── __init__.py
│   │       └── validators
│   │           └── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── category.cpython-310.pyc
│   │   │   └── enums.cpython-310.pyc
│   │   ├── category.py
│   │   └── enums.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── categories.cpython-310.pyc
│   │   └── categories.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── category.cpython-310.pyc
│   │   └── category.py
│   ├── tests
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── docker-compose.yml
├── docs
│   ├── comands.md
│   ├── development_tracker.md
│   ├── path_structure.md
│   └── technical.md
└── requirements.txt