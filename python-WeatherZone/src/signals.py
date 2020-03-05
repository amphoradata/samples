from amphora_client import Signal

def signals():
    return [
        Signal(_property='description', value_type='String'),
        Signal(_property='temperature', value_type='Numeric', attributes={'units': 'degrees C'}),
        Signal(_property='rainProb', value_type='Numeric', attributes={'units': '%'}),
        Signal(_property='windSpeed', value_type='Numeric', attributes={'units': 'km/h'}),
        Signal(_property='windDirection', value_type='Numeric', attributes={'units': 'degrees'}),
        Signal(_property='cloudCover', value_type='Numeric', attributes={'units': '%'}),
        Signal(_property='pressure', value_type='Numeric', attributes={'units': 'hPa'}),
        Signal(_property='rainfallRate', value_type='Numeric', attributes={'units': 'mm/h'})
    ]
