# cn_zipline
基于tdx的zipline bundle.

## 安装依赖
git: 下载地址 https://git-scm.com/download/win

\
pytdx: tdx数据源 https://rainx.gitbooks.io/pytdx/content

    pip install pytdx

pdx: 获取历史k线数据 https://github.com/JaysonAlbert/tdx.git

    pip install git+https://github.com/JaysonAlbert/tdx.git
      
cn_stock_holidays: 沪深300日历 https://github.com/rainx/cn_stock_holidays
      
    pip install git+https://github.com/rainx/cn_stock_holidays.git
    
cn-treasury_curve: 国债收益率曲线 https://github.com/rainx/cn_treasury_curve

    pip install cn-treasury_curve
`
## 安装：

    pip install git+https://github.com/JaysonAlbert/tdx.git
    
将`cn_zipline/extension.py`拷贝至zipline的数据目录,默认为`~/.zipline`
    
    
## 使用：

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