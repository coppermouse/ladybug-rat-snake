# ----------------------------------------
# file: file_to_class.py
# methods: file_to_class, class_to_file
# ----------------------------------------

def file_to_class( file ):
    r = ""
    upper = True
    for c in file:
        if c == '_':
            upper = True
            continue
        r += c.upper() if upper else c
        upper = False
    return r


def class_to_file( _class ):
    r = ""
    for e, c in enumerate( _class ):
        if e != 0 and c.isupper():
            r += "_"
        r += c.lower()
    return r


