# coding=utf-8

from zipline.api import order, record, symbol


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol('000001'), 10)
    current_dt = data.current_dt
    record(AAPL=data.current(symbol('000001'), 'price'))


if __name__ == '__main__':
    from cn_zipline.utils.run_algo import run_algorithm
    from zipline.utils.cli import Date
    from cn_stock_holidays.zipline.default_calendar import shsz_calendar

    start = Date(tz='utc', as_timestamp=True).parser('2017-01-01')

    end = Date(tz='utc', as_timestamp=True).parser('2017-10-20')
    run_algorithm(start, end, initialize, 10e6, handle_data=handle_data, bundle='tdx',trading_calendar=shsz_calendar,data_frequency="minute", output='out.pickle')
