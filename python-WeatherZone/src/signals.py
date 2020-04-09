

class sig():
    def __init__(self, prop, value_type, attributes = {}):
        self._property = prop
        self.value_type = value_type
        self.attributes = attributes
        
def signals() -> [sig]:
    return [
        sig('description', 'String'),
        sig('temperature', 'Numeric', {'units': 'degrees C'}),
        sig('rainProb', 'Numeric', {'units': '%'} ),
        sig('windSpeed', 'Numeric', {'units': 'km/h'}),
        sig('windDirection', 'Numeric', {'units': 'degrees'}),
        sig('cloudCover', 'Numeric', {'units': '%'}),
        sig('pressure', 'Numeric', {'units': 'hPa'}),
        sig('rainfallRate', 'Numeric', {'units': 'mm/h'}),
    ]
