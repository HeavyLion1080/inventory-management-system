# Inventory Management System 

A command-line Inventory Management System built with Python and SQLite.  
This project demonstrates practical backend development skills including CRUD operations, persistent storage, input validation, and clean CLI design.

## Features

- Create, read, update, and delete inventory items (CRUD)
- Persistent storage using SQLite
- Input validation for all user inputs
- Optional pricing support (NULL values handled correctly)
- Clean, formatted table output for inventory listings
- Confirmation prompts for destructive actions (update/delete)
- Simple and intuitive command-line interface

## Technologies Used

- Python 3
- SQLite
- Python Standard Library (`sqlite3`)
- Git / GitHub

## Project Structure

```
inventory-management-system/
├── inventory.py # Main application
├── README.md # Project documentation
└── .gitignore # Git ignore rules
```

> The SQLite database file (`inventory.db`) is created automatically at runtime and is excluded from version control.

## How It Works

Each inventory item contains:
- `id` (auto-incremented primary key)
- `name`
- `quantity`
- `price` (optional)

The system allows users to:
- Add new items with validation
- View all items in a formatted table
- Update existing items while keeping current values if desired
- Clear prices or set them to NULL
- Delete items with confirmation
- Exit cleanly while closing the database connection

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/HeavyLion1080/inventory-management-system.git
cd inventory-management-system
```

### 2. Run the Application
```bash
python inventory.py
```