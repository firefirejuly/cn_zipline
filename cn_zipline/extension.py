from zipline.data.bundles import register

from cn_zipline.bundles.tdx_bundle import tdx_bundle

register('tdx',
         tdx_bundle,
         )