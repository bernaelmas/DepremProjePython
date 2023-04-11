adminKullanici = ["bernaelms@gmail.com"]
adminSifre = ["789456123"]
kullaniciListe = []
parolaListe = []
menu = """***Sisteme Hoşgeldiniz***
1-Sisteme Üye Ol\n2-Sisteme Giriş Yap\n3-Şifremi Unuttum\n4-Sistemden Çık\n5-Admin Girişi"""

while True:
    print(menu)
    secim = int(input("Lütfen bir işlem seçiniz:"))
    if secim == 1:
        print("***Sisteme Üye Ol***")
        mail = input("E-mail adresinizi giriniz:")
        sifre = input("Şifrenizi giriniz:")

        if mail not in kullaniciListe:
            if mail and sifre != "":
                kullaniciListe.append(mail)
                parolaListe.append(sifre)
                print("Başarıyla Üye Olundu.")
            else:
                print("Mail veya Şifre Boş!")
        else:
            print("Kullanıcı Daha Önceden Üye Oldu!")
    elif secim == 2:
        print("***Sisteme Giriş Yap***")
        mail = input("E-mail adresinizi giriniz:")
        sifre = input("Şifrenizi giriniz:")

        if mail in kullaniciListe:
            indexNum = kullaniciListe.index(mail)
            if sifre == parolaListe[indexNum]:
                print("Başarıyla Giriş Yapıldı.")
            else:
                print("Hatalı Şifre Girdiniz!")
        else:
            print("Kullanıcı Bulunamadı.")
    elif secim == 3:
        print("***Şifremi Unuttum***")
        mail = input("E-mail adresinizi giriniz:")

        if mail in kullaniciListe:
            indexNum = kullaniciListe.index(mail)
            yenisifre = input("Yeni şifrenizi giriniz:")

            if yenisifre != "":
                parolaListe[indexNum] = yenisifre
                print("Şifre Başarıyla Değiştirildi.")
        else:
            print("Kullanıcı Bulunamadı.")
    elif secim == 4:
        print("Çıkış Yapıldı")
        break
    elif secim == 5:
        print("***Admin Girişi***")
        kullaniciAdi = input("Kullanıcı Adınızı Giriniz:")
        sifre = input("Şifrenizi Giriniz:")

        if kullaniciAdi == adminKullanici[0] and sifre == adminSifre[0]:
            print("Admin Girişi Başarılı.")
        else:
            print("Yanlış Kullanıcı Adı veya Şifre Girdiniz!")
    else:
        print("Hatalı Seçim Yaptınız!")