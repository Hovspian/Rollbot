#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pickle IO utility module.

useful method:

- :func:`load`
- :func:`dump`
- :func:`safe_dump`
- :func:`obj2bytes`
- :func:`bytes2obj`
- :func:`obj2str`
- :func:`str2obj`
"""

from __future__ import print_function, unicode_literals

import time
import os, shutil
import sys
import gzip
import base64
import pickle

try:
    from . import compress
    from . import textfile
    from . import py23
    from .printer import prt
except:
    from dataIO import compress
    from dataIO import textfile
    from dataIO import py23
    from dataIO.printer import prt


class PickleExtError(Exception):
    pass


def is_pickle_file(abspath):
    """Parse file extension.
    
    - *.pickle: uncompressed, utf-8 encode pickle file
    - *.gz: compressed, utf-8 encode pickle file
    """
    abspath = abspath.lower()
    fname, ext = os.path.splitext(abspath)
    if ext in [".pickle", ".pk", ".p"]:
        is_pickle = True
    elif ext == ".gz":
        is_pickle = False
    elif ext == ".tmp":
        return is_pickle_file(fname)
    else:
        raise PickleExtError(
            "'%s' is not a valid pickle file. "
            "extension has to be '.pickle' for uncompressed, '.gz' "
            "for compressed." % abspath)
    return is_pickle


def lower_ext(abspath):
    """Convert file extension to lowercase.
    """
    fname, ext = os.path.splitext(abspath)
    return fname + ext.lower()


def load(abspath, default=None, enable_verbose=True):
    """Load Pickle from file. If file are not exists, returns ``default``.

    :param abspath: file path. use absolute path as much as you can. 
      extension has to be ``.pickle`` or ``.gz`` (for compressed Pickle). 
    :type abspath: string

    :param default: default ``dict()``, if ``abspath`` not exists, return the
        default Python object instead.

    :param enable_verbose: default ``True``, help-message-display trigger.
    :type enable_verbose: boolean

    Usage::

        >>> from dataIO import pk
        >>> pk.load("test.pickle") # if you have a pickle file
        Load from `test.pickle` ...
            Complete! Elapse 0.000432 sec.
        {'a': 1, 'b': 2}

    **中文文档**

    从Pickle文件中读取数据

    :param abspath: Pickle文件绝对路径, 扩展名需为 ``.pickle`` 或 ``.gz``, 其中 ``.gz``
      是被压缩后的Pickle文件
    :type abspath: ``字符串``

    :param default: 默认 ``dict()``, 如果文件路径不存在, 则会返回指定的默认值

    :param enable_verbose: 默认 ``True``, 信息提示的开关, 批处理时建议关闭
    :type enable_verbose: ``布尔值``
    """
    if default is None:
        default = dict()

    prt("\nLoad from '%s' ..." % abspath, enable_verbose)

    abspath = lower_ext(str(abspath))
    is_pickle = is_pickle_file(abspath)

    if not os.path.exists(abspath):
        prt("    File not found, use default value: %r" % default,
            enable_verbose)
        return default

    st = time.clock()
    if is_pickle:
        data = pickle.loads(textfile.readbytes(abspath))
    else:
        data = pickle.loads(compress.read_gzip(abspath))

    prt("    Complete! Elapse %.6f sec." % (time.clock() - st), enable_verbose)
    return data


def dump(data, abspath, pk_protocol=py23.pk_protocol,
         overwrite=False, enable_verbose=True):
    """Dump picklable object to file.
    Provides multiple choice to customize the behavior.

    :param data: picklable python object.
    :type data: dict or list

    :param abspath: ``save as`` path, file extension has to be ``.pickle`` or ``.gz``
        (for compressed Pickle)
    :type abspath: string

    :param pk_protocol: default = your python version, use 2, to make a
        py2.x/3.x compatible pickle file. But 3 is faster.
    :type pk_protocol: int

    :param overwrite: default ``False``, If ``True``, when you dump to existing
        file, it silently overwrite it. If ``False``, an alert message is shown.
        Default setting ``False`` is to prevent overwrite file by mistake.
    :type overwrite: boolean

    :param enable_verbose: default True, help-message-display trigger.
    :type enable_verbose: boolean

    Usage::

        >>> from dataIO import pk
        >>> data = {"a": 1, "b": 2}
        >>> dump(data, "test.pickle", overwrite=True)
        Dump to `test.pickle` ...
            Complete! Elapse 0.002432 sec

    **中文文档**

    将Python中可被序列化的"字典", "列表"以及他们的组合, 按照Json的编码方式写入文件
    文件

    参数列表

    :param data: 可Pickle化的Python对象
    :type data: ``字典`` 或 ``列表``

    :param abspath: Pickle文件绝对路径, 扩展名需为 ``.pickle`` 或 ``.gz``, 其中 ``.gz``
      是被压缩后的Pickle文件
    :type abspath: ``字符串``

    :param pk_protocol: 默认值为你的Python大版本号, 使用2可以使得Python2/3都能
      兼容你的Pickle文件。不过Python3的速度更快。
    :type pk_protocol: int

    :param overwrite: 默认 ``False``, 当为``True``时, 如果写入路径已经存在, 则会
      自动覆盖原文件。而为``False``时, 则会打印警告文件, 防止误操作覆盖源文件。
    :type overwrite: "布尔值"

    :param enable_verbose: 默认 ``True``, 信息提示的开关, 批处理时建议关闭
    :type enable_verbose: ``布尔值``
    """
    prt("\nDump to '%s' ..." % abspath, enable_verbose)

    abspath = lower_ext(str(abspath))
    is_pickle = is_pickle_file(abspath)

    if os.path.exists(abspath):
        if not overwrite:  # 存在, 并且overwrite=False
            prt("    Stop! File exists and overwrite is not allowed",
                enable_verbose)
            return

    st = time.clock()
    content = pickle.dumps(data, pk_protocol)
    if is_pickle:
        textfile.writebytes(content, abspath)
    else:
        compress.write_gzip(content, abspath)

    prt("    Complete! Elapse %.6f sec." % (time.clock() - st), enable_verbose)


def safe_dump(data, abspath, pk_protocol=py23.pk_protocol, enable_verbose=True):
    """A stable version of :func:`dump`, this method will silently overwrite 
    existing file.
    
    There's a issue with :func:`dump`: If your program is interrupted while 
    writing, you got an incomplete file, and you also lose the original file.
    So this method write pickle to a temporary file first, then rename to what
    you expect, and silently overwrite old one. This way can guarantee atomic 
    write.
    
    **中文文档**

    在对文件进行写入时, 如果程序中断, 则会留下一个不完整的文件。如果使用了覆盖式
    写入, 则我们即没有得到新文件, 同时也丢失了原文件。所以为了保证写操作的原子性
    (要么全部完成, 要么全部都不完成), 更好的方法是: 首先将文件写入一个临时文件中, 
    完成后再讲文件重命名, 覆盖旧文件。这样即使中途程序被中断, 也仅仅是留下了一个
    未完成的临时文件而已, 不会影响原文件。
    """
    abspath = lower_ext(str(abspath))
    abspath_temp = "%s.tmp" % abspath
    dump(data, abspath_temp,
         pk_protocol=pk_protocol, enable_verbose=enable_verbose)
    shutil.move(abspath_temp, abspath)


def obj2bytes(obj, pk_protocol=py23.pk_protocol):
    """Convert arbitrary pickable Python Object to bytes.

    **中文文档**

    将可Pickle化的Python对象转化为bytestr
    """
    return pickle.dumps(obj, protocol=pk_protocol)


def bytes2obj(b):
    """Load Python object from bytes.

    **中文文档**

    从bytestr中恢复Python对象
    """
    return pickle.loads(b)


def obj2str(obj, pk_protocol=py23.pk_protocol):
    """Convert arbitrary object to base64 encoded string.

    **中文文档**

    将可Pickle化的Python对象转化为utf-8编码的 ``纯ASCII字符串``
    """
    return base64.urlsafe_b64encode(pickle.dumps(
        obj, protocol=pk_protocol)).decode("utf-8")


def str2obj(s):
    """Load object from base64 encoded string.

    **中文文档**

    从base64编码的 ``纯ASCII字符串`` 中恢复Python对象
    """
    return pickle.loads(base64.urlsafe_b64decode(s.encode("utf-8")))
