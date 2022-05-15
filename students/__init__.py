import importlib as __importlib
import os as __os
import os.path as __path
import re as __re


_IMPORT_ERRORS = []

__module_path = __path.dirname(__file__)
_pyfiles = []

for _filename in __os.listdir(__module_path):
    if _filename.startswith("."):
        continue
    if _filename.startswith("__"):
        continue
    if _filename.endswith(".py"):
        _pyfiles.append(_filename)

_pyfiles.sort()

# Students may upload the same file multiple times.  This will result in files
# such as "AwesomeBot.py" and "AwesomeBot (1).py". We will overwrite
# "AwesomeBot.py" with its highest numbered version.
_agent_files = set()
_duplicate_id = {}
_ORIGINAL_ID = -1

for _filename in _pyfiles:
    _canonical_name = __re.sub(" \(\d+\).py$", ".py", _filename)
    _dup_id = _ORIGINAL_ID
    if _filename != _canonical_name:
        _dup_id = int(__re.search("(?<= \()\d+(?=\).py)", _filename).group())
    if _dup_id >= _duplicate_id.get(_canonical_name, _ORIGINAL_ID):
        if _dup_id != _ORIGINAL_ID:
            try:
                __os.remove(__path.join(__module_path, _canonical_name))
            except OSError:
                pass
            __os.rename(__path.join(__module_path, _filename),
                    __path.join(__module_path, _canonical_name))
        _duplicate_id[_canonical_name] = _dup_id
        _agent_files.add(_canonical_name)

for _filename in _agent_files:
    _modname = _filename[:-len('.py')]
    try:
        __importlib.import_module(__name__ + "." + _modname)
    except:
        _IMPORT_ERRORS.append(_modname)

try:
    del _ORIGINAL_ID, _agent_files, _canonical_name, _dup_id, _duplicate_id, \
            _filename, _modname, _pyfiles
except NameError:
    pass
