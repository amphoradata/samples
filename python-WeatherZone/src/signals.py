from amphora_client import SignalDto

def signals():
    return [
        SignalDto(_property='description', value_type='String'),
        SignalDto(_property='temperature', value_type='Numeric'),
        SignalDto(_property='rainProb', value_type='Numeric'),
        SignalDto(_property='windSpeed', value_type='Numeric'),
        SignalDto(_property='windDirection', value_type='Numeric'),
        SignalDto(_property='cloudCover', value_type='Numeric'),
        SignalDto(_property='pressure', value_type='Numeric'),
    ]
