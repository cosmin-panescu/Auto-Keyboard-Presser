![License](https://img.shields.io/badge/License-MIT-yellow)

# 🎹 Auto Keyboard Presser

**Aplicație pentru înregistrarea și redarea automată a acțiunilor de tastatură și mouse**

## 🚀 Instalare Ultra-Simplă

### Pentru Utilizatori Normali (Recomandat)
1. **Mergi la Releases**
2. **Descarcă** `KeyMouseRecorder.exe`
3. **Dublu-click** pe executabil
4. **Gata!** Nu trebuie să instalezi nimic altceva!

### Pentru Developeri
git clone https://github.com/cosmin-panescu/Auto-Keyboard-Presser.git
cd Auto-Keyboard-Presser
pip install -r requirements.txt
python key_recorder_gui.py

## ✨ Caracteristici Principale

### 🎹 Înregistrare Completă Tastatură
- **Toate tastele Windows:** A-Z, 0-9, F1-F12, NumPad, săgeți, Insert, Delete, etc.
- **Combinații complexe:** CTRL+C, SHIFT+F12, ALT+TAB, CTRL+ALT+DELETE
- **Taste speciale:** Print Screen, Scroll Lock, Pause, Apps/Menu
- **Modificatori:** Support complet pentru Left/Right Shift, Ctrl, Alt, Win

### ⚡ Funcționalități Avansate
- **Repetări flexibile:** De la 1 până la infinit
- **Timing precis:** Pauze exacte între acțiuni pentru reproducere perfectă
- **Oprire instantanee:** CTRL+SHIFT+X oprește orice operațiune
- **Countdown vizual:** 5 secunde pentru pregătire înainte de înregistrare/redare
- **Log detaliat:** Istoric complet cu timestamp pentru toate acțiunile

## 📖 Ghid de Utilizare

### Pașii de Bază
1. **Lansează aplicația** - dublu-click pe executabil
2. **Configurează opțiunile:**
   - Setează numărul de repetări (gol = infinit)
3. **Începe înregistrarea** - apasă "🔴 Începe Înregistrarea"
4. **Așteaptă countdown-ul** de 5 secunde pentru poziționare
5. **Execută acțiunile** pe care vrei să le automatizezi
6. **Oprește înregistrarea** cu CTRL+SHIFT+X
7. **Redă secvența** cu "▶️ Redă Secvența"

### Interfața Utilizator

#### Butoane Principale
- **🔴 Începe Înregistrarea** - Pornește înregistrarea cu countdown
- **⏹️ Oprește** - Oprește înregistrarea curentă
- **▶️ Redă Secvența** - Redă acțiunile înregistrate
- **🗑️ Șterge** - Șterge înregistrarea curentă

#### Zona de Status
- **Status curent:** Afișează starea aplicației (Pregătit/Înregistrez/Se redă)
- **Contor acțiuni:** Numărul total de acțiuni înregistrate
- **Jurnal live:** Log detaliat cu timestamp pentru toate evenimentele

## 🎯 Cazuri de Utilizare Perfecte

- 🏢 Automatizarea Sarcinilor de Birou
- 🎮 Gaming și Macros
- 🧪 Testing și QA
- 📹 Demonstrații și Tutoriale

## ⚙️ Specificații Tehnice

### Cerințe de Sistem
- **OS:** Windows 7/8/10/11 (32-bit sau 64-bit)
- **RAM:** Minimum 50MB disponibil
- **Spațiu disk:** 15MB pentru executabil
- **Permisiuni:** Acces la tastatură și mouse (nu necesită admin)

### Performanță
- **CPU Usage:** <1% în idle, 2-3% în timpul înregistrării
- **Precizie timing:** ±1ms pentru secvențe critice
- **Latency:** <10ms pentru detectarea acțiunilor
- **Capacitate:** Suport pentru secvențe de mii de acțiuni

### Tehnologii Utilizate
- **Python 3.7+** - Core application
- **Tkinter** - GUI framework
- **PyAutoGUI** - Cross-platform automation
- **Keyboard** - Global keyboard hooks
- **PyInstaller** - Executable packaging

## 🛠️ Pentru Developeri

### Setup Environment
-> Clone repository
-> git clone https://github.com/cosmin-panescu/Auto-Keyboard-Presser.git
-> cd Auto-Keyboard-Presser

Install dependencies
-> pip install -r requirements.txt

### Dependențe
pyautogui==0.9.54 # GUI automation
keyboard==0.13.5 # Global keyboard hooks
pyinstaller>=6.10.0 # Executable building

### Build Executabil
Metoda manuala
pyinstaller --onefile --windowed --name=KeyMouseRecorder key_recorder_gui.py

## 🔧 Troubleshooting

### Probleme Comune

**Q: CTRL+SHIFT+X nu oprește înregistrarea**
A: Verifică că nu ai alte aplicații care interceptează aceste combinații de taste (ex: software gaming, macro tools).

**Q: Executabilul nu pornește**
A: Verifică Windows Defender/antivirus - uneori blochează executabile necunoscute. Adaugă o excepție pentru aplicație.

**Q: Acțiunile nu se redau precis**
A: Pentru aplicații care necesită focus specific, asigură-te că fereastra țintă este activă înainte de redare.

**Q: Aplicația consumă prea multă memorie**
A: Pentru secvențe foarte lungi (>1000 acțiuni), folosește opțiunea "Șterge" periodic pentru a elibera memoria.

## 🤝 Contribuții

Contribuțiile sunt binevenite! Pentru a contribui:

1. **Fork** repository-ul
2. **Creează** o branch pentru feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** modificările (`git commit -m 'Add some AmazingFeature'`)
4. **Push** branch-ul (`git push origin feature/AmazingFeature`)
5. **Deschide** un Pull Request

## 📜 Licență

Acest proiect este licențiat sub **MIT License** - vezi fișierul [LICENSE](LICENSE) pentru detalii.

### Ce înseamnă MIT License?

**✅ Poți:**
- Să folosești codul comercial sau personal
- Să modifici și să distribui codul
- Să incluzi codul în proiecte private
- Să vinzi software bazat pe acest cod

**❗ Trebuie să:**
- Incluzi licența originală în orice distribuție
- Incluzi copyright notice-ul

**🚫 Nu sunt responsabil pentru:**
- Daune cauzate de utilizarea software-ului
- Bugs sau probleme de funcționare
- Suport tehnic obligatoriu
