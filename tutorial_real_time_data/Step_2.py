# This function takes the current time and outputs the product of the hour, minutes and seconds

def time_product(date_time):
  time_hour = date_time.hour
  time_minute = date_time.minute
  time_second = date_time.second

  time_prod = time_hour * time_minute * time_second
  
  return time_prod
