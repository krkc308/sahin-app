import datetime
import random
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle

kivy.require('2.0.0')

class TechBackgroundLayout(BoxLayout):
    """Arka plana siber güvenlik / HUD tarzı teknik desen (grid) çizen özel yerleşim"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # 1. Derin koyu uzay/terminal arkaplanı
            Color(0.06, 0.07, 0.1, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # 2. Şık teknolojik kafes (grid) deseni çizgileri
            Color(0.12, 0.3, 0.45, 0.15)  # Çok hafif şeffaf mavi/gri ton
            step = 40  
            
            # Dikey çizgiler
            for x in range(int(self.x), int(self.x + self.width), step):
                Line(points=[x, self.y, x, self.y + self.height], width=1)
            
            # Yatay çizgiler
            for y in range(int(self.y), int(self.y + self.height), step):
                Line(points=[self.x, y, self.x + self.width, y], width=1)

class ChatBubble(BoxLayout):
    def __init__(self, text, is_user=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [22, 18, 22, 18]  # Büyük ve ferah baloncuklar
        self.spacing = 8
        
        if is_user:
            bg_color = (0.12, 0.35, 0.6, 1)  # Mavi (Kullanıcı)
            halign_type = 'right'
            self.size_hint_x = 0.9
            self.pos_hint = {'right': 0.98}
        else:
            bg_color = (0.15, 0.16, 0.22, 0.9)  # Yarı şeffaf koyu gri (Ş.A.H.İ.N.)
            halign_type = 'left'
            self.size_hint_x = 0.92
            self.pos_hint = {'x': 0.02}

        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.label = Label(
            text=text,
            markup=True,
            size_hint_y=None,
            halign=halign_type,
            valign='middle',
            color=(1, 1, 1, 1),
            font_size=17
        )
        self.label.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
        self.label.bind(texture_size=lambda s, t: self.setter('height')(self, t[1] + 30))
        self.label.bind(texture_size=lambda s, t: setattr(s, 'height', t[1]))
        
        self.add_widget(self.label)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class SahinApp(App):
    def build(self):
        self.title = "Ş.A.H.İ.N. Yapay Zeka"
        
        # Ana arkaplan desenli yerleşim
        layout = TechBackgroundLayout(orientation='vertical', padding=10, spacing=10)
        
        # Üst Panel: Yazı yazma yeri ve gönder butonu EN ÜSTTE (Klavyeden etkilenmez)
        ust_panel = BoxLayout(orientation='horizontal', size_hint=(1, None), height=65, spacing=8)
        
        self.user_input = TextInput(
            hint_text='Mesajınızı yazın efendim...', 
            size_hint=(0.78, 1), 
            multiline=False,
            background_color=(0.1, 0.11, 0.15, 0.9),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[12, 16, 12, 12],
            font_size=16
        )
        self.user_input.bind(on_text_validate=self.komut_isle)
        ust_panel.add_widget(self.user_input)
        
        send_button = Button(
            text='GÖNDER 🦅', 
            size_hint=(0.22, 1),
            background_color=(0.15, 0.5, 0.8, 1),
            font_size=14
        )
        send_button.bind(on_press=self.komut_isle)
        ust_panel.add_widget(send_button)
        
        layout.add_widget(ust_panel)
        
        # Sohbet Geçmişi Alanı
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.chat_layout = GridLayout(cols=1, spacing=14, size_hint_y=None, padding=[5, 10, 5, 10])
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        
        self.scroll.add_widget(self.chat_layout)
        layout.add_widget(self.scroll)
        
        # Karşılama mesajı
        self.ekle_mesaj("[color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] Sistemler aktif ve ağ deseni yüklendi. Emrinizi bekliyorum efendim.", is_user=False)
        
        return layout

    def ekle_mesaj(self, metin, is_user=False):
        bubble = ChatBubble(text=metin, is_user=is_user)
        self.chat_layout.add_widget(bubble)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.05)

    def komut_isle(self, instance):
        ham_komut = self.user_input.text.strip()
        if not ham_komut:
            return
        
        komut = ham_komut.lower()
        self.ekle_mesaj(ham_komut, is_user=True)
        self.user_input.text = ""
        
        # 1. ÇIKIŞ
        if komut in ["kapat", "çık", "sistemi kapat"]:
            self.ekle_mesaj("[color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] Sistem uyku moduna alınıyor. İyi günler efendim...", is_user=False)
            return

        # 2. GİZLİ KOD: "krüt"
        elif "krüt" in komut:
            self.ekle_mesaj("[color=#DA70D6]🧠 [ZİNCİRLEME DÜŞÜNME - CoT AKTİF][/color]\n  └─ Gizli kod doğrulandı.", is_user=False)
            self.ekle_mesaj("[b][color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] Tarihin her sayfasında şanla, şerefle ve bağımsızlıkla yazılmış asil bir milletin evladı olmak en büyük gururdur efendim! Ne mutlu Türk'üm diyene! 🇹🇷[/b]", is_user=False)

        # 3. EASTER EGG: IP BULMA ANİMASYONU
        elif "jarvis" in komut and "ip" in komut:
            self.ekle_mesaj("[color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] Peki efendim, hedef ağ taranıyor...\n[color=#FF4500]🔒 SIZMA PROTOKOLÜ AKTİF[/color]", is_user=False)
            
            temp_bubble = ChatBubble(text="[color=#00FF00]BYPASS: Başlatılıyor...[/color]", is_user=False)
            self.chat_layout.add_widget(temp_bubble)
            
            self.bypass_sayac = 0
            def ip_akis_adim(dt):
                if self.bypass_sayac < 35:
                    rastgele_kodlar = "".join(random.choice("0189ABCDEF#%&*<>[]/\\") for _ in range(24))
                    temp_bubble.label.text = f"[color=#00FF00]BYPASS_{random.randint(100,999)}: {rastgele_kodlar}[/color]"
                    self.bypass_sayac += 1
                    return True
                else:
                    self.chat_layout.remove_widget(temp_bubble)
                    sahte_ip = f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                    self.ekle_mesaj(f"[b][color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] Hedef IP yakalandı: [color=#00FFFF]{sahte_ip}[/color] 🎯[/b]\n[color=#FFD700]Hedefin harika bir gün geçirdiğinden emin olundu efendim.[/color]", is_user=False)
                    return False

            Clock.schedule_interval(ip_akis_adim, 0.06)

        # 4. SAAT
        elif "saat" in komut:
            simdi = datetime.datetime.now().strftime('%H:%M:%S')
            self.ekle_mesaj(f"[color=#DA70D6]🧠 [CoT AKTİF][/color]\n[color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] Zaman: {simdi}", is_user=False)

        else:
            self.ekle_mesaj(f"[color=#FFD700]🦅 Ş.A.H.İ.N.:[/color] '{ham_komut}' komutu kayıtlarda tanımlı değil efendim.", is_user=False)

if __name__ == '__main__':
    SahinApp().run()
