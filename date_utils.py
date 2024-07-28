from datetime import datetime

def parse_date(date_str):
    date_python = datetime.strptime(date_str, '%d %b %Y %H:%M')

    date_python = date_python.strftime('%d/%m/%Y')
    return date_python