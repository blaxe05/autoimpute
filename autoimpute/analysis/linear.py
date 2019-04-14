"""Module containing linear regression for multiply imputed datasets."""

import pandas as pd
# from sklearn.linear_model import LinearRegression
# from statsmodels.api import OLS
from autoimpute.utils import check_nan_columns
from .base_regressor import BaseRegressor
# pylint:disable=attribute-defined-outside-init

class MiLinearRegression(BaseRegressor):
    """Linear Regression wrapper for multiply imputed datasets.

    The LinearRegression class wraps the sklearn and statsmodels libraries
    to extend linear regression to multiply imputed datasets. The class wraps
    statsmodels as well as sklearn because sklearn alone does not provide
    sufficient functionality to pool estimates under Rubin's rules. sklearn is
    for machine learning; therefore, important inference capabilities are
    lacking, such as easily calculating std. error estimates for parameters.
    If users want inference from regression analysis of multiply imputed
    data, utilze the statsmodels implementation in this class instead.
    """

    def __init__(self, model_lib="statsmodels", mi_kwgs=None,
                 model_kwgs=None):
        """Create an instance of the AutoImpute LinearRegression class.

        Args:
            model_lib (str, Optional): library the regressor will use to
                implement regression. Options are sklearn and statsmodels.
                Default is statsmodels.
            mi_kwgs (dict, Optional): keyword args to instantiate
                MultipleImputer. Default is None.
            model_kwgs (dict, Optional): keyword args to instantiate
                regressor. Default is None.

        Returns:
            self. Instance of the class.
        """
        BaseRegressor.__init__(
            self,
            model_lib=model_lib,
            mi_kwgs=mi_kwgs,
            model_kwgs=model_kwgs
        )

    def _fit_strategy_validator(self, X, y):
        """Private method to validate data before fitting model."""
        # y must be a series or dataframe
        if not isinstance(y, (pd.Series, pd.DataFrame)):
            err = "y must be a Series or DataFrame"
            raise ValueError(err)

        # y and X must have the same number of rows
        if X.shape[0] != y.shape[0]:
            err = "y and X must have the same number of records"
            raise ValueError(err)

        # y must have a name if series.
        if isinstance(y, pd.Series):
            self._yn = y.name
            if self._yn is None:
                err = "series y must have a name"
                raise ValueError(err)

        # y must have one column if dataframe.
        if isinstance(y, pd.DataFrame):
            yc = y.shape[1]
            if yc != 1:
                err = "y should only have one column"
                raise ValueError(err)
            self._yn = y.columns.tolist()[0]

        # if no errors thus far, add y to X for imputation
        X[self._yn] = y
        return self.mi.fit_transform(X)

    @check_nan_columns
    def fit(self, X, y):
        """Fit model specified to multiply imputed dataset."""
        mi_data = self._fit_strategy_validator(X, y)
        return mi_data
