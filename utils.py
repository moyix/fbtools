from construct import Container

def construct_str(c):
    str = 'Container('
    str += ', '.join("%s = %s" % (field, construct_str(data) if isinstance(data, Container) else repr(data)) for field, data in c.items())
    str += ')'
    return str
