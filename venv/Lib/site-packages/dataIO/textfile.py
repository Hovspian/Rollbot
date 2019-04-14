#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
text file IO utility module.

By default, it use "utf-8" encoding.
"""

from __future__ import print_function

import os
import zlib

try:
    import chardet
except ImportError as e:
    import sys    
    err_msg = ("Warning: '%s', ``smartread`` method is not available. " 
               "install 'chardet' to activate this feature.") % e
    sys.stderr.write(err_msg)

try:
    from .py23 import int_type
except:
    from dataIO.py23 import int_type


def is_gzip_file(abspath):
    """Parse file extension.

    - *.json: uncompressed, utf-8 encode json file
    - *.gz: compressed, utf-8 encode json file
    """
    abspath = abspath.lower()
    _, ext = os.path.splitext(abspath)
    if ext in [".gz", ".zip"]:
        is_gzip = True
    else:
        is_gzip = False
    return is_gzip


def write(s, path, encoding="utf-8"):
    """Write string to text file.
    """
    is_gzip = is_gzip_file(path)

    with open(path, "wb") as f:
        if is_gzip:
            f.write(zlib.compress(s.encode(encoding)))
        else:
            f.write(s.encode(encoding))


def writebytes(b, path):
    """Write binary to file.
    """
    with open(path, "wb") as f:
        f.write(b)

    
def read(path, encoding="utf-8"):
    """Read string from text file.
    """
    is_gzip = is_gzip_file(path)

    with open(path, "rb") as f:
        if is_gzip:
            return zlib.decompress(f.read()).decode(encoding)
        else:
            return f.read().decode(encoding)


def readbytes(path):
    """Read binary from file.
    """
    with open(path, "rb") as f:
        return f.read()


def smartread(path):
    """Read text from file, automatically detect encoding. ``chardet`` required.
    """
    with open(path, "rb") as f:
        content = f.read()
        result = chardet.detect(content)
        return content.decode(result["encoding"])
    

def to_utf8(path, output_path=None):
    """Convert any text file to utf8 encoding.
    """
    if output_path is None:
        basename, ext = os.path.splitext(path)
        output_path = basename + "-UTF8Encode" + ext
    
    text = smartread(path)
    write(text, output_path)
    

#--- Text file line reader ---
def no_strip(s):
    return s


def left_strip(s):
    return s.lstrip()


def right_strip(s):
    return s.rstrip()


def both_strip(s):
    return s.strip()


_strip_method_mapping = {
    "none": no_strip,
    "left": left_strip,
    "right": right_strip,
    "both": both_strip,
}


def readlines(path, encoding="utf-8", skiplines=None, nlines=None, strip='right'):
    """skip n lines and fetch the next n lines.
    
    :param skiplines: default None, skip first n lines
    :param nlines: default None, yield next n lines
    :param strip: default None, available option 'left', 'right', 'both'
    
    **中文文档**
    
    跳过前#skiplines行, 然后读取#nlines行。可对字符串进行strip预处理。
    """
    strip_method = str(strip).lower()
    if strip_method in _strip_method_mapping:
        strip_func = _strip_method_mapping[strip_method]
    else:
        raise ValueError("'strip' keyword has to be one of "
                         "None, 'left', 'right', 'both'.")
    
    with open(path, "rb") as file:        
        if skiplines:
            for _ in range(skiplines):
                next(file)
        
        if nlines:
            for _ in range(nlines):
                yield strip_func(next(file).decode(encoding))
        else:
            for line in file:
                yield strip_func(line.decode(encoding))


def readchunks(path, encoding="utf-8", skiplines=None, chunksize=None, strip='right'):
    """skip n lines and fetch the next n lines as a chunk, and repeat fetching.
    
    :param skiplines: default None, skip first n lines
    :param chunksize: default None (size-1 chunk), lines chunk size
    :param strip: default None, avaliable option 'left', 'right', 'both'
    
    **中文文档**
    
    跳过前#skiplines行, 每次读取#chunksize行yield。可对字符串进行strip预处理。
    """
    strip_method = str(strip).lower()
    if strip_method in _strip_method_mapping:
        strip_func = _strip_method_mapping[strip_method]
    else:
        raise ValueError("'strip' keyword has to be one of "
                         "None, 'left', 'right', 'both'.")
        
    with open(path, "rb") as file:
        if skiplines:
            for _ in range(skiplines):
                next(file)
            
        if chunksize is None:
            chunksize = 1
        elif not isinstance(chunksize, int_type): 
            raise ValueError("'chunksize' has to be None or an integer.")
        
        chunk = list()
        while 1:
            for _ in range(chunksize):
                chunk.append(strip_func(next(file).decode(encoding)))
            if len(chunk) < chunksize:
                break
            yield chunk
            chunk = list()
        yield chunk