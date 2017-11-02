from tdx.engine import Engine
import pandas as pd
from collections import OrderedDict
import numpy as np
import click

OHLC_RATIO = 1000
DAY_BARS_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "day",
    "id"
]

SCALED_COLUMNS = [
    "open",
    "high",
    "low",
    "close"
]


def fetch_symbols(engine):
    stock_list = engine.stock_list
    symbols = pd.DataFrame()
    symbols['symbol'] = stock_list.code
    symbols['asset_name'] = stock_list.name
    symbols['exchange'] = ['sz' if i == 0 else 'sh' for i in stock_list.sse]
    return symbols.reset_index()


def fetch_single_equity(engine, symbol, freq='1d'):
    df = engine.get_security_bars(symbol, freq)
    df['volume'] = df['vol'].astype(np.int32)
    for col in SCALED_COLUMNS:
        df[col] = (df[col] * 1000).astype(np.int32)

    if freq == '1d':
        df.index = df['day'] = df.index.shift(-15, '1H')  # change datetime at 15:00 to midnight
        df['id'] = int(symbol)
        df.day = df.day.values.astype('datetime64[m]').astype(np.int64)
    else:
        df.index = df.index.values.astype('datetime64[m]').astype(np.int64)
    return df.drop(['vol', 'amount', 'code'], axis=1)


def fetch_splits_and_dividends(engine, symbols):
    mask = engine.gbbq.code.isin(symbols['symbol']) & (engine.gbbq.peigu_houzongguben == 0)
    gbbq = engine.gbbq[mask]
    sid = gbbq.code.values.astype('int64')
    splits = pd.DataFrame({
        'sid': sid,
        'effective_date': gbbq.datetime,
        'ratio': 10 / (10 + gbbq.songgu_qianzongguben)
    })

    dividends = pd.DataFrame({
        'sid': sid,
        'ex_date': gbbq.datetime,
        'amount': gbbq.hongli_panqianliutong / 10,
        'record_date': pd.NaT,
        'declared_date': pd.NaT,
        'pay_date': pd.NaT
    })
    return splits[splits.ratio != 1], dividends[dividends.amount != 0]


def get_meta_from_bars(df):
    index = df.index
    return OrderedDict([
        ("start_date", index[0]),
        ("end_date", index[-1]),
        ("first_traded", index[0]),
        ("auto_close_date", index[-1])
    ])


def reindex_to_calendar(calendar, data, freq='1d'):
    start_session, end_session = data.index[[0, -1]]
    if not isinstance(start_session, pd.Timestamp):
        start_session = pd.Timestamp(start_session, unit='m').round('D')
        end_session = pd.Timestamp(end_session, unit='m').round('D')

    if freq == '1d':
        all_sessions = calendar.sessions_in_range(start_session, end_session)
    else:
        all_sessions = calendar.minutes_for_sessions_in_range(start_session, end_session)
    return data.reindex(all_sessions.tz_localize(None), copy=False).fillna(0.0)


def tdx_bundle(environ,
               asset_db_writer,
               minute_bar_writer,
               daily_bar_writer,
               adjustment_writer,
               calendar,
               start_session,
               end_session,
               cache,
               show_progress,
               output_dir):
    eg = Engine(auto_retry=True, multithread=True, best_ip=True, thread_num=8)
    eg.connect()

    symbols = fetch_symbols(eg)
    metas = []

    def gen_symbols_data(symbol_map, freq='1d'):
        for index, symbol in symbol_map.iteritems():
            data = reindex_to_calendar(
                calendar,
                fetch_single_equity(eg, symbol, freq),
                freq=freq,
            )
            if freq == '1d':
                metas.append(get_meta_from_bars(data))
            yield int(symbol), data

    symbol_map = symbols.symbol

    assets = set([int(s) for s in symbol_map])
    daily_bar_writer.write(gen_symbols_data(symbol_map, freq="1d"), assets=assets, show_progress=show_progress)
    with click.progressbar(gen_symbols_data(symbol_map, freq="1m"),
                           label="Merging minute equity files:",
                           length=len(assets),
                           item_show_func=lambda e: e if e is None else str(e[0]),
                           ) as bar:
        minute_bar_writer.write(bar, show_progress=False)

    symbols = pd.concat([symbols, pd.DataFrame(data=metas)], axis=1)
    splits, dividends = fetch_splits_and_dividends(eg, symbols)
    symbols.set_index('symbol', drop=False, inplace=True)
    asset_db_writer.write(symbols)
    adjustment_writer.write(
        splits=splits,
        dividends=dividends
    )

    eg.exit()


if __name__ == '__main__':
    eg = Engine(auto_retry=True, multithread=True, thread_num=8)
    with eg.connect():
        symbols = fetch_symbols(eg)
        symbols = symbols[:3]
        data = []
        metas = []
        for symbol in symbols.symbol:
            data.append((int(symbol), fetch_single_equity(eg, symbol)))
            metas.append(get_meta_from_bars(data[-1][1]))
        symbols = pd.concat([symbols, pd.DataFrame(data=metas)], axis=1)
        splits, dividends = fetch_splits_and_dividends(eg, symbols)
