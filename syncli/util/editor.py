"""
Recipe from OReilly Python Cookbook
Credit to Larry Price, Peter Cogolo

http://books.google.com/books?id=Q0s6Vgb98CQC&lpg=PT436&ots=hc6X43QfoD&dq=python%20invoke%20system%20editor%20on%20temp%20file&pg=PT436#v=onepage&q&f=false
"""

import sys, os, tempfile

def edit_text(starting_text=''):
    temp_fd, temp_filename = tempfile.mkstemp(text=True)
    os.write(temp_fd, starting_text)
    os.close(temp_fd)
    time = os.path.getmtime(temp_filename)
    editor = _what_editor()
    x = os.spawnlp(os.P_WAIT, editor, editor, temp_filename)
    if x:
        raise RuntimeError, "Can't run %s %s (%s)" % (editor, temp_filename, x)
    result = open(temp_filename).read()
    updated = os.path.getmtime(temp_filename)
    os.unlink(temp_filename)
    if time == updated:
        raise NotModifiedException()
    return result

def _what_editor():
    editor = os.getenv('VISUAL') or os.getenv('EDITOR')
    if not editor:
        if sys.platform == 'windows':
            editor = 'Notepad.Exe'
        else:
            editor = 'vi'
    return editor

class NotModifiedException(Exception):
    pass
