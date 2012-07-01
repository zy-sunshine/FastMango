import json
g_vars = {}
l_vars = {}
execfile('pkgarr.py', g_vars, l_vars)
pyconf = l_vars
with open('pkgarr.json', 'w') as f:
    json.dump(pyconf, f, indent=4)