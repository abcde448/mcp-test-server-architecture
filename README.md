# MCP Test Server Architecture

A minimal, test-focused MCP (Model Context Protocol) server built using FastAPI, designed to demonstrate clean architecture, tool registration, validation, and automated testing.

---

## 📌 Overview

This project implements a basic MCP server with:
- Clear separation of concerns (server, tools, schemas, tests)
- Tool execution via a registry pattern
- Input validation and structured error handling
- Automated testing using pytest

The goal is to provide a clean and extensible reference architecture for MCP-style servers.

---

## 🏗 Project Structure

# MCP Test Server Architecture

A minimal, test-focused MCP (Model Context Protocol) server built using FastAPI, designed to demonstrate clean architecture, tool registration, validation, and automated testing.

---

## 📌 Overview

This project implements a basic MCP server with:
- Clear separation of concerns (server, tools, schemas, tests)
- Tool execution via a registry pattern
- Input validation and structured error handling
- Automated testing using pytest

The goal is to provide a clean and extensible reference architecture for MCP-style servers.

---

## 🏗 Project Structure

mcp-test-server-architecture/
├── architecture/ # Architecture notes & diagrams
├── server/
│ ├── main.py # FastAPI entry point
│ ├── registry.py # Tool registry & execution logic
│ ├── config.py # Server configuration
│ ├── schemas/ # Pydantic request/response schemas
│ ├── tools/ # MCP tools (e.g. add_numbers, dummy_tool)
│ └── tests/ # Pytest-based test suite
├── pytest.ini # Pytest configuration
├── requirements.txt # Dependencies
├── run_tests.py # Test runner script
└── README.md


---

## ⚙️ Tech Stack

- Python 3.9+
- FastAPI
- Pydantic
- Pytest

---

## 🚀 Setup & Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


##Run the server
python server/main.py

🧪 Testing

##Run all tests from the project root:
python -m pytest
python -m pytest
✅ All tests are passing successfully


🎯 Key Highlights
Modular MCP server design
Tool-based execution model
Strong validation & error handling
Clean, reproducible test setup
Easy to extend with new tools


📎 Status
Architecture: Completed
Implementation: Completed
Testing: Completed (All tests passing)


Author
Md. Rabbi Hasan


