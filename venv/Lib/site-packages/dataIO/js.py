#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
json IO utility module.

useful method:

- :func:`load`
- :func:`dump`
- :func:`safe_dump`
- :func:`pprint`
"""

from __future__ import print_function, unicode_literals

import time
import os
import shutil
from json import encoder

try:
    from bson import json_util as json
except ImportError as e:
    import sys

    err_msg = ("Notice: '%s', using standard lib 'json'. "
               "install 'pymongo' to support datetime type. "
               "You can ignore this message if you want.")
    sys.stderr.write(err_msg)
    import json

try:
    from . import compress
    from . import textfile
    from .printer import prt
except:
    from dataIO import compress
    from dataIO import textfile
    from dataIO.printer import prt


class JsonExtError(Exception):
    """Raises when it is not a json file.
    """
    pass


def is_json_file(abspath):
    """Parse file extension.

    - *.json: uncompressed, utf-8 encode json file
    - *.gz: compressed, utf-8 encode json file
    """
    abspath = abspath.lower()
    fname, ext = os.path.splitext(abspath)
    if ext in [".json", ".js"]:
        is_json = True
    elif ext == ".gz":
        is_json = False
    elif ext == ".tmp":
        return is_json_file(fname)
    else:
        raise JsonExtError(
            "'%s' is not a valid json file. "
            "extension has to be '.json' for uncompressed, '.gz' "
            "for compressed." % abspath)
    return is_json


def lower_ext(abspath):
    """Convert file extension to lowercase.
    """
    fname, ext = os.path.splitext(abspath)
    return fname + ext.lower()


def load(abspath, default=None, enable_verbose=True):
    """Load Json from file. If file are not exists, returns ``default``.

    :param abspath: file path. use absolute path as much as you can. 
      extension has to be ``.json`` or ``.gz`` (for compressed Json). 
    :type abspath: string

    :param default: default ``dict()``, if ``abspath`` not exists, return the
        default Python object instead.

    :param enable_verbose: default ``True``, help-message-display trigger.
    :type enable_verbose: boolean

    Usage::

        >>> from dataIO import js
        >>> js.load("test.json") # if you have a json file
        Load from 'test.json' ...
            Complete! Elapse 0.000432 sec.
        {'a': 1, 'b': 2}

    **中文文档**

    从Json文件中读取数据

    :param abspath: Json文件绝对路径, 扩展名需为 ``.json`` 或 ``.gz``, 其中 ``.gz``
      是被压缩后的Json文件
    :type abspath: ``字符串``

    :param default: 默认 ``dict()``, 如果文件路径不存在, 则会返回指定的默认值

    :param enable_verbose: 默认 ``True``, 信息提示的开关, 批处理时建议关闭
    :type enable_verbose: ``布尔值``
    """
    if default is None:
        default = dict()

    prt("\nLoad from '%s' ..." % abspath, enable_verbose)

    abspath = lower_ext(str(abspath))
    is_json = is_json_file(abspath)

    if not os.path.exists(abspath):
        prt("    File not found, use default value: %r" %
            default, enable_verbose)
        return default

    st = time.clock()
    if is_json:
        data = json.loads(textfile.read(abspath, encoding="utf-8"))
    else:
        data = json.loads(compress.read_gzip(abspath).decode("utf-8"))

    prt("    Complete! Elapse %.6f sec." % (time.clock() - st), enable_verbose)
    return data


def dump(data, abspath,
         indent_format=False,
         float_precision=None,
         ensure_ascii=True,
         overwrite=False,
         enable_verbose=True):
    """Dump Json serializable object to file.
    Provides multiple choice to customize the behavior.

    :param data: Serializable python object.
    :type data: dict or list

    :param abspath: ``save as`` path, file extension has to be ``.json`` or ``.gz``
        (for compressed Json)
    :type abspath: string

    :param indent_format: default ``False``, If ``True``, then dump to human
      readable format, but it's slower, the file is larger
    :type indent_format: boolean

    :param float_precision: default ``None``, limit flotas to N-decimal points. 
    :type float_precision: integer

    :param overwrite: default ``False``, If ``True``, when you dump to existing
        file, it silently overwrite it. If ``False``, an alert message is shown.
        Default setting ``False`` is to prevent overwrite file by mistake.
    :type overwrite: boolean

    :param enable_verbose: default True, help-message-display trigger.
    :type enable_verbose: boolean

    Usage::

        >>> from dataIO import js
        >>> data = {"a": 1, "b": 2}
        >>> dump(data, "test.json", overwrite=True)
        Dumping to 'test.json'...
            Complete! Elapse 0.002432 sec

    **中文文档**

    将Python中可被序列化的"字典", "列表"以及他们的组合, 按照Json的编码方式写入文件
    文件

    参数列表

    :param js: 可Json化的Python对象
    :type js: ``字典`` 或 ``列表``

    :param abspath: Json文件绝对路径, 扩展名需为 ``.json`` 或 ``.gz``, 其中 ``.gz``
      是被压缩后的Json文件
    :type abspath: ``字符串``

    :param indent_format: 默认 ``False``, 当为 ``True`` 时, Json编码时会对Key进行
      排序, 并进行缩进排版。但是这样写入速度较慢, 文件体积也更大。
    :type indent_format: "布尔值"

    :param overwrite: 默认 ``False``, 当为``True``时, 如果写入路径已经存在, 则会
      自动覆盖原文件。而为``False``时, 则会打印警告文件, 防止误操作覆盖源文件。
    :type overwrite: "布尔值"

    :param float_precision: 默认 ``None``, 当为任意整数时, 则会保留小数点后N位
    :type float_precision: "整数"

    :param enable_verbose: 默认 ``True``, 信息提示的开关, 批处理时建议关闭
    :type enable_verbose: ``布尔值``
    """
    prt("\nDump to '%s' ..." % abspath, enable_verbose)

    abspath = lower_ext(str(abspath))
    is_json = is_json_file(abspath)

    if os.path.exists(abspath):
        if not overwrite:  # 存在, 并且overwrite=False
            prt("    Stop! File exists and overwrite is not allowed",
                enable_verbose)
            return

    if float_precision is not None:
        encoder.FLOAT_REPR = lambda x: format(x, ".%sf" % float_precision)
        indent_format = True
    else:
        encoder.FLOAT_REPR = repr

    if indent_format:
        sort_keys = True
        indent = 4
    else:
        sort_keys = False
        indent = None

    st = time.clock()
    js = json.dumps(data, sort_keys=sort_keys, indent=indent,
                    ensure_ascii=ensure_ascii)
    content = js.encode("utf-8")
    if is_json:
        textfile.writebytes(content, abspath)
    else:
        compress.write_gzip(content, abspath)

    prt("    Complete! Elapse %.6f sec." % (time.clock() - st), enable_verbose)


def safe_dump(data, abspath,
              indent_format=False,
              float_precision=None,
              ensure_ascii=True,
              enable_verbose=True):
    """A stable version of :func:`dump`, this method will silently overwrite 
    existing file.

    There's a issue with :func:`dump`: If your program is interrupted while 
    writing, you got an incomplete file, and you also lose the original file.
    So this method write json to a temporary file first, then rename to what
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
         indent_format=indent_format, float_precision=float_precision,
         ensure_ascii=ensure_ascii,
         overwrite=True, enable_verbose=enable_verbose)
    shutil.move(abspath_temp, abspath)


def pretty_dumps(data):
    """Return json string in pretty format.

    **中文文档**

    将字典转化成格式化后的字符串。
    """
    try:
        return json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    except:
        return json.dumps(data, sort_keys=True, indent=4, ensure_ascii=True)


def pprint(data):
    """Print Json in pretty human readable format.

    There's a standard module pprint, can pretty print python dict and list.
    But it doesn't support sorted key, and indent doesn't looks good.

    Usage::

        >>> from dataIO import js
        >>> js.pprint({"a": 1, "b": 2})
        {
            "a": 1,
            "b": 2
        }

    **中文文档**

    以人类可读的方式打印可Json化的Python对象。
    """
    print(pretty_dumps(data))
