class yakuza:
    def __init__(self,position='Rookie'):
        self.position=position
    
    def get_family(self,family='kazama'):
        return family



def celcius(degrees):
    return (9/5*degrees+32)


values=[10,11,12]
results=map(celcius,values)


