def row_transform(image, pixel_size, name=False):
    """
    Kiszámolja a kép soronkénti DFT-jét és ábrázol.
    """
    # arrayek létrehozása 
    fft_size = (image.shape[0], int((image.shape[1] / 2) + 1))
    imag_unit = 0 + 0j
    fft_matrix = np.zeros(fft_size) * imag_unit
    freq_matrix = np.zeros(fft_size)
    
    # DFT számolás
    for i in range(image.shape[0]):
        fft_matrix[i] = np.fft.rfft(image[i] - image[i].mean())
        freq_matrix[i] = np.fft.rfftfreq(image.shape[1], d=pixel_size)
    
    # ábrázolás
    plt.figure(figsize=(10,13))
    
    plt.pcolormesh(abs(fft_matrix[: , 1:]))
    
    plt.ylim(fft_matrix.shape[0], 0)
    
    plt.xticks(np.linspace(1,fft_matrix.shape[1]-1,5), np.round_(np.linspace(freq_matrix[0][1]  *1e-7, freq_matrix[0][-1]  *1e-7, 5), decimals=2), fontsize=22)
    plt.yticks(fontsize=22)
    
    plt.xlabel(r'Frekvencia [1/m $ \cdot 10^7$]', fontsize=27)
    plt.ylabel("Sor száma", fontsize=27)

    cbar = plt.colorbar()
    cbar.set_label("Intenzitás", fontsize=27)
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(20)
    
    # mentés
    if (name != False):
        plt.savefig("../latex/images/" + name + ".png", dpi=300)




            
def analize_row(image, row, pixel_size, Afreq=False, name=False, micron=False):
    """
    A megadott sorra jellemző hullámhossz megállapítását teszi lehetővé kiegészítő függvények segítségével. Utoljára az ábrázoláshoz használtam.
    """
    # arrayek létrehozása
    y = image[row, :]
    x = np.linspace(1, len(y), len(y))    
    
    # sor Fourier transzformáltja
    fft = np.fft.rfft(image[row] - image[row].mean())
    freq = np.fft.rfftfreq(image.shape[1], d=pixel_size)
    
    # ábrázolás
    plt.figure(figsize=(20,10))
    
    # ezt csak az adatfeldolgozáshoz használtam, de nem lesz tőle szép az ábra
    #plt.plot(x, y.mean() + (y.mean()/10)* np.sin(pixel_size*Afreq * x), color="red")
    
    plt.plot(x,y)
       
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    
    plt.xlabel(r'x [$\mu$m]', fontsize=27)
    plt.ylabel(r'z [ ]', fontsize=27)

    # mentés
    if (name != False):
        plt.savefig("../latex/images/" + name + "_1.png", dpi=300)
        
        
    # az ábra valódi méreteinek prezentálásához szükséges paraméterek
    height = int(image.shape[1] / 100 * 85)
    height2 = int(image.shape[1] / 100 * 15)
    percent = 0.3
    length = percent * image.shape[0] * pixel_size * 1e6
    
    if (micron != False):
        percent = micron / (image.shape[0] * PIXEL_SIZE * 1e6)
        length = micron
    
    
    # második ábra
    plt.figure(figsize=(20,10))

    plt.imshow(image, cmap="gray")
    plt.axhline(row, color="orange", linewidth=5)
    
    # ezt csak az adatfeldolgozáshoz használtam, de nem lesz tőle szép az ábra
    #plt.plot(x, row + (row/10) * np.sin(pixel_size * Afreq * x), color="red", linewidth=5)

    plt.tick_params(left=False,
        bottom=False,
        labelleft=False,
        labelbottom=False)
    
    # az ábrára jellemző mikrométeres szakasz felhelyezése a nagyságrendek bemutatására
    if (micron == False):
        if ((row / len(y)) > 0.8):
            plt.axhline(height2, 0.1, 0.4, linewidth=10, color="k", label=r'$\bf{%.1f \;\; \mu m}$' % length)
            leg = plt.legend(loc='upper left', framealpha=0, fontsize=26)
            for lh in leg.legendHandles: 
                lh.set_alpha(0)
        if ((row / len(y)) < 0.8):
            plt.axhline(height, 0.1, 0.4, linewidth=10, color="k", label=r'$\bf{%.1f \;\; \mu m}$' % length)
            leg = plt.legend(loc='lower left', framealpha=0, fontsize=26)
            for lh in leg.legendHandles: 
                lh.set_alpha(0)
    if (micron != False):
        if ((row / len(y)) > 0.8):
            plt.axhline(height2, 0.1, percent + 0.1, linewidth=10, color="k", label=r'$\bf{%d \;\; \mu m}$' % length)
            leg = plt.legend(loc='upper left', framealpha=0, fontsize=26)
            for lh in leg.legendHandles: 
                lh.set_alpha(0)
        if ((row / len(y)) < 0.8):
            plt.axhline(height, 0.1, percent + 0.1, linewidth=10, color="k", label=r'$\bf{%d \;\; \mu m}$' % length)
            leg = plt.legend(loc='lower left', framealpha=0, fontsize=26)
            for lh in leg.legendHandles: 
                lh.set_alpha(0)

    # mentés
    if (name != False):
        plt.savefig("../latex/images/" + name + "_2.png", dpi=300)

        

    # harmadik ábra
    plt.figure(figsize=(20,10))
    
    plt.plot(freq, abs(fft))
    plt.axvline(Afreq, color="red", label="Kiválasztott frekvencia")

    plt.grid()
    
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)

    plt.xlabel("Frequency", fontsize=27)
    plt.ylabel("Amplitude", fontsize=27)
    
    plt.legend(fontsize=25)
    
    # mentés
    if (name != False):
        plt.savefig("../latex/images/" + name + "_3.png", dpi=300)





