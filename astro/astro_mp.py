from datetime import datetime
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpmath import *
mp.dps = 10_000

def read_file(path, column1, column2, column3=None):
    """
    function for easy reading of csv files
    """
    with open(path) as f:
        raw = csv.reader(f)
        raw_list = list(raw)
        if column3 is None:
            return [[ls[column1], ls[column2]] for ls in raw_list]  # just the columns that are needed
        else:
            return [[ls[column1], ls[column2], ls[column3]] for ls in raw_list]
def ra_mp(data):
    ra_ls = [[mpmathify(ls[1][3:5]),mpmathify(ls[1][6:8]),mpmathify(ls[1][9:-1])] for ls in data]
    return [fsum([fdiv(ls[0],24),fdiv(ls[1],(60*24)),fdiv(ls[2],(60*60*24))])*360 for ls in ra_ls]
def elong_mp(elongation:str):
    """
    function for converting the elongation angle from string to float
    """
    elongation = elongation[:-10] + elongation[-9:]
    ls = elongation.replace('"','').replace("'",'°').split('°')
    return mpmathify(ls[0])+ fdiv(mpmathify(ls[1]),60)  + fdiv(mpmathify(ls[2]),3600)
def string_to_seconds(date_string, epoch=datetime(1970, 1, 1)):#the function you gave us
    """
    Convert a date string of the form 'YYYY-MM-DD HH:MM:SS' to the number of
    seconds since a given epoch.
    Args:
    date_string (str): Date string to convert.
    epoch (datetime.datetime, optional): Epoch to calculate seconds from.
    Defaults to 1970-01-01 00:00:00.
    Returns:
    int: Number of seconds since the epoch.
    """
    date_time_obj = datetime.strptime(date_string, ' %Y-%m-%d %H:%M:%S')
    seconds_since_epoch = (date_time_obj - epoch).total_seconds()
    return int(seconds_since_epoch)
def data_to_seconds(data):
    """
    Function That Takes In A Metrix Data from Stellarium In Which
    The Time Is In The First Index Of Each list, And return A list
    Of The Times In The Form Of Integers Normalze To Start From 0
    """
    time_raw = [ls[0] for ls in data]
    start_seconds = string_to_seconds(time_raw[0])
    return [string_to_seconds(time)-start_seconds for time in time_raw]

sun_data2 = read_file("sun_data.csv",1,2,3)
sun_data2.pop(0)

ra = ra_mp(sun_data2)
dec = [elong_mp(deci[2]) for deci in sun_data2]
seconds = data_to_seconds(sun_data2)


def angle_between_stars(ra1, dec1, ra2, dec2):
    """
    Calculate the angle between two stars given in the equatorial coordinate
    system. The function gets the angles and converts them to radians.
    """
    # Convert the coordinates from degrees to radians
    ra1, dec1 = radians(ra1), radians(dec1)
    ra2, dec2 = radians(ra2), radians(dec2)
    # Calculate the angle using the spherical law of cosines
    angle = acos(fmul(sin(dec1),sin(dec2)) + fmul(fmul(cos(dec1),cos(dec2)),cos(ra1 - ra2)))
    return mp.degrees(angle) # Convert radians to degrees

def angle_between_stars2(ra1, dec1, ra2, dec2):
    """
    Calculate the angle between two stars given in the equatorial coordinate
    system. The function gets the angles and converts them to radians.
    """
    # Convert the coordinates from degrees to radians
    ra1, dec1 = radians(ra1), radians(dec1)
    ra2, dec2 = radians(ra2), radians(dec2)
    # Calculate the angle using the spherical law of cosines
    angle = fadd(fmul(sin(dec1), sin(dec2)), fmul(fmul(cos(dec1), cos(dec2)), cos(fsub(ra1, ra2))))
    return mp.degrees(angle) # Convert radians to degrees

before_arc_cos = []

sun_data2_clear = [seconds,ra,dec]
deltaTheta = []
deltaTime = []
time = []
for i in range(len(ra)-1):
    deltaTheta.append(angle_between_stars(ra[i],dec[i],ra[i+1],dec[i+1]))
    before_arc_cos.append(angle_between_stars2(ra[i],dec[i],ra[i+1],dec[i+1]))
    deltaTime.append(seconds[i+1]-seconds[i])
    time.append(0.5*(seconds[i+1]+seconds[i]))
sun_data_delta = [deltaTheta,deltaTime,time]
omega = [fdiv(thetai,timei) for thetai,timei in zip(deltaTheta,deltaTime)]
sun_data_omega = [omega,time]

print(deltaTheta[4])
#plt.scatter(time,omega)
#plt.ylim(top = 1.23*10**(-5),bottom = 1.08*10**(-5))
#plt.show(block=True)
def std(ls):
    avg = fdiv(fsum(ls),len(ls))
    return sqrt(fdiv(fsum((power(fsub(num,avg),2)) for num in ls),len(ls)))
def std_norm(ls):
    avg = fdiv(fsum(ls),len(ls))
    a = std(ls)
    return fdiv(a,(fadd(a,fabs(avg))))

with open("results.csv",'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["before","after"])
    writer.writerow([std_norm(before_arc_cos),std_norm(deltaTheta)])


