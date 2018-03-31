#-*-coding: utf-8 -*-
#@author:tyhj

#input
total_position_ratio=0.2
amount=6000000
cash=6000000
predict_bottom_price=5.12
current_price=8.30
stop_profit_price=9.58
cusion_times=4
short_term_revenue=1935.32
long_term_revenue=1034.34
short_term_ratio=0.8 #default


#devariate
total_position=amount*total_position_ratio
short_term_position=total_position*short_term_ratio
breakeven_loss_range=1.0/cusion_times
cusion_times_risk_score=2*cusion_times if cusion_times<=5.0 else 10.0
bonus_to_cusion_times_risk_score=((current_price-predict_bottom_price)/(stop_profit_price-predict_bottom_price))*10.0
total_risk_score=cusion_times_risk_score+bonus_to_cusion_times_risk_score
suggested_cusion_times=bonus_to_cusion_times_risk_score
short_term_return=short_term_revenue/short_term_position

def get_long_term_position():
    v=(short_term_revenue+long_term_revenue)*cusion_times
    if v<=total_position*0.2:
        long_term_position=total_position*0.2
    elif v>cash:
        long_term_position=cash
    else:
        long_term_position=v
    return long_term_position

long_term_position=get_long_term_position()
cash_remained=cash-(long_term_position-total_position*0.2)





# update_long_term_position()
# cash=cash-(long_term_position-previous_long_term_position)
#
# with open('test.csv','w') as f:
#     f.write('amount,cash,total_position_ratio,total_position,short_term_ratio,'
#             +'short_term_position,long_term_position,cash,short_term_revenue,'
#             +'long_term_revenue,short_term_return,long_term_return,'
#             +'breakeven_loss_range,cusion_times_risk_score,bonus_to_cusion_times_risk_score,'
#             +'total_risk_score,suggested_cusion_times\n')
#     values=[amount,cash,total_position_ratio,total_position,short_term_ratio,
#             short_term_position, long_term_position, cash, short_term_revenue,
#             long_term_revenue, short_term_return, long_term_return,
#             breakeven_loss_range, cusion_times_risk_score, bonus_to_cusion_times_risk_score,
#             total_risk_score, suggested_cusion_times
#             ]
#     f.write(','.join([str(va) for va in values])+'\n')
























































































































