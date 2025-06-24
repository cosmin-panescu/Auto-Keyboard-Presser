import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import keyboard
import pyautogui
from datetime import datetime
from pynput import mouse as pynput_mouse  # detectare automata mouse

class KeyRecorderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎹 Advanced Key & Mouse Recorder v4.0")
        self.root.geometry("950x900")
        self.root.configure(bg='#2c3e50')
        
        pyautogui.PAUSE = 0.01
        pyautogui.FAILSAFE = False
        
        # Variabile pt. recorder
        self.recorded_actions = []
        self.recording = False
        self.last_time = None
        self.active_modifiers = set()
        self.stop_requested = False
        self.countdown_active = False
        
        # Variabile pt. mouse
        self.record_mouse = tk.BooleanVar(value=False)
        self.mouse_listener = None 
        self.last_mouse_pos = None
        self.mouse_move_threshold = 15  # numar minim pixeli pentru miscare mouse
        
        # lista completa taste
        self.key_mappings = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j',
            'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't',
            'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
            'left shift': 'shift', 'right shift': 'shift', 'shift': 'shift',
            'left ctrl': 'ctrl', 'right ctrl': 'ctrl', 'ctrl': 'ctrl',
            'left alt': 'alt', 'right alt': 'alt', 'alt': 'alt',
            'left windows': 'win', 'right windows': 'win', 'win': 'win',
            'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4', 'f5': 'f5', 'f6': 'f6',
            'f7': 'f7', 'f8': 'f8', 'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
            'esc': 'escape', 'escape': 'escape', 'tab': 'tab', 'caps lock': 'capslock',
            'enter': 'enter', 'return': 'enter', 'space': 'space', 'spacebar': 'space',
            'backspace': 'backspace', 'delete': 'delete', 'insert': 'insert', 'home': 'home', 'end': 'end',
            'page up': 'pageup', 'page down': 'pagedown',
            'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
            'num lock': 'numlock', 'num 0': 'num0', 'num 1': 'num1', 'num 2': 'num2', 'num 3': 'num3',
            'num 4': 'num4', 'num 5': 'num5', 'num 6': 'num6', 'num 7': 'num7', 'num 8': 'num8', 'num 9': 'num9',
            'num +': 'num+', 'num -': 'num-', 'num *': 'num*', 'num /': 'num/', 'num enter': 'numenter', 'num .': 'num.',
            '`': '`', '-': '-', '=': '=', '[': '[', ']': ']', '\\': '\\', ';': ';', "'": "'", ',': ',', '.': '.', '/': '/',
            'print screen': 'printscreen', 'scroll lock': 'scrolllock', 'pause': 'pause', 'apps': 'apps'
        }
        
        self.modifier_keys = {'shift', 'ctrl', 'alt', 'win'}
        
        self.setup_gui()
        self.setup_keyboard_hooks()
    
    def calculate_distance(self, pos1, pos2):
        # distanta intre doua pozitii
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    def on_pynput_move(self, x, y):
        # miscare mouse
        if not self.recording or not self.record_mouse.get():
            return
            
        current_pos = (x, y)
        current_time = time.time()
        
        if self.last_mouse_pos:
            distance = self.calculate_distance(current_pos, self.last_mouse_pos)
            
            if distance >= self.mouse_move_threshold:
                pause = current_time - self.last_time if self.last_time else 0
                self.record_mouse_action('mouse_move', x, y, {
                    'from_position': self.last_mouse_pos,
                    'to_position': current_pos
                }, pause, current_time)
                
                self.root.after(0, lambda: self.log(f"🖱️ ✨ Miscare automata: {self.last_mouse_pos} → {current_pos}"))
                self.last_mouse_pos = current_pos
                self.last_time = current_time
    
    def on_pynput_click(self, x, y, button, pressed):
        # mouse click
        if not self.recording or not self.record_mouse.get() or not pressed:
            return
            
        current_time = time.time()
        current_pos = (x, y)

        # convertire buton mouse 
        if button == pynput_mouse.Button.left:
            button_name = 'left'
        elif button == pynput_mouse.Button.right:
            button_name = 'right'
        elif button == pynput_mouse.Button.middle:
            button_name = 'middle'
        else:
            button_name = 'left'
        
        pause = current_time - self.last_time if self.last_time else 0
        self.record_mouse_action('mouse_click', x, y, {
            'button': button_name,
            'position': current_pos
        }, pause, current_time)
        
        self.root.after(0, lambda b=button_name: self.log(f"🖱️ ✨ Click {b} automat: {current_pos}"))
        self.last_time = current_time
    
    def on_pynput_scroll(self, x, y, dx, dy):
        # scroll mouse
        if not self.recording or not self.record_mouse.get():
            return
            
        current_time = time.time()
        current_pos = (x, y)
        
        direction = 'up' if dy > 0 else 'down'
        
        pause = current_time - self.last_time if self.last_time else 0
        self.record_mouse_action('mouse_scroll', x, y, {
            'direction': direction,
            'delta': dy,
            'position': current_pos
        }, pause, current_time)
        
        self.root.after(0, lambda d=direction: self.log(f"🖱️ ✨ Scroll {d} automat: {current_pos}"))
        self.last_time = current_time
    
    def start_mouse_monitoring(self):
        # monitorizare mouse
        if not self.record_mouse.get():
            return
        
        try:
            # oprire listener daca exista
            if self.mouse_listener:
                self.mouse_listener.stop()
            
            # creare listener pynput nou
            self.mouse_listener = pynput_mouse.Listener(
                on_move=self.on_pynput_move,
                on_click=self.on_pynput_click,
                on_scroll=self.on_pynput_scroll
            )
            
            # pornire listener
            self.mouse_listener.start()
            self.last_mouse_pos = pyautogui.position()
            
            self.log("🖱️ ✨ Detectare automata mouse activata")
            self.log("🎯 Se detecteaza automat: miscare, click-uri, scroll")
            
        except Exception as e:
            self.log(f"❌ Eroare la pornirea detectarii mouse: {e}")
    
    def stop_mouse_monitoring(self):
        try:
            if self.mouse_listener:
                self.mouse_listener.stop()
                self.mouse_listener = None
            self.log("🖱️ Detectare mouse oprita")
        except Exception as e:
            self.log(f"⚠️ Eroare la oprirea mouseului: {e}")
    
    def record_mouse_action(self, action_type, x, y, data, pause, timestamp):
        action = {
            'type': 'mouse',
            'action': action_type,
            'x': int(x),
            'y': int(y),
            'data': data,
            'pause_before': pause,
            'timestamp': timestamp
        }
        self.recorded_actions.append(action)
        self.update_status(f"Inregistrez... ({len(self.recorded_actions)} actiuni)", '#e74c3c')
    
    def replay_mouse_action(self, action):
        try:
            action_type = action['action']
            x, y = int(action['x']), int(action['y'])
            data = action['data']
            
            if action_type == 'mouse_move':
                pyautogui.moveTo(x, y, duration=0.1)
                self.root.after(0, lambda: self.log(f"🖱️ ✓ Miscare: ({x}, {y})"))
                
            elif action_type == 'mouse_click':
                button = data['button']
                pyautogui.moveTo(x, y, duration=0.05)
                time.sleep(0.02)
                pyautogui.click(x, y, button=button)
                self.root.after(0, lambda b=button: self.log(f"🖱️ ✓ Click {b}: ({x}, {y})"))
                
            elif action_type == 'mouse_scroll':
                direction = data['direction']
                delta = data['delta']
                # scroll
                pyautogui.moveTo(x, y, duration=0.05)
                time.sleep(0.02)
                scroll_amount = int(delta * 3)  # amplificare scroll
                pyautogui.scroll(scroll_amount)
                self.root.after(0, lambda d=direction: self.log(f"🖱️ ✓ Scroll {d}: ({x}, {y})"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log(f"❌ Eroare mouse: {e}"))

    def is_stop_combination_pressed(self):
        try:
            ctrl_pressed = (keyboard.is_pressed('ctrl') or 
                           keyboard.is_pressed('left ctrl') or 
                           keyboard.is_pressed('right ctrl'))
            shift_pressed = (keyboard.is_pressed('shift') or 
                            keyboard.is_pressed('left shift') or 
                            keyboard.is_pressed('right shift'))
            x_pressed = keyboard.is_pressed('x')
            return ctrl_pressed and shift_pressed and x_pressed
        except:
            return False
    
    def normalize_key(self, key):
        key_lower = str(key).lower().strip()
        if key_lower in self.key_mappings:
            return self.key_mappings[key_lower]
        return key_lower
    
    def is_modifier(self, key):
        normalized = self.normalize_key(key)
        return normalized in self.modifier_keys
    
    def setup_gui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎹 Advanced Key & Mouse Recorder", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#34495e')
        title_label.pack(pady=20)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#2c3e50')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="Status: Pregatit", 
                                    font=('Arial', 12), fg='#1abc9c', bg='#2c3e50')
        self.status_label.pack(side='left')
        
        self.actions_count_label = tk.Label(status_frame, text="Acțiuni: 0", 
                                           font=('Arial', 12), fg='#f39c12', bg='#2c3e50')
        self.actions_count_label.pack(side='right')
        
        # Countdown label
        self.countdown_label = tk.Label(self.root, text="", 
                                       font=('Arial', 24, 'bold'), fg='#e74c3c', bg='#2c3e50')
        self.countdown_label.pack(pady=10)
        
        # Butoane control
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Buton inregistrare
        self.record_button = tk.Button(control_frame, text="🔴 Incepe Inregistrarea", 
                                      command=self.start_recording_with_countdown,
                                      bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                      height=2, relief='raised', cursor='hand2')
        self.record_button.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        # Buton STOP
        self.stop_button = tk.Button(control_frame, text="⏹️ Opreste", 
                                    command=self.stop_recording,
                                    bg='#7f8c8d', fg='white', font=('Arial', 12, 'bold'),
                                    height=2, relief='raised', cursor='hand2', state='disabled')
        self.stop_button.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        # Buton PLAY
        self.play_button = tk.Button(control_frame, text="▶️ Reda Secventa", 
                                    command=self.start_playback_with_countdown,
                                    bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                    height=2, relief='raised', cursor='hand2')
        self.play_button.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        # Buton CURATARE Inregistrare
        self.clear_button = tk.Button(control_frame, text="🗑️ Sterge", 
                                     command=self.clear_recording,
                                     bg='#8e44ad', fg='white', font=('Arial', 12, 'bold'),
                                     height=2, relief='raised', cursor='hand2')
        self.clear_button.pack(side='left', fill='x', expand=True)
        
        # Setari
        settings_frame = tk.LabelFrame(self.root, text="⚙️ Setari", 
                                      font=('Arial', 11, 'bold'), fg='white', bg='#2c3e50')
        settings_frame.pack(fill='x', padx=10, pady=5)
        
        # Checkbox Inregistrare Mouse
        mouse_frame = tk.Frame(settings_frame, bg='#2c3e50')
        mouse_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        self.mouse_checkbox = tk.Checkbutton(mouse_frame, 
                                            text="🖱️ Inregistreaza mouse-ul (detectare automata: clicuri, miscare, scroll)",
                                            variable=self.record_mouse,
                                            font=('Arial', 10, 'bold'),
                                            fg='#3498db', bg='#2c3e50',
                                            selectcolor='#34495e',
                                            activebackground='#2c3e50',
                                            activeforeground='#3498db')
        self.mouse_checkbox.pack(side='left')
        
        # Numar repetari frame
        rep_frame = tk.Frame(settings_frame, bg='#2c3e50')
        rep_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(rep_frame, text="Repetari:", font=('Arial', 10), 
                fg='white', bg='#2c3e50').pack(side='left')
        
        self.repetitions_var = tk.StringVar(value="1")
        self.repetitions_entry = tk.Entry(rep_frame, textvariable=self.repetitions_var, 
                                         width=10, font=('Arial', 10))
        self.repetitions_entry.pack(side='left', padx=(10, 5))
        
        tk.Label(rep_frame, text="(gol = infinit)", font=('Arial', 9), 
                fg='#95a5a6', bg='#2c3e50').pack(side='left')
        
        # Instructiuni
        instructions_frame = tk.LabelFrame(self.root, text="📋 Instructiuni", 
                                          font=('Arial', 11, 'bold'), fg='white', bg='#2c3e50')
        instructions_frame.pack(fill='x', padx=10, pady=5)
        
        instructions = """
• Inregistreaza orice tasta Windows
• Suport pentru combinatii simultane (ex: SHIFT + F12, CTRL + ALT + DELETE)
• MOUSE: Bifeaza checkbox-ul pentru detectarea mouseului (pozitie + click-uri)
• CTRL+SHIFT+X pentru oprirea inregistrarii/redarii
        """
        
        tk.Label(instructions_frame, text=instructions.strip(), 
                font=('Arial', 9), fg='#bdc3c7', bg='#2c3e50', 
                justify='left').pack(padx=10, pady=5, anchor='w')
        
        # Log-uri
        log_frame = tk.LabelFrame(self.root, text="📝 Istoric actiuni", 
                                 font=('Arial', 11, 'bold'), fg='white', bg='#2c3e50')
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, 
                                                 font=('Courier', 9), 
                                                 bg='#34495e', fg='#ecf0f1',
                                                 insertbackground='white',
                                                 state='disabled',
                                                 wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_keyboard_hooks(self):
        try:
            keyboard.on_press(self.on_key_press)
            keyboard.on_release(self.on_key_release)
        except Exception as e:
            self.log(f"❌ Eroare la configurarea hook-urilor: {e}")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, full_message)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
    
    def update_status(self, status, color='#1abc9c'):
        self.status_label.config(text=f"Status: {status}", fg=color)
        self.actions_count_label.config(text=f"Acțiuni: {len(self.recorded_actions)}")
    
    def countdown_display(self, seconds, message, callback=None):
        self.countdown_active = True
        self.disable_all_buttons()
        
        def countdown_thread():
            for i in range(seconds, 0, -1):
                self.root.after(0, lambda i=i: self.countdown_label.config(text=f"{message}\n{i}"))
                self.root.after(0, lambda i=i: self.log(f"⏰ {message} în {i} secunde..."))
                time.sleep(1)
            
            self.root.after(0, lambda: self.countdown_label.config(text=""))
            self.root.after(0, lambda: self.log(f"🚀 {message} - START!"))
            self.countdown_active = False
            
            if callback:
                self.root.after(0, callback)
            else:
                self.root.after(0, self.enable_appropriate_buttons)
        
        threading.Thread(target=countdown_thread, daemon=True).start()
    
    def disable_all_buttons(self):
        self.record_button.config(state='disabled', bg='#7f8c8d')
        self.stop_button.config(state='disabled', bg='#7f8c8d')
        self.play_button.config(state='disabled', bg='#7f8c8d')
        self.clear_button.config(state='disabled', bg='#7f8c8d')
    
    def enable_appropriate_buttons(self):
        if not self.recording:
            self.record_button.config(state='normal', bg='#e74c3c')
            self.clear_button.config(state='normal', bg='#8e44ad')
            if self.recorded_actions:
                self.play_button.config(state='normal', bg='#27ae60')
        else:
            self.stop_button.config(state='normal', bg='#e74c3c')
    
    def start_recording_with_countdown(self):
        if self.countdown_active:
            return
        
        self.log("📝 Pregatesc inregistrarea...")
        if self.record_mouse.get():
            self.log("🖱️ Detectare automata mouse activata!")
        self.update_status("Se pregateste...", '#f39c12')
        self.countdown_display(5, "Pozitioneaza-te pentru inregistrare", self.start_recording)
    
    def start_playback_with_countdown(self):
        if self.countdown_active:
            return
            
        if not self.recorded_actions:
            messagebox.showwarning("Avertisment", "Nu exista actiuni inregistrate!")
            return
        
        try:
            reps_text = self.repetitions_var.get().strip()
            repetitions = float('inf') if not reps_text else int(reps_text)
        except ValueError:
            messagebox.showerror("Eroare", "Numarul de repetari trebuie sa fie un numar intreg!")
            return
        
        self.log("▶️ Pregatesc redarea...")
        self.update_status("Se pregatește redarea...", '#f39c12')
        self.countdown_display(5, "Pozitioneaza-te pentru redare", 
                              lambda: self.start_playback(repetitions))
    
    def on_key_press(self, event):
        if not self.recording or self.countdown_active:
            return
            
        current_time = time.time()
        pause = current_time - self.last_time if self.last_time else 0
        key_name = self.normalize_key(event.name)
        
        # CTRL+SHIFT+X pentru oprire
        if (key_name == 'x' and 'ctrl' in self.active_modifiers and 'shift' in self.active_modifiers):
            self.log("🛑 CTRL+SHIFT+X detectat - opresc inregistrarea...")
            self.stop_requested = True
            return
        
        if self.is_modifier(key_name):
            self.active_modifiers.add(key_name)
            self.log(f"+ Modificator: {key_name}")
            return
        else:
            if self.active_modifiers:
                modifiers = sorted(list(self.active_modifiers))
                combination = '+'.join(modifiers + [key_name])
                self.record_action(combination, pause, current_time, is_combination=True)
                self.log(f"🔗 Combinatie: {combination}")
                self.active_modifiers.clear()
            else:
                self.record_action(key_name, pause, current_time, is_combination=False)
                self.log(f"⌨️ Tasta: {key_name}")
            
            self.last_time = current_time
            self.update_status(f"Inregistrez... ({len(self.recorded_actions)} actiuni)", '#e74c3c')
    
    def on_key_release(self, event):
        if not self.recording or self.countdown_active:
            return
            
        key_name = self.normalize_key(event.name)
        
        if self.is_modifier(key_name):
            self.active_modifiers.discard(key_name)
    
    def record_action(self, key_combination, pause, timestamp, is_combination=False):
        action = {
            'type': 'keyboard',
            'keys': key_combination,
            'pause_before': pause,
            'timestamp': timestamp,
            'is_combination': is_combination
        }
        self.recorded_actions.append(action)
    
    def start_recording(self):
        self.recorded_actions = []
        self.recording = True
        self.stop_requested = False
        self.last_time = time.time()
        self.active_modifiers = set()
        
        # Pornire inregistrare mouse daca este activata optiunea
        if self.record_mouse.get():
            self.start_mouse_monitoring()
        
        self.record_button.config(state='disabled', bg='#7f8c8d')
        self.stop_button.config(state='normal', bg='#e74c3c')
        self.play_button.config(state='disabled', bg='#7f8c8d')
        self.clear_button.config(state='disabled', bg='#7f8c8d')
        
        self.update_status("Inregistrez...", '#e74c3c')
        self.log("🔴 INREGISTRARE PORNITA")
        self.log("💡 Apasa CTRL+SHIFT+X pentru a opri")
        
        threading.Thread(target=self.monitor_stop, daemon=True).start()
    
    def monitor_stop(self):
        while self.recording and not self.stop_requested:
            time.sleep(0.1)
        if self.recording:
            self.root.after(0, self.stop_recording)
    
    def stop_recording(self):
        self.recording = False
        self.active_modifiers.clear()
        
        # Opreste detectare mouse
        if self.record_mouse.get():
            self.stop_mouse_monitoring()
        
        self.record_button.config(state='normal', bg='#e74c3c')
        self.stop_button.config(state='disabled', bg='#7f8c8d')
        self.play_button.config(state='normal', bg='#27ae60')
        self.clear_button.config(state='normal', bg='#8e44ad')
        
        self.update_status("Pregatit", '#1abc9c')
        self.log(f"⏹️ INREGISTRARE OPRITA - {len(self.recorded_actions)} actiuni")
    
    def start_playback(self, repetitions):
        self.play_button.config(state='disabled', bg='#7f8c8d')
        self.record_button.config(state='disabled', bg='#7f8c8d')
        self.clear_button.config(state='disabled', bg='#7f8c8d')
        
        threading.Thread(target=self.replay_actions, args=(repetitions,), daemon=True).start()
    
    def replay_actions(self, repetitions):
        try:
            self.root.after(0, lambda: self.update_status("Se reda...", '#f39c12'))
            self.root.after(0, lambda: self.log(f"▶️ INCEPE REDAREA ({repetitions if repetitions != float('inf') else '∞'} repetari)"))
            
            cycle = 0
            while cycle < repetitions:
                if self.is_stop_combination_pressed():
                    self.root.after(0, lambda: self.log("⏹️ Oprit de utilizator"))
                    break
                
                self.root.after(0, lambda c=cycle+1: self.log(f"=== Repetarea {c} ==="))
                
                for action in self.recorded_actions:
                    if self.is_stop_combination_pressed():
                        self.root.after(0, lambda: self.log("⏹️ Secventa oprita"))
                        return
                    
                    if action['pause_before'] > 0.1:
                        pause_time = action['pause_before']
                        steps = max(1, int(pause_time / 0.1))
                        step_time = pause_time / steps
                        
                        for _ in range(steps):
                            if self.is_stop_combination_pressed():
                                return
                            time.sleep(step_time)
                    else:
                        time.sleep(action['pause_before'])
                    
                    try:
                        if action.get('type') == 'mouse':
                            self.replay_mouse_action(action)
                        else:
                            keys = action['keys']
                            if action.get('is_combination') and '+' in keys:
                                key_parts = [k.strip() for k in keys.split('+')]
                                pyautogui.hotkey(*key_parts)
                                self.root.after(0, lambda k=keys: self.log(f"🔗 Combinatie: {k}"))
                            else:
                                pyautogui.press(keys)
                                self.root.after(0, lambda k=keys: self.log(f"✓ Tasta: {k}"))
                        
                    except Exception as e:
                        action_desc = action.get('keys', 'mouse action')
                        self.root.after(0, lambda k=action_desc, e=e: self.log(f"❌ Eroare la {k}: {e}"))
                    
                    time.sleep(0.02)
                
                cycle += 1
                if cycle < repetitions:
                    time.sleep(0.2)
            
            self.root.after(0, lambda: self.log(f"✅ Redare completa"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"❌ Eroare in timpul redarii: {e}"))
        finally:
            self.root.after(0, self.playback_finished)
    
    def playback_finished(self):
        self.play_button.config(state='normal', bg='#27ae60')
        self.record_button.config(state='normal', bg='#e74c3c')
        self.clear_button.config(state='normal', bg='#8e44ad')
        self.update_status("Pregatit", '#1abc9c')
    
    def clear_recording(self):
        if self.countdown_active:
            return
            
        if messagebox.askyesno("Confirmare", "Sigur vrei sa stergi inregistrarea?"):
            self.recorded_actions = []
            
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state='disabled')
            
            self.update_status("Pregatit", '#1abc9c')
            self.log("🗑️ Inregistrare stearsa")

def main():
    root = tk.Tk()
    app = KeyRecorderGUI(root)
    
    def on_closing():
        if messagebox.askokcancel("Iesire", "Sigur vrei sa inchizi aplicatia?"):
            keyboard.unhook_all()
            if hasattr(app, 'mouse_listener') and app.mouse_listener:
                app.mouse_listener.stop()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
