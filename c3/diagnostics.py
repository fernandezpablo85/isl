import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn import preprocessing
import numpy as np


line_kw = {'color':'red', 'alpha':0.5}
scatter_kw = {'marker':'o', 'edgecolors':'black', 'color':'white'}


def lm_plots(model, y):
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

    _plot_residuals(model, y, ax=ax1)
    _plot_qq(model, y, ax=ax2)
    _plot_scale(model, y, ax=ax3)
    _plot_leverage(model, y, ax=ax4)    
    

def _plot_residuals(model, y, ax):
    fitted = model.predict()
    residuals = y - fitted
    sns.residplot(fitted, residuals, lowess=True, line_kws=line_kw, scatter_kws=scatter_kw, ax=ax)
    ax.set_xlabel('fitted values')
    ax.set_ylabel('residuals')
    ax.set_title('Residuals vs Fitted')
    

def _plot_qq(model, y, ax):
    fitted = model.predict()
    residuals = y - fitted
    sd_residuals = preprocessing.scale(residuals)
    (x, y), (slope, intercept, _) = stats.probplot(sd_residuals, plot=None)
    ax.scatter(x, y, **scatter_kw);
    ax.plot(x, [_x * slope + intercept for _x in x], **line_kw)
    ax.set_title('Normal Q-Q')
    ax.set_xlabel('Theoretical quantiles')
    ax.set_ylabel('Standarized residuals')
    
    
def _plot_scale(model, y, ax):
    fitted = model.predict()
    residuals = y - fitted
    abs_sqrt_resid = np.sqrt(np.abs(residuals))
    sns.regplot(fitted, abs_sqrt_resid, lowess=True, line_kws=line_kw, scatter_kws=scatter_kw, ax=ax)
    ax.set_title('Scale-Location')
    ax.set_xlabel('Fitted values')
    ax.set_ylabel('Absolute Sqrt Residuals')

    
def _plot_leverage(model, y, ax):
    fitted = model.predict()
    residuals = y - fitted
    sd_residuals = preprocessing.scale(residuals)
    leverage = model.get_influence().hat_matrix_diag
    ax.scatter(leverage, sd_residuals, **scatter_kw);
    ax.set_xlim(0.001, )
    ax.set_title('Residuals vs Leverage')
    ax.set_xlabel('Leverage')
    ax.set_ylabel('Standardized Residuals')
