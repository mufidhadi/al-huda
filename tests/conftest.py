import sys
import os

# Menambahkan root directory ke sys.path agar module search_engine bisa ditemukan oleh pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