def abra(path, name, PIXEL_SIZE):
    """
    A feldolgozott képek ábrázolásához írt függvény.
    """
    # az elérés útjai
    if (path == 1):
        path = '../data/PD01_Cu_pillar/20220428/selected_data_platina/'
    if (path == 2):
        path = '../data/PD01_Cu_pillar/20220406/selected_data/'
    
    # beolvasás
    image = imageio.imread(path + name + ".tif")

    # az ábra valódi méreteinek prezentálásához szükséges paraméterek
    height = int(image.shape[1] / 100 * 85)
    length = 0.3 * image.shape[0] * PIXEL_SIZE * 1e6
    length = int(length - length % 5)
    
    # ábrázolás
    plt.figure(figsize=(10,10))
    
    plt.imshow(image, cmap="gray")
    plt.axhline(height, 0.1, 0.4, linewidth=10, color="k", label=r'$\bf{%d \;\; \mu m}$' % length)
    leg = plt.legend(loc='lower left', framealpha=0, fontsize=26)
    
    for lh in leg.legendHandles: 
        lh.set_alpha(0)

    plt.tick_params(left=False,
        bottom=False,
        labelleft=False,
        labelbottom=False)
    
    # mentés
    plt.savefig("../latex/images/" + name + "_new.png", dpi=300)

    
    
    
    
def func(phi):
    """
    A Bradley--Harper cikkben szereplő ábra reprodukálása adott paraméterek esetén.
    """
    
    # beesés szöge
    phi = 2*np.pi/360 *phi
    
    # a cikkben szereplő szögfüggő tagok
    A = (a/alpha)**2 * np.sin(phi)
    B_1 = (a/alpha)**2 * np.sin(phi)**2 + (a/beta)**2 * np.cos(phi)**2
    B_2 = (a/alpha)**2 * np.cos(phi)
    C = 1/2 * ((a/beta)**2 - (a/alpha)**2) * np.sin(phi) * np.cos(phi)
    
    # a porlasztási hozam
    Y_0_1 = Lambda * epsilon * n * a / ((2*np.pi)**(1/2) * alpha * beta)
    Y_0_2 = np.exp(-a**2 / (2 * alpha**2) * B_1**(-1/2))
    Y_0_3 = np.exp(A**2 / (2*B_1**2))
    Y_0 = Y_0_1 * Y_0_2 * Y_0_3
    
    # a gamma függvények
    func_1 = A/B_1 * np.sin(phi)
    func_2 = B_2 / (2*B_1) * (1 + A**2 / B_1) * np.cos(phi)
    func_3 = A * C / B_1**2 * (3 + A**2 / B_1) * np.cos(phi)
      
    gamma_one = func_1 - func_2 - func_3
    gamma_two = - beta**2 / a**2 * (1/2 * B_2 + A * C / B_1) * np.cos(phi)
    
    # az elfordulási szög számolása
    loc = (abs(gamma_one - gamma_two) < 0.001) * phi
    theta_c = loc.max()

    return gamma_one, gamma_two, theta_c