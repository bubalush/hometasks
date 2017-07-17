d_key = ['hostname', 'location', 'owner']
d_value = ['production', 'Minsk', 'Bel', 'true']

result = dict(zip(d_key, d_value + [None] * (len(d_key) - len(d_value))))
print (result)