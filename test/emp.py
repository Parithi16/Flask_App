

def cal_emp_salary(salary,bonus):
    if(salary<0 or bonus<0):
        raise ValueError("Basic salary or bonus cannot be negative")
    return salary*12 + bonus

