import os
import os.path

import g

import listops

def openreadclose(path):
    tmp = file(path)
    try:
        result = tmp.read()
    finally:
        tmp.close()
    return result
        
@g.debug.debug_func
def get_templates(pathname):
    for pwd in os.walk(pathname):
        for fil in pwd[2]:
            name,ext=os.path.splitext(os.path.basename(fil))
            if ext == ".mako":
                filpath = os.path.join(pwd[0], name)
                data = openreadclose(filpath+ext)
                templatename = os.path.join(pwd[0], name)
                templatename = templatename.replace(pathname,'')
                g.debug(templatename)
                g.templates.add_template(templatename,data)