from getspecs import Product
import sqlite3
import functools

def get_spec_names(product_list):
    return functools.reduce(lambda a,b: a.union(b), [set(prod.specs.keys()) for prod in product_list])

def interactive(product_list):
    spec_names = get_spec_names(product_list)
    db = sqlite3.connect(":memory:")
    db.execute('CREATE TABLE main_tbl(Name,' + ','.join(spec_names) + ');')
    for product in product_list:
        keys = ['Name'] + list(product.specs.keys())
        vals = [product.name] + list(product.specs.values())
        db.execute('INSERT INTO main_tbl(' + ','.join(keys) + ') VALUES(' + ','.join(['?' for x in vals]) + ');', vals)
    return db

if __name__ == "__main__":
    product_list = [
        Product('Reaction Wheel Assembly (RWA05-24)','https://satsearch.co/products/berlin-space-tech-rwa05-24',{'lead time': '12 mo', 'mass': '1.70 kg (RW + WDE + Gyro)1.55 kg (RW + WDE)', 'length': '105 mm', 'width': '106.6 mm', 'height': '109.5 mm', 'power supply': '5 V (electronics)7 to 24 V (motor)', 'power consumption': '0.5 W @ 5 V', 'power consumption (motor)': '0.15 A @ 3000 rpm0.9 A @ max. torque', 'angular speed': '500 to 5000 rpm', 'angular speed control accuracy': '±2 rpm', 'angular momentum storage': '0.5 N m s', 'net torque': '8.6 mN m @ 500 rpm6.8 mN m @ 5000 rpm', 'data interface': 'RS422', 'operating temperature': '-20 to 40 C', 'storage temperature ': '-30 to 50 C', 'radiation test (Co60)': '30 krad', 'lifetime': '5 years LEO'}),
        Product('Reaction Wheel Assembly (RWA-05)','https://satsearch.co/products/berlin-space-tech-rwa05',{'lead time': '4 to 6 mo', 'mass': '1.70 kg (RW + WDE + Gyro)1.55 kg (RW + WDE)', 'length': '105 mm', 'width': '106.6 mm', 'height': '109.5 mm', 'power supply': '5 V (electronics)17 to 32 V (motor)', 'power consumption': '0.5 W @ 5 V', 'power consumption (motor)': '0.07 A @ 3000 rpm0.8 A @ max. torque', 'angular speed': '500 to 5000 rpm', 'angular speed control accuracy': '±2 rpm', 'angular momentum storage': '0.5 N m s', 'net torque': '16.0 mN m @ 500 rpm14.2 mN m @ 5000 rpm', 'data interface': 'RS422', 'operating temperature': '-20 to 40 C', 'storage temperature ': '-30 to 50 C', 'radiation test (Co60)': '30 krad', 'lifetime': '5 years LEO'}),
        Product('60 mNms RW-0.06 Reaction Wheel','https://satsearch.co/products/rocketlab-60-mnms-reaction-wheel',{}),
        Product('400 mNms RW-0.4 Reaction Wheel','https://satsearch.co/products/rocketlab-400-mnms-reaction-wheel',{}),
        Product('10 mNms RW-0.01 Reaction Wheel','https://satsearch.co/products/rocketlab-10-mnms-reaction-wheel',{}),
        Product('3 mNms RW-0.003 Reaction Wheel','https://satsearch.co/products/rocketlab-3-mnms-reaction-wheel',{}),
        Product('1Nms RW-1.0 Reaction Wheel','https://satsearch.co/products/rocketlab-1nms-reaction-wheel',{}),
        Product('30 mNms RW-0.03 Reaction Wheel','https://satsearch.co/products/rocketlab-30-mnms-reaction-wheel',{}),
        Product('200 mNms RW-0.2 Reaction Wheel','https://satsearch.co/products/rocketlab-200-mnms-reaction-wheel',{}),
        Product('CMG-40m Control Moment Gyroscope','https://satsearch.co/products/tensortech-cmg-40m-control-moment-gyroscope',{'lead time': '5 to 8 mo', 'mass': '< 1000 g', 'volume': '4x Tuna-can & 0.4U', 'bus voltage': '5 V3.3 V', 'power consumption': '< 4 W @ 5 V< 1 W @ 3.3 V', 'maximum torque': '< 2 mN m for 1-axis (adjustable)< 3 mN m for 2-axis', 'maximum momentum storage': '< 20 mN m s for 1-axis (adjustable)< 30 mN m s for 2-axis', 'data interface': 'I2CUART RS422/485 (optional, only one of the two can be selected)'}),
        Product('COSRW15 15mNms Reaction Wheel','https://satsearch.co/products/cosats-cosrw15-15mnms-reaction-wheel',{}),
        Product('COSRW300 300mNms Reaction Wheel','https://satsearch.co/products/cosats-cosrw300-300mnms-reaction-wheel',{}),
        Product('COSRW600mNms Reaction Wheel','https://satsearch.co/products/cosats-cosrw600mnms-reaction-wheel',{}),
        Product('Arcus ADCS','https://satsearch.co/products/arcsec-arcus-adcs',{'power interface': '5 V3.3 V', 'data interface': 'I2CCAN ', 'power consumption': '940 to 1400 mW (depending on determination/control mode)', 'lead time': '6 mo', 'mass': '715 g', 'height': '50 mm', 'length': '96 mm', 'width': '91 mm'}),
        Product('Reaction Wheel (RW) for 100 kg-class small satellites','https://satsearch.co/products/aspina-reaction-wheel-for-100-kg-class-small-satellites',{}),
        Product('CMG-20m Control Moment Gyroscope','https://satsearch.co/products/tensortech-cmg-20m-control-moment-gyroscope',{'lead time': '4 to 7 mo', 'maximum torque': '< 1 mN m for 2-axis (adjustable)< 2 mN m for 1-axis', 'mass': '< 500 g', 'volume': '2x Tuna-can & 0.2U', 'bus voltage': '5 V3.3 V', 'power consumption': '< 1 W @ 5 V< 1 W @ 3.3 V', 'maximum momentum storage': '< 10 mN m s for 2-axis (adjustable)< 20 mN m s for 1-axis', 'data interface': 'I2CUART RS422/485 (optional, only one of the two can be selected)'}),
        Product('ADCS-40m Integrated Attitude Determination and Control System','https://satsearch.co/products/tensortech-adcs-40m-integrated-attitude-determination-and-control-system',{'lead time': '6 to 12 mo', 'mass': '< 1200 g', 'volume': '4 x Tuna-cans & 0.8U', 'supply voltage': '5 V3.3 V', 'power consumption': '< 1 W @ 3.3 V< 4 W @ 5 V', 'maximum torque': '< 3 mN m for 2-axis< 2 mN m for 1-axis (adjustable)', 'maximum momentum storage': '< 20 mN m s for 1-axis (adjustable)< 30 mN m s for 2-axis', 'pointing knowledge': '< ±0.1 deg (with sun)< ±1 deg (no sun)', 'pointing accuracy': '< ±0.2 deg (with sun)< ±1 deg (no sun)', 'data interface': 'I2CUART RS422/485 (optional, only one of the two can be selected)'}),
        Product('ADCS-10m Integrated Attitude Determination and Control System','https://satsearch.co/products/tensortech-adcs-10m-integrated-attitude-determination-and-control-system',{'lead time': '4 to 8 mo', 'mass': '< 300 g', 'volume': 'Tuna-can & 0.2U', 'supply voltage': '5 V3.3 V', 'power consumption': '< 1 W (both 5V bus and 3.3V bus)', 'maximum torque': '< 1 mN m for 2-axis (adjustable)', 'maximum momentum storage': '< 10 mN m s for 2-axis (adjustable)', 'pointing knowledge': '< ±0.1 deg (with sun)< ±1 deg (no sun)', 'pointing accuracy': '< ±0.2 deg (with sun)< ±1 deg (no sun)', 'data interface': 'I2CUART RS422/485 (optional, only one of the two can be selected)'}),
        Product('CMG-10m Control Moment Gyroscope','https://satsearch.co/products/tensortech-cmg-10m-control-moment-gyroscope',{'lead time': '3 to 6 mo', 'mass': '< 250 g', 'volume': 'Tuna-can & 0.1U', 'supply voltage': '5 V3.3 V', 'power consumption': '< 1 W (both 5V bus and 3.3V bus)', 'maximum torque': '< 1 mN m for 2-axis (adjustable)', 'maximum momentum storage': '< 10 mN m s for 2-axis (adjustable)', 'data interface': 'I2CUART RS422/485 (optional, only one of the two can be selected)'}),
        Product('Reaction Wheel 60','https://satsearch.co/products/comat-reaction-wheel-60',{'mass': '270 g', 'diameter': '65.6 mm', 'height': '44.8 mm', 'torque': '6 mNm mean', 'angular momentum storage': '60 mN m s', 'angular speed control accuracy': '> 2 rpm', 'lifetime1': '8 yr', 'data interface': 'RS 485 full duplex', 'operating temperature': '-30 to 50 C'}),
        Product('Reaction Wheels 20','https://satsearch.co/products/comat-reaction-wheels-20',{'mass': '180 g', 'length': '48 mm', 'width': '48 mm', 'height': '28.2 mm', 'torque': '2 mNm mean', 'angular momentum storage': '20 mN m s', 'angular speed control accuracy': '> 2 rpm', 'lifetime1': '8 yr', 'data interface': 'RS 485 full duplex', 'operating temperature': '-30 to 50 C'}),
        Product('Reaction Wheels 40','https://satsearch.co/products/comat-reaction-wheels-40',{'mass': '230 g (electronic and radiation protection included)', 'diameter': '67 mm', 'length': '44.8 mm', 'torque': '4 mN m', 'data interface': 'RS485', 'lifetime1': '8 yr', 'communication protocol': 'NSP', 'operating temperature': '-30 to 50 C', 'angular momentum storage': '40 mN m s', 'angular speed control accuracy': '2 rpm'}),
        Product('RW500','https://satsearch.co/products/veoware-space-rw500',{'mass': '0.8 kg', 'width': '97 mm', 'length': '97 mm', 'height': '40 mm', 'maximum momentum storage': '0.7 N m s', 'Nominal momentum storage': '0.5 to 0.7 N m s', 'maximum torque': '0.1 N m', 'torque': '0.05 N m', 'power consumption': '<3 W (nominal)', 'peak power': '< 30 W', 'voltage': '28 V', 'data interface': 'CANUART RS485 '}),
        Product('CubeADCS 3-Axis','https://satsearch.co/products/cubespace-cubeadcs-3-axis',{'lead time': '16 wk'})
    ]

