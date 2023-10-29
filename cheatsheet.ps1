# To rebuild report template list on windows only. 
# Using VSCode select the line(s) you wish to execute and use "Run Selection (F8)"

# Activate python
python -m venv env

# Rebuild index

python build_index.py
