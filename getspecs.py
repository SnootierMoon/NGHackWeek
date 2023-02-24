#TODO: find the actual spec number, not just the string 
#TODO: find name of item (easier to do in getlinks) 
import requests
from bs4 import BeautifulSoup
import asyncio

class Product:
        def __init__(self, name, url, specs):
            self.name = name
            self.url = url
            self.specs = specs

def add_urls(urls):
    products = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        divs = soup.find('div', {'class': 'specs-table'})
        if divs: 
            divs = divs.find_all('div', {'class': 'border-bottom'})

        specs = {}
        if divs:
            for i in range(0, len(divs), 2):
                specs[divs[i].get_text()] = divs[i+1].get_text() #fix
        
        products.append(Product(url, url, specs))
    return products
        
    
def main():
    urls = ['/products/tensortech-cmg-40m-control-moment-gyroscope', '/products/tensortech-cmg-20m-control-moment-gyroscope', '/products/tensortech-adcs-40m-integrated-attitude-determination-and-control-system', '/products/tensortech-adcs-10m-integrated-attitude-determination-and-control-system', '/products/tensortech-cmg-10m-control-moment-gyroscope', '/products/berlin-space-tech-rwa05-24', '/products/berlin-space-tech-rwa05', '/products/rocketlab-60-mnms-reaction-wheel', '/products/rocketlab-400-mnms-reaction-wheel', '/products/rocketlab-10-mnms-reaction-wheel', '/products/rocketlab-3-mnms-reaction-wheel', '/products/rocketlab-1nms-reaction-wheel', '/products/rocketlab-30-mnms-reaction-wheel', '/products/rocketlab-200-mnms-reaction-wheel', '/products/cosats-cosrw15-15mnms-reaction-wheel', '/products/cosats-cosrw300-300mnms-reaction-wheel', '/products/cosats-cosrw600mnms-reaction-wheel', '/products/arcsec-arcus-adcs', '/products/aspina-reaction-wheel-for-100-kg-class-small-satellites', '/products/comat-reaction-wheel-60', '/products/comat-reaction-wheels-20', '/products/comat-reaction-wheels-40', '/products/veoware-space-rw500', '/products/cubespace-cubeadcs-3-axis', '/products/cubespace-cube-wheel-medium', '/products/cubespace-cube-wheel-small-plus', '/products/cubespace-cube-wheel-small', '/products/cubespace-cube-wheel-large', '/products/collins-aero-rsi-18-220-45', '/products/spaceteq-reaction-wheel-rw-10nms', '/products/cgsatellite-flywheel', '/products/bluecanyontech-rwp100-reaction-wheel', '/products/astrofein-rw-1-type-a', '/products/bluecanyontech-rwp500-reaction-wheel', '/products/collins-aero-rsi-30-280-30', '/products/bluecanyontech-rwp015-reaction-wheel', '/products/bluecanyontech-rwp050-reaction-wheel', '/products/astrofein-rw-1-type-b', '/products/microsat-systems-canada-micro-wheel-1000', '/products/collins-aero-rsi-45-75-60', '/products/progresja-space-mrw-50h', '/products/collins-aero-rsi-4-75-60', '/products/bluecanyontech-rw4-reaction-wheel', '/products/newspace-systems-nrwa-t065-reaction-wheel', '/products/collins-aero-rsi-12-75-60', '/products/microsat-systems-canada-micro-wheel-200', '/products/collins-aero-rsi-15-215-20', '/products/progresja-space-mrw-50l', '/products/microsat-systems-canada-micro-wheel-4000', '/products/newspace-systems-nrwa-t2-reaction-wheel', '/products/aac-clyde-trillian-1-reaction-wheel', '/products/bradford-reaction-wheel-unit-w45', '/products/aac-clyde-rw400-cubesat-reaction-wheels', '/products/bluecanyontech-rw8-reaction-wheel', '/products/arcsec-reaction-wheel', '/products/aac-clyde-rw210-cubesat-reaction-wheels', '/products/bradford-reaction-wheel-unit-w18', '/products/bradford-reaction-wheel-unit-w18es', '/products/bluecanyontech-rw1-reaction-wheel', '/products/progresja-space-mrw-35', '/products/collins-aero-rsi-68-170-60', '/products/wittenstein-cyber-motor-cyber-reaction-wheel-2', '/products/gnssmart-gs-rw-reaction-wheels', '/products/tamagawa-seiki-reaction-wheel-for-microsatellite', '/products/oce-technology-rw250b-momentum-wheel-25nms-b', '/products/oce-technology-rw1000-reaction-wheel', '/products/oce-technology-rw500-sgcmg-50nms', '/products/oce-technology-rw250-reaction-wheel-25nms', '/products/oce-technology-rw40-reaction-wheel-4nms', '/products/oce-technology-rw5-single-axis-micro-wheel-500m-nms', '/products/oce-technology-rw150-reaction-wheel-15nms', '/products/aac-clyde-i-adcs200-attitude-determination-and-control-system', '/products/aac-clyde-i-adcs400-attitude-determination-and-control-system', '/products/honeywell-aero-m50-cmg', '/products/astrofein-reaction-wheel-1', '/products/sinclair-interplanetary-picosatellite-reaction-wheels-rw-0-003', '/products/sinclair-interplanetary-rw3-1-0', '/products/sinclair-interplanetary-rw4-1-0', '/products/sinclair-interplanetary-rw-0-01', '/products/sinclair-interplanetary-rw-0-03', '/products/sinclair-interplanetary-rw3-0-060', '/products/sinclair-interplanetary-rw4-0-2-rw4-0-4', '/products/vectronic-aerospace-reaction-wheel-vrw-1', '/products/astrofein-rw-250', '/products/collins-aero-rsi-01-5-15', '/products/vectronic-aerospace-reaction-wheel-vrw02', '/products/astrofein-rw-35', '/products/honeywell-aero-hr-0610', '/products/collins-aero-rsi-01-5-28i', '/products/collins-aero-rdr-68', '/products/pumpkin-miniature-3-axis-reaction-wheel-attitude-determination-and-control-system-for-cube-sat-kit-nanosatellites', '/products/astrofein-rw-150', '/products/astrofein-rw-90', '/products/millennium-space-systems-rwa1000-small-reaction-wheel', '/products/pumpkin-miniature-3-axis-reaction-wheel-adcs', '/products/comat-reaction-wheels-180', '/products/serenumspace-rw25-cubesat-reaction-wheel', '/products/comat-sadm-400-solar-array-drive-mechanism', '/products/myonic-bearings-for-reaction-wheels-and-gyroscopes', '/products/newspace-systems-nmtr-x-custom-magnetorquer-rod', '/products/bluecanyontech-cmg-8', '/products/bluecanyontech-cmg-12', '/products/newspace-systems-nctr-m003-magnetorquer-rod', '/products/newspace-systems-nctr-m016-magnetorquer-rod', '/products/newspace-systems-nctr-m012-magnetorquer-rod', '/products/bluecanyontech-xact-100', '/products/bluecanyontech-xact-50', '/products/bluecanyontech-flexcore', '/products/bluecanyontech-xact-15', '/products/cosats-cosmtq-three-axis-magnetorquers', '/products/serenumspace-vac02-adcs', '/products/arquimea-aqtmc01-tmtc-assp-16b-adc', '/products/orbastro-orb-3-3u-satellite-platform', '/products/orbastro-orb-6-6u-satellite-platform', '/products/berlin-space-tech-i-adcs-100', '/products/cubespace-cube-torquer-large', '/products/cubespace-cube-torquer-small', '/products/cubespace-cube-torquer-medium', '/products/cubespace-cube-torquer-coil', '/products/zarm-technik-magnetic-torquers', '/products/aac-clyde-mtq800-magnetorquers', '/products/space-structures-high-vibration-damping-parts', '/products/aitech-defense-systems-s940-3u-compact-pci-digital-i-o-board', '/products/dsi-aerospace-on-board-computer', '/products/busek-bit-3']
    
    products = add_urls(urls)

    for p in products: 
        print(p.name + ":")
        for spec in p.specs:
            print("\t"+spec+": "+p.specs[spec])



if __name__ == "__main__":
    main()
        
        








    
