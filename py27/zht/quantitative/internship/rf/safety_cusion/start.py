#-*-coding: utf-8 -*-
#@author:tyhj


#input
total_position_ratio=0.3
amount=1000000
cash=1000000
predict_bottom_price=5.12
current_price=8.30
stop_profit=9.58
times=4

#devariate
total_position=amount*total_position_ratio


short_term_revenue=16582.58
long_term_revenue=1034.04

#output
short_term_ratio=0.8
short_term_position=total_position*short_term_ratio
breakeven_loss_rate=1.0/times
times_risk_score=2*times if times<=5.0 else 10
bonus_to_times_risk_score=((current_price-predict_bottom_price)/(stop_profit-predict_bottom_price))*10.0
total_risk_score=times_risk_score+bonus_to_times_risk_score
suggested_times=bonus_to_times_risk_score
short_term_return=short_term_revenue/short_term_position

def get_long_term_position():
    v=(short_term_revenue+long_term_revenue)*times
    if v<=total_position*0.2:
        long_term_position=total_position*0.2
    elif v-

long_term_position=(short_term_revenue+long_term_revenue)*times
long_term_return=long_term_revenue/long_term_position


cash=cash-(long_term_position-)


