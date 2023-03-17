import dpkt
import socket
import pygeoip

# Database of locations that will match to our IP addresses
gi = pygeoip.GeoIP('GeoLiteCity.dat')

# Translate IP addresses to geo locations
def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    # Input IP here
    src = gi.record_by_name('x.xxx.xxx.xxx')
    try:
        # Get coordinates using GeoLiteCity database
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        # Create record for destination IP
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

# Capture and plot the IP Addresses
def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            # Capture source and destination
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            # Place IPs
            KML = retKML(dst, src)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts


def main():
    # Open captured data
    f = open('wire.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    # Can input kml to google maps 
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter