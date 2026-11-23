"""
app.py - entry point for Streamlit / Render.

The UI itself lives in PART4_Simple_App_Interface/task6_streamlit_ui.py.
Run locally:  streamlit run app.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from task6_streamlit_ui import main

main()
