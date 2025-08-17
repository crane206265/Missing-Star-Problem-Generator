import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import random

#pdf = PdfPages('Star Chart.pdf')
download_path = "C:/Users/dlgkr/OneDrive/Desktop/code/starmap/"

df = pd.read_csv("D:/자료/starmap/hip1.csv")

df = pd.DataFrame(df, columns=['RAJ2000','DEJ2000','Vmag'])
ra = df['RAJ2000'].to_numpy()
dec = df['DEJ2000'].to_numpy()
mag = df['Vmag'].to_numpy()
ra = ra*np.pi/180
dec = dec*np.pi/180

############################### setting #####################################

mag_lim = 6#5.5 #성도 한계 등급
missing_cnt = 5 #미싱스타 개수
missing_lim = 2.5 #미싱스타 한계 등급
mode = 1 #나는 1을 놀이용으로 쓰고 2를 대회용으로 썼음
adding_cnt = 0 #에딩스타 개수
adding_inf = -2 #에딩스타 등급 하한
adding_sup = 2 #에딩스타 등급 상한
low_a = 10 #미싱/에딩스타의 가장 낮은 고도 (degree 단위)
map_num = 5 #성도 개수
lat_inf = -90 #위도 하한
lat_sup = 90 #위도 상한

#############################################################################

lat = 180
while(lat >= lat_inf and lat <= lat_sup):
    lat = np.pi*np.random.rand(1) - 0.5*np.pi
lst = 2*np.pi*np.random.rand(1)

def a_func(raf, decf, latf, lstf):
    haf = lstf - raf
    sin_af = np.sin(latf)*np.sin(decf) + np.cos(latf)*np.cos(decf)*np.cos(haf)
    return np.arcsin(sin_af)

def az_func(af, raf, decf, latf, lstf):
    haf = lstf - raf
    cos_az = (np.sin(decf) - np.sin(latf)*np.sin(af))/(np.cos(latf)*np.cos(af))
    sin_az = -np.cos(decf)*np.sin(haf)/np.cos(af)
    az_0 = np.arcsin(sin_az)
    if sin_az >= 0 and cos_az >= 0:
        az = az_0
        k = 0
    elif sin_az >= 0 and cos_az < 0:
        az = np.pi - az_0
        k = 1
    elif sin_az < 0 and cos_az < 0:
        az = -np.pi - az_0
        k = 2
    elif sin_az < 0 and cos_az >=0:
        az = az_0
        k = 3
    return az    

#print(lat*180/np.pi)
#print(lst*180/np.pi)

