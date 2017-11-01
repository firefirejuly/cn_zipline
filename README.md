# cn_zipline

--------------



[![PyPI version](https://badge.fury.io/py/cn-zipline.svg)](https://badge.fury.io/py/cn-zipline)
[![Py version](https://img.shields.io/pypi/pyversions/cn-zipline.svg)](https://pypi.python.org/pypi/cn-zipline)
[![Build Status](https://travis-ci.org/JaysonAlbert/cn_zipline.svg?branch=master)](https://travis-ci.org/JaysonAlbert/cn_zipline)
[![Build status](https://ci.appveyor.com/api/projects/status/b0pf9nndpj65x0nj/branch/master?svg=true)](https://ci.appveyor.com/project/JaysonAlbert/cn-zipline/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/JaysonAlbert/cn_zipline/badge.svg?branch=master)](https://coveralls.io/github/JaysonAlbert/cn_zipline?branch=master)

基于tdx的zipline bundle.

[zipline](http://zipline.io/)是美国[Quantopian](https://quantopian.com/) 公司开源的量化交易回测引擎，它使用`Python`语言开发，
部分代码使用`cython`融合了部分c语言代码。`Quantopian` 在它的网站上的回测系统就是基于`zipline`的，
经过生产环境的长期使用，已经比完善，并且在持续的改进中。

`zipline`的基本使用方法在http://www.zipline.io/beginner-tutorial.html， 对于zipline的深度解析，可以看大神[rainx](https://github.com/rainx)写的[文档](https://www.gitbook.com/book/rainx/-zipline/details)，本项目中的大部分依赖项目也都是rainx开发的项目
`

## 数据源：
`cn_zipline`的历史k线以及除息除权数据来自通达信，数据接口来自项目github 项目tdx https://github.com/JaysonAlbert/tdx 

## 安装：

    pip install cn_zipline
**注意**：在`windows`上，如果`zipline`安装失败，先用`conda install -c Quantopian zipline`安装`zipline`,然后再安装`cn_zipline`
    
将`cn_zipline/extension.py`拷贝至zipline的数据目录,默认为`~/.zipline`
    
## 使用：
cn_zipline与zipline大同小异，具体使用方法请参考zipline[官方文档](http://zipline.io/)。不同之处在于，`ingest`数据时请使用
`cn_zipline`命令，管理以及清理`bundls`数据时使用`zipline`。运行策略的形式也不同，为便于调试代码，采用直接运行策略脚本，
而**不是**通过`zipline run`命令来运行。下面是使用示例：

ingest数据：

    cn_zipline ingest -b tdx
    
编辑策略`cn_zipline/examples/buyapply.py`：

    from zipline.api import order, record, symbol


    def initialize(context):
        pass
    
    
    def handle_data(context, data):
        order(symbol('000001'), 10)
        record(AAPL=data.current(symbol('000001'), 'price'))
    
    
    if __name__ == '__main__':
        from cn_zipline.utils.run_algo import run_algorithm
        from zipline.utils.cli import Date
        from cn_stock_holidays.zipline.default_calendar import shsz_calendar
    
        start = Date(tz='utc', as_timestamp=True).parser('2017-01-01')
    
        end = Date(tz='utc', as_timestamp=True).parser('2017-10-20')
        run_algorithm(start, end, initialize, 10e6, handle_data=handle_data, bundle='tdx',trading_calendar=shsz_calendar,output='out.pickle')
       
运行策略文件 `cn_zipline/examples/buyapply.py`

运行分析脚本`cn_zipline/examples/analyse.py`
