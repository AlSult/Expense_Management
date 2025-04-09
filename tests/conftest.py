import os
import sys

project_root = os.path.join(os.path.dirname(__file__), '..')
print("**Project Root:", project_root)

# Inserting the projct root to the system path
sys.path.insert(0, project_root)
print(sys.path)
