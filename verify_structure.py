#!/usr/bin/env python
"""
Project verification script.
Checks if all required directories and files exist, and validates imports.
"""

import sys
import os
from pathlib import Path

def check_structure():
    """Verify project structure is correct."""
    
    required_dirs = [
        "llm",
        "agents",
        "database",
        "storage",
        "api",
        "ui"
    ]
    
    required_files = {
        "llm": ["__init__.py", "llm.py"],
        "agents": ["__init__.py", "agent.py", "sql_agent.py", "tools.py"],
        "database": ["__init__.py", "sql_db.py"],
        "storage": ["__init__.py", "memory.py"],
        "api": ["__init__.py", "main.py"],
        "ui": ["__init__.py", "streamlit_app.py"],
    }
    
    print("📁 Checking project structure...")
    print("=" * 50)
    
    all_ok = True
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ exists")
        else:
            print(f"✗ {dir_name}/ MISSING")
            all_ok = False
            continue
        
        # Check files in this directory
        for file_name in required_files.get(dir_name, []):
            file_path = dir_path / file_name
            if file_path.exists():
                print(f"  ✓ {file_name}")
            else:
                print(f"  ✗ {file_name} MISSING")
                all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("✅ Project structure is valid!\n")
        return True
    else:
        print("❌ Project structure has issues!\n")
        return False

def check_imports():
    """Verify all modules can be imported."""
    
    print("📦 Checking module imports...")
    print("=" * 50)
    
    sys.path.insert(0, '.')
    
    modules_to_check = [
        ("llm.llm", "ask_llm"),
        ("database.sql_db", "get_connection"),
        ("storage.memory", "get_history"),
        ("agents.agent", "run_agent"),
        ("agents.sql_agent", "ask_database"),
        ("agents.tools", "run_tool"),
        ("api.main", "app"),
        ("ui.streamlit_app", None),
    ]
    
    all_ok = True
    
    for module_name, func_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[func_name] if func_name else [])
            if func_name and not hasattr(module, func_name):
                print(f"✗ {module_name}.{func_name} NOT FOUND")
                all_ok = False
            else:
                print(f"✓ {module_name} imports OK")
        except Exception as e:
            print(f"✗ {module_name} - {str(e)[:50]}")
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("✅ All imports are valid!\n")
        return True
    else:
        print("⚠️  Some imports failed\n")
        return False

def check_files():
    """Check if required files exist."""
    
    print("📄 Checking required files...")
    print("=" * 50)
    
    required_files = [
        "requirements.txt",
        "README.md",
        "run_backend.py",
        "run_frontend.py",
    ]
    
    all_ok = True
    
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✓ {file_name}")
        else:
            print(f"✗ {file_name} MISSING")
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("✅ All required files exist!\n")
        return True
    else:
        print("❌ Some files are missing!\n")
        return False

def main():
    """Run all checks."""
    
    print("\n" + "=" * 50)
    print("🚀 Mini Devin Project Verification")
    print("=" * 50 + "\n")
    
    structure_ok = check_structure()
    files_ok = check_files()
    imports_ok = check_imports()
    
    print("=" * 50)
    if structure_ok and files_ok and imports_ok:
        print("✅ Project is ready to run!")
        print("\nNext steps:")
        print("1. Ensure MongoDB is running: mongod --dbpath C:\\data\\db")
        print("2. Ensure MySQL is running with mini_devin database")
        print("3. Start backend: python run_backend.py")
        print("4. In another terminal, start frontend: python run_frontend.py")
        print("=" * 50)
        return 0
    else:
        print("❌ Project needs fixes before running")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
