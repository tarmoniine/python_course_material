
# coding: utf-8

# # Python keywords
# 
# There are a limited number of keywords that form the Python language:

# In[1]:

import keyword
print(keyword.kwlist)


# Note that variable names cannot be one of these keywords. 
# 
# In addition, variables cannot be one of the `__builtin__` objects (classes or functions) listed below (although some of these are [IPython] specific and are allowed outside of [IPython]).

# In[2]:

print(dir(__builtin__))


# # Built in Python components
# 
# In addition to both keywords and `__builtin__` objects, the Python standard library has very many built-in features and routines that make it a joy to program in.
# 
# **Warning** It is best if you never assign a new variable to have the same name as that found in the Python standard library
# 
# The following list includes both the hidden and standard library components from your computer. The code to generate this list is found below, however, I do not expect you to understand this code so view at your own risk ;)
# 
# **Python standard library**
# 
# ```
# sndhdr textwrap cmd mimetypes io pyclbr linecache termios sunau site mailcap 
# re pdb sysconfig xmlrpc pstats crypt selectors asynchat fnmatch locale 
# xdrlib importlib plistlib datetime types ftplib imp keyword queue gettext 
# glob enum pty this shlex string os pickle traceback aifc imghdr http timeit 
# resource parser getpass tabnanny codeop copyreg socket token xml cProfile 
# asyncore functools sre_parse pipes fileinput nis threading distutils wsgiref 
# tracemalloc colorsys antigravity ctypes bisect symtable platform struct 
# warnings email gzip formatter readline dummy_threading bz2 uuid imaplib 
# py_compile pkgutil urllib decimal asyncio fractions venv idlelib collections 
# bdb csv sre_compile dis stringprep base64 json rlcompleter configparser 
# codecs smtpd audioop mailbox turtle posixpath poplib sre_constants numbers 
# mmap runpy cgi lib2to3 symbol statistics pprint inspect html macpath 
# unittest operator compileall sitecustomize sqlite3 copy trace uu tempfile 
# heapq quopri hashlib tkinter nntplib logging doctest shelve fpectl sched 
# opcode macurl2path concurrent optparse shutil ntpath argparse lzma pathlib 
# webbrowser contextlib hmac getopt netrc tty pydoc dbm subprocess weakref 
# encodings calendar modulefinder xxlimited test nturl2path socketserver stat 
# pydoc_data telnetlib tarfile cmath smtplib curses chunk pickletools zipfile 
# multiprocessing random wave genericpath code binhex filecmp ast difflib ssl 
# ipaddress tokenize abc reprlib cgitb profile ossaudiodev
# ```
# 
# **Python hidden standard library**
# 
# ```
# _markupbase _testcapi _compat_pickle _json _testimportmultiple _curses 
# _codecs_cn _weakrefset _strptime __phello__ _osx_support _sysconfigdata 
# _ctypes _dbm _bz2 _codecs_tw _collections_abc _multibytecodec 
# _multiprocessing _crypt _testbuffer _hashlib _codecs_jp _threading_local 
# _ssl _pyio _codecs_kr _opcode _codecs_hk _sitebuiltins _decimal _bootlocale 
# _lzma _sqlite3 _dummy_thread _codecs_iso2022 _lsprof __future__ _ctypes_test 
# _curses_panel _csv _gdbm
# ```

# In[ ]:

import os
import imp
import sys
import pprint
import distutils.sysconfig

std_lib = distutils.sysconfig.get_python_lib(standard_lib=True)

std_set = set()
hidden_set = set()
for top, dirs, files in os.walk(std_lib):
    for fn in files:
        
        # Remove the std_lib path from the path
        prefix = top.replace(std_lib, '').replace(os.path.sep, '')
        
        if prefix.count('site-packages') > 0:
            continue
        if fn == '__init__.py':
            item = top[len(std_lib) + 1:]
        elif fn[-3:] == '.py':
            item = os.path.join(prefix, fn)[:-3]
        elif fn[-3:] == '.so' and top[-11:] == 'lib-dynload':
            item = fn[0:-3]
            
        # Only consider top level imports
        item = item.split(os.path.sep)[0]
        if item.count('.') > 0:
            item = item.split('.')[0]
        
        # Only add items that you can actually import
        try:
            imp.find_module(item)
        except ImportError as e:
            continue
        
        if item.startswith('_'):
            hidden_set.add(item)
        else:
            std_set.add(item)
          
def format_set(raw_set):
    return pprint.pformat(' '.join(list(raw_set))).replace("'", '')
            
print('**Python standard library**\n\n```\n{}\n```'.format(format_set(std_set)))
print('\n**Python hidden standard library**\n\n```\n{}\n```'.format(format_set(hidden_set)))

