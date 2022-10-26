import pandas as pd
import statsmodels.api as sm
import numpy as np
from patsy import dmatrices
from re import sub, escape
import re

df = pd.read_csv('data.csv')


y, X = dmatrices('y ~ 0 + x', data=df, return_type='dataframe')

fitted = sm.GLM(y, X, family=sm.families.Binomial(), missing='drop').fit()


coef = fitted.params

coef.mean()

coef.index.tolist()


def useRegex(input):
    pattern = re.compile(r"[a-zA-Z]\\[dfdf]", re.IGNORECASE)
    return pattern.match(input)


coef.index.tolist()[0].replace('/[[\]]/g', '')

pd.concat([coef, pd.Series(coef.mean(), index=['x[new]'])])

res = pd.DataFrame({
    'x': [sub(r'[x, \[\]]', '', index) for index in coef.index.tolist()],
    'values': coef.tolist()
})
