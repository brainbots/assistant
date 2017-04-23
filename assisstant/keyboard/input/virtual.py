import time

def read(_, no_of_seconds):
    print("Started sleeping")
    time.sleep(no_of_seconds)
    print("Stopped sleeping")

    values={'O1':[],'O2':[],'P7':[],'P8':[]}
    for i in range(no_of_seconds*128):
        values['O1'].append(1)
        values['O2'].append(2)
        values['P7'].append(3)
        values['P8'].append(4)

    quality={'O1':[],'O2':[],'P7':[],'P8':[]}
    for i in range(no_of_seconds*128):
        quality['O1'].append(1)
        quality['O2'].append(2)
        quality['P7'].append(3)
        quality['P8'].append(4)

    return (values, quality)
