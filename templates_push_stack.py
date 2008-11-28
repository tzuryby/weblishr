
def format_gmt(dt):
    return datetime(*time.strptime(dt, "%Y-%m-%d %H:%M:%S")[0:5]).strftime('%a, %d %h %Y %H:%M:%S GMT')

sorted = sorted

