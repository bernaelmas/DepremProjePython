menu = """ ***Sisteme Hoşgeldiniz***\n1-Sisteme Üye Ol\n2-Sisteme Giriş Yap\n3-Şifremi Unuttum\n4-Sistemden Çık"""
print(menu)
secim = int(input("Lütfen bir işlem seçiniz:"))
if secim == 1:
    print("***Sisteme Üye Ol***")
    ad = input("Adınız:")
    soyad = input("Soyadınız:")
    