def plotsetting():
    ax = fig.add_subplot(projection='polar')
    plt.grid(False)
    ax.set_ylim(0, 1)
    #ax.set_facecolor('k')
    title = 'Star Chart (latitude :' + str(lat*180/np.pi) + 'degree , LST :' + str(lst*12/np.pi) + 'hour)'
    ax.set_title(title , va='bottom')
    ax.set_yticks(np.arange(0,1,1), labels=[''])
    ax.set_xticks(np.arange(0,2.0*np.pi,np.pi/12.0), labels=['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

for j in range(map_num):

    az_random = 2*np.pi*np.random.rand(1)
    star_num = [x for x in range(len(mag)) if mag[x] < mag_lim and a_func(ra[x], dec[x], lat, lst) >= 0]

    #일반 성도
    """
    fig = plt.figure(figsize=(20, 20))
    plotsetting()

    for i in star_num:
        a_val = a_func(ra[i], dec[i], lat, lst)
        az_val = az_func(a_val, ra[i], dec[i], lat, lst) + az_random
        #print(ra[i], dec[i], mag[i])
        z_val = np.pi/2 - a_val
        l_val = np.sin(z_val)/(1+np.cos(z_val))#2*z_val/np.pi #놀이용
        #l_val = z_val #평사도법 - 대회 준비용  
        star_size = 10**(0.40*(6-mag[i])) - 0.7 #0.38 - 대회 준비용 / 0.40 - 놀이용
        plt.scatter(az_val, l_val, s = star_size, color='k')

    #print(mag[24420], ra[24420], dec[24420])
    #print(mag[27968], ra[27968], dec[27968])
    
    pdf.savefig(fig)
    """

    #missing star
    fig = plt.figure(figsize=(20, 20))
    plotsetting()

    missing_star_num = [x for x in range(len(mag)) if mag[x] < missing_lim and a_func(ra[x], dec[x], lat, lst) >= low_a*np.pi/180]
    random.shuffle(missing_star_num)

    adding_star = []
    while(adding_cnt > 0):
        add_ra = 2*np.pi*random.random()
        add_dec = np.pi*random.random() - np.pi/2
        add_mag = (adding_sup-adding_inf)*random.random() + adding_inf
        if a_func(add_ra, add_dec, lat, lst) >= low_a*np.pi/180:
            add_a = a_func(add_ra, add_dec, lat, lst)
            add_az = az_func(add_a, add_ra, add_dec, lat, lst) + az_random
            adding_star.append((add_a, add_az, add_mag))
            adding_cnt = adding_cnt - 1

    for i in star_num:
        a_val = a_func(ra[i], dec[i], lat, lst)
        az_val = az_func(a_val, ra[i], dec[i], lat, lst) + az_random
        #print(ra[i], dec[i], mag[i])
        z_val = np.pi/2 - a_val
        if mode == 1:
            l_val = np.sin(z_val)/(1+np.cos(z_val)) #2*z_val/np.pi #놀이용
            star_size = 10**(0.40*(6-mag[i])) - 0.7 #0.38 - 대회 준비용 / 0.40 - 놀이용
        elif mode == 2:
            l_val = z_val #평사도법 - 대회 준비용  
            star_size = 10**(0.38*(6-mag[i])) - 0.7 #0.38 - 대회 준비용 / 0.40 - 놀이용
        if not(i in missing_star_num[:missing_cnt]):
            plt.scatter(az_val, l_val, s = star_size, color='k')

    for star_info in adding_star:
        z_val = np.pi/2 - star_info[0]
        if mode == 1:
            l_val = np.sin(z_val)/(1+np.cos(z_val))
            star_size = 10**(0.40*(6-star_info[2])) - 0.7
        elif mode == 2:
            l_val = z_val
            star_size = 10**(0.38*(6-star_info[2])) - 0.7
        plt.scatter(star_info[1], l_val, s = star_size, color='k')
    
    plt.savefig(download_path+"starmap"+str(j)+".png")
    #pdf.savefig(fig)

    #missing star solution
    fig = plt.figure(figsize=(20, 20))
    plotsetting()
    for i in star_num:
        a_val = a_func(ra[i], dec[i], lat, lst)
        az_val = az_func(a_val, ra[i], dec[i], lat, lst) + az_random
        #print(ra[i], dec[i], mag[i])
        z_val = np.pi/2 - a_val
        if mode == 1:
            l_val = np.sin(z_val)/(1+np.cos(z_val)) #2*z_val/np.pi #놀이용
            star_size = 10**(0.40*(6-mag[i])) - 0.7 #0.38 - 대회 준비용 / 0.40 - 놀이용
        elif mode == 2:
            l_val = z_val #평사도법 - 대회 준비용  
            star_size = 10**(0.38*(6-mag[i])) - 0.7 #0.38 - 대회 준비용 / 0.40 - 놀이용
        if i in missing_star_num[:missing_cnt]:
            plt.scatter(az_val, l_val, s = star_size, color='r')    
        else:
            plt.scatter(az_val, l_val, s = star_size, color='k')

    for star_info in adding_star:
        z_val = np.pi/2 - star_info[0]
        if mode == 1:
            l_val = np.sin(z_val)/(1+np.cos(z_val))
            star_size = 10**(0.40*(6-star_info[2])) - 0.7
        elif mode == 2:
            l_val = z_val
            star_size = 10**(0.38*(6-star_info[2])) - 0.7
        plt.scatter(star_info[1], l_val, s = star_size, color='b')

    #pdf.savefig(fig)
    plt.savefig(download_path+"starmapsol"+str(j)+".png")

    lat = np.pi*np.random.rand(1) - 0.5*np.pi
    lst = 2*np.pi*np.random.rand(1)
    print(lat*180/np.pi)
    print(lst*180/np.pi)
    print(j)
    plt.close()

#pdf.close()
#a Ori : 27968
#b Ori : 24420