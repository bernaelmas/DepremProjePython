import pandas as pd
import requests

# Admin bilgilerini saklayan bir sözlük
admin = {
    "kullaniciAdi": "bernaelms@gmail.com",
    "parola": "789456123"
}
# Menü seçeneklerini saklayan bir tuple
menuTuple = ("**Sisteme Hoşgeldiniz**\n1-Sisteme Üye Ol\n2-Sisteme Giriş Yap\n3-Şifremi Unuttum\n4-Admin Girişi\n5-Çıkış")
depremTuple = ("1-En Son Gerçekleşen Depremler\n2-Şehire Göre Depremler\n3-Büyüklüğe Göre Depremler\n4-Çıkış")

# Kullanıcının giriş yapma durumunu ve anlık kullanıcı adını saklayan değişkenler
girisYapildi = False
anlikKullanici = ""
dongu_bitir = False

# Sisteme üye olma fonksiyonu
def kayit():
    print("**Sisteme Üye Ol**")
    username = input("Kullanıcı Adı: ")
    password = input("Şifre: ")

    # Kullanıcıların kaydedildiği csv dosyasını okuma
    df = pd.read_csv('kullanicilar.csv')

    # Eğer kullanıcı adı zaten kayıtlıysa uyarı verme
    if username in df['Username'].values:
        print("Kullanıcı zaten kayıtlı!")
        return
    # Yeni kullanıcıyı csv dosyasına ekleme
    data = {'Username': [username], 'Password': [password]}
    df = pd.DataFrame(data)

    with open('kullanicilar.csv', 'a') as f:
        df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

    print("Başarıyla Üye Olundu.")

# Sisteme giriş yapma fonksiyonu
def giris():
    print("**Sisteme Giriş Yap**")
    username = input("Kullanıcı Adı: ")
    password = input("Şifre: ")

    # Kullanıcıların kaydedildiği csv dosyasını okuma
    df = pd.read_csv('kullanicilar.csv')
    # Kullanıcı adı ve şifresini kontrol etme
    login_df = df.loc[(df['Username'] == username) & (df['Password'] == password)]

    # Eğer giriş başarılıysa anlık kullanıcıyı güncelleme ve giriş yapıldığını belirtme
    if not login_df.empty:
        print("Başarıyla Giriş Yapıldı.")
        global anlikKullanici, girisYapildi  # Metod dışındaki değişkenlere erişmek için kullandım
        anlikKullanici = username
        girisYapildi = True
    else:
        print("Hatalı Kullanıcı Adı Veya Şifre.")
        return False

# Şifremi unuttum fonksiyonu
def sifremi_unuttum():
    print("**Şifremi Unuttum**")
    username = input("Kullanıcı Adı: ")

    # Kullanıcıların kaydedildiği csv dosyasını okuma
    df = pd.read_csv('kullanicilar.csv')

    # Eğer kullanıcı adı kayıtlıysa şifresini gösterme
    if username in df['Username'].values:
        password = df.loc[df['Username'] == username, 'Password'].values[0]
        print("Şifreniz: {}".format(password))
    else:
        print("Geçersiz Kullanıcı Adı!")

# Admin girişi fonksiyonu
def admin_giris():
    print("**Admin Girişi**")
    kullaniciAdi = input("Kullanıcı Adınızı Giriniz:")
    sifre = input("Şifrenizi Giriniz:")

    # Admin bilgilerini kontrol etme
    if kullaniciAdi == admin["kullaniciAdi"] and sifre == admin["parola"]:
        print("Admin Girişi Başarılı.")
        # Eğer giriş başarılıysa anlık kullanıcıyı güncelleme ve giriş yapıldığını belirtme
        global anlikKullanici, girisYapildi   # Metod dışındaki değişkenlere erişmek için kullandım
        anlikKullanici = kullaniciAdi
        girisYapildi = True
    else:
        print("Yanlış Kullanıcı Adı veya Şifre Girdiniz!")

# Sistemden çıkış yapma fonksiyonu
def cikis():
    print("Çıkış Yapıldı")
    # Anlık kullanıcıyı ve giriş yapıldığını sıfırlama
    global anlikKullanici, girisYapildi   # Metod dışındaki değişkenlere erişmek için kullandım
    girisYapildi = False
    anlikKullanici = ""

