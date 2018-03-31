#-*-coding: utf-8 -*-
#@author:tyhj
import normalize_the_factors
import get_month_returns
import preprocess_SW_industry
import solve_the_model
import get_cross_regression_data
import preprocess_the_src_data
import analyse

preprocess_the_src_data.unify_filenames()
get_month_returns.get_month_returns()
preprocess_SW_industry.change_the_industry_format()
normalize_the_factors.run()
get_cross_regression_data.run()
solve_the_model.run()
analyse.compare_fc_with_benchmark()







