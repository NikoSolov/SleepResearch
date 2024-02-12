# test.py
import sys, os

print('List of parameters')
print(sys.argv)
print('Source bytes')
print([os.fsencode(arg) for arg in sys.argv])
