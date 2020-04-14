from printy import printy

# This uses the Escape Sequences, it won't work w/o importing printy. 
# The part which enables the terminal variable is in core.py:line35.
print("\033[1;31m" + 'This is should be red' + "\033[0;0m")

# Even though escape sequences now work the printy class itself still doesn't.
# I can't understand the problem though I'll keep looking.
printy('This should be red too', 'r')

