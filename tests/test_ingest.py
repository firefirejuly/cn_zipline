import pytest
from tdx.engine import Engine
from cn_zipline.bundles.tdx_bundle import *


def test_data():
    eg = Engine(auto_retry=True, multithread=True, thread_num=8)
    with eg.connect():

        symbols = fetch_symbols(eg)
        symbols = symbols[:5]
        metas = []

        def gen_symbols_data(symbol_map, freq='1d'):
            for index, symbol in symbol_map.iteritems():
                data = fetch_single_equity(eg, symbol, freq)

                if freq == '1d':
                    metas.append(get_meta_from_bars(data))

                assert data is not None
                yield int(symbol), data

        symbol_map = symbols.symbol

        assets = set([int(s) for s in symbol_map])
        gen_symbols_data(symbol_map, freq="1d")
        gen_symbols_data(symbol_map, freq="1m")

        symbols = pd.concat([symbols, pd.DataFrame(data=metas)], axis=1)
        splits, dividends = fetch_splits_and_dividends(eg, symbols)
        symbols.set_index('symbol', drop=False, inplace=True)

        assert symbols is not None
        assert splits is not None
        assert dividends is not None
