# IETT_API
Bu repository, IETT WebServisleri kullanarak python dili üzerinden yazmış olduğum scriptleri içermektedir.  
WebServisleri ve veriler [IBB Açık Veri Portalı](https://data.ibb.gov.tr/) adresinden alınmıştır.  
Kullanım hakları ve lisansa yönelik detaylı bilgi için lisans sekmesini ziyaret edebilirsiniz.  


### Kullanım (TR)
**Linux:**  
1. Zip'i unpack'leyin, ana klasöre geçin  
2. Virtual environment'ı oluşturun  
```
python3 -m venv .venv
```
3. Virtual environment'ı aktifleştirin  
```
source .venv/bin/activate
```
4. Gerekli dependency'leri kurun  
```
pip install -r utils/requirements.txt
```
5. Çalıştırmak istediğiniz dosyayı çalıştırın (Örnek)  
```
python3 akaryakit_toplam_litre.py
```
  
**Windows:**  
1. Zip'i unpack'leyin, ana klasöre geçin  
2. Virtual environment'ı oluşturun  
```
py -m venv .venv
```
3. Virtual environment'ı aktifleştirin  
```
.venv\Scripts\activate
```
4. Gerekli dependency'leri kurun  
```
pip install -r utils\requirements.txt
```
5. Çalıştırmak istediğiniz dosyayı çalıştırın (Örnek)  
```
py akaryakit_toplam_litre.py
```


### Usage (ENG)
**Linux:**  
1. Unpack the zip file, change to main directory  
2. Create a virtual environment  
```
python3 -m venv .venv
```
3. Activate virtual environment  
```
source .venv/bin/activate
```
4. Install required dependencies  
```
pip install -r utils/requirements.txt
```
5. Run the script you would like to execute. (Example below)  
```
python3 akaryakit_toplam_litre.py
```
  
**Windows:**  
1. Unpack the zip file, change to main directory  
2. Create a virtual environment  
```
py -m venv .venv
```
3. Activate virtual environment  
```
.venv\Scripts\activate
```
4. Install required dependencies  
```
pip install -r utils\requirements.txt
```
5. Run the script you would like to execute. (Example below)  
```
py akaryakit_toplam_litre.py
```
