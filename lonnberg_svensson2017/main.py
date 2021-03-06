import pandas as pd
import xarray as xr

try:
    # Python 2
    from urlparse import urljoin
except ImportError:
    # Python 3
    from urllib.parse import urljoin

BASE_URL = 'https://raw.githubusercontent.com/olgabot/lonnberg_svensson2017/' \
           'master/lonnberg_svensson2017'


def read_csv(folder, filename):
    """Wrapper for pandas read_csv that uses the first column for the index"""
    csv = urljoin(folder, filename)
    return pd.read_csv(csv, index_col=0)


def _load(prefix, package):
    """Internal method for loading """

    # TODO make this files and serve them from github repo
    expression    = read_csv(BASE_URL, '{}_expression.csv'.format(prefix))
    cell_metadata = read_csv(BASE_URL, '{}_cell_metadata.csv'.format(prefix))
    gene_metadata = read_csv(BASE_URL, '{}_gene_metadata.csv'.format(prefix))

    if package == 'xarray':
        ds = xr.Dataset({'expression': (['cell', 'gene'], expression),
                         'gene_metadata':
                             (['gene', 'gene_feature', ], gene_metadata),
                         'cell_metadata':
                             (['cell', 'cell_feature'], cell_metadata)},
                        coords={'gene': expression.columns,
                                'cell': expression.index,
                                'cell_feature': cell_metadata.columns,
                                'gene_feature': gene_metadata.columns})
        return ds
    if package == 'pandas':
        return expression, cell_metadata, gene_metadata
    else:
        raise ValueError('"{}" is not a valid format. Only "pandas" and '
                         '"xarray" are accepted'.format(package))


def load_clusters(package='pandas'):
    """Read expression and metadata for 50 random cells from 6 biggest clusters

    300 cells, 259 genes

    Parameters
    ----------
    package : 'pandas' | 'xarray'

    Returns
    -------
    if format == "pandas":
        expression, cell_metadata, gene_metadata
    if format == "xarray"
        xarray.Dataset
    """
    return _load('clusters', package)

