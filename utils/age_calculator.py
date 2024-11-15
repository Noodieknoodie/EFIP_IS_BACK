from datetime import datetime, date

def calculate_age(born):
    try:
        born = datetime.strptime(born, '%Y-%m-%d').date()
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except:
        return 0 