# En son gerçekleşen depremleri gösteren fonksiyon
def son_deprem():
    limit = int(input("Depremlerin sayısını girin: "))
    # API'den veri çekme
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live?limit={}".format(limit)
    response = requests.get(url)
    data = response.json()

    # Eğer API'den veri alındıysa depremleri gösterme
    if data["status"]:
        for earthquake in data["result"]:
            title = earthquake["title"]
            date = earthquake["date"]
            mag = earthquake["mag"]
            depth = earthquake["depth"]
            closest_cities = [city["name"] for city in earthquake["location_properties"]["closestCities"][:3]]
            airports = [airport["name"] for airport in earthquake["location_properties"]["airports"][:3]]

            print("*************")
            print("Yer:", title)
            print("Tarih:", date)
            print("Büyüklük:", mag)
            print("Derinlik:", depth, "km")
            print("En Yakın 3 Şehir:", ", ".join(closest_cities))
            print("En Yakın 3 Havalimanı:", ", ".join(airports))
    else:
        print("API'den veri alınamadı.")

# Şehire göre depremleri gösteren fonksiyon
def sehir_deprem():
    # API'den veri çekme
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live?limit=100"
    response = requests.get(url)
    data = response.json()

    # Eğer API'den veri alındıysa depremleri gösterme
    if data["status"]:
        print("\nDikkat! Doğru verinin gösterilmesi için küçük ve İngilizce harf kullanılması gerekiyor!")
        city = input("Şehir adını girin: ")
        count = 0
        for earthquake in data["result"]:
            title = earthquake["title"]
            if city.lower() in title.lower():
                date = earthquake["date"]
                mag = earthquake["mag"]
                depth = earthquake["depth"]
                closest_cities = [city["name"] for city in earthquake["location_properties"]["closestCities"][:3]]
                airports = [airport["name"] for airport in earthquake["location_properties"]["airports"][:3]]

                print("*************")
                print("Yer:", title)
                print("Tarih:", date)
                print("Büyüklük:", mag)
                print("Derinlik:", depth, "km")
                print("En Yakın 3 Şehir:", ", ".join(closest_cities))
                print("En Yakın 3 Havalimanı:", ", ".join(airports))

                count += 1
                if count == 5:
                    break

        if count == 0:
            print("\nBelirtilen şehre ait deprem bulunamadı.")
    else:
        print("API'den veri alınamadı.")

# Büyüklüklere göre depremleri gösteren fonksiyon
def buyukluk_sirala():
    # API'den veri çekme
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live?limit=100"
    response = requests.get(url)
    data = response.json()

    # Eğer API'den veri alındıysa depremleri gösterme
    if data["status"]:
        magnitude = float(input("Büyüklük değerini girin: "))

        count = 0
        for earthquake in data["result"]:
            mag = earthquake["mag"]
            if mag >= magnitude:
                title = earthquake["title"]
                date = earthquake["date"]
                depth = earthquake["depth"]
                closest_cities = [city["name"] for city in earthquake["location_properties"]["closestCities"][:3]]
                airports = [airport["name"] for airport in earthquake["location_properties"]["airports"][:3]]

                print("*************")
                print("Yer:", title)
                print("Tarih:", date)
                print("Büyüklük:", mag)
                print("Derinlik:", depth, "km")
                print("En Yakın 3 Şehir:", ", ".join(closest_cities))
                print("En Yakın 3 Havalimanı:", ", ".join(airports))

                count += 1
                if count == 5:
                    break

        if count == 0:
            print("Belirtilen büyüklük değerine ait deprem bulunamadı.")
    else:
        print("API'den veri alınamadı.")

while True:
    while not girisYapildi:
        print(menuTuple)
        secim = int(input("Lütfen bir işlem seçiniz: "))
        if secim == 1:
            kayit()
        elif secim == 2:
            giris()
        elif secim == 3:
            sifremi_unuttum()
        elif secim == 4:
            admin_giris()
        elif secim == 5:
            print("Çıkış Yapıldı")
            dongu_bitir = True
            break
        else:
            print("Hatalı seçim yaptınız!")

    if dongu_bitir:
        break

    while girisYapildi:
        print("\nHoşgeldin {}!\nSon depremler ile ilgili bilgileri görebilirsiniz!".format(anlikKullanici))
        print(depremTuple)
        secim = int(input("Lütfen bir işlem seçiniz: "))
        if secim == 1:
            son_deprem()
        elif secim == 2:
            sehir_deprem()
        elif secim == 3:
            buyukluk_sirala()
        elif secim == 4:
            cikis()
        else:
            print("Hatalı seçim yaptınız!")