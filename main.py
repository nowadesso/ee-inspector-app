import sys
import os

# Add the modules folder to Python path so Android can find calculators.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from calculators import CloudOrLocalCalculator

# main.py
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
import sys
import os

# Add the modules folder to Python path so we can import our calculator
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from calculators import CloudOrLocalCalculator

class ProfessionalEEMonitorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # --- HEADER ---
        title = MDLabel(text="EE Inspector Pro", halign="center", font_style="H4", size_hint_y=0.08)
        main_layout.add_widget(title)
        
        # --- INPUT CARD ---
        input_card = MDCard(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=0.25, elevation=2, radius=[dp(15)])
        
        self.area_input = MDTextField(hint_text="Apartment Area (m²)", input_filter="int", text="80")
        self.temp_out_input = MDTextField(hint_text="Outside Temp (°C)", input_filter="float", text="35")
        self.temp_in_input = MDTextField(hint_text="Inside Temp (°C)", input_filter="float", text="24")
        self.power_input = MDTextField(hint_text="HVAC Power (kWh)", input_filter="float", text="1.2")
        
        input_card.add_widget(MDLabel(text="Scan Parameters", font_style="H6"))
        input_card.add_widget(self.area_input)
        input_card.add_widget(self.temp_out_input)
        input_card.add_widget(self.temp_in_input)
        input_card.add_widget(self.power_input)
        main_layout.add_widget(input_card)
        
        # --- RESULTS CARD ---
        self.result_card = MDCard(orientation='vertical', padding=dp(30), spacing=dp(10), size_hint_y=0.35, elevation=1, radius=[dp(15)])
        
        self.lbl_ee_score = MDLabel(text="EE Score: --", halign="center", font_style="H2", theme_text_color="Custom", text_color=[1, 1, 1, 1])
        self.lbl_ee_rating = MDLabel(text="Rating: Waiting...", halign="center", font_style="H5", theme_text_color="Custom", text_color=[0.6, 0.6, 0.6, 1])
        self.lbl_price = MDLabel(text="Premium: --", halign="center", font_style="H6", theme_text_color="Custom", text_color=[0.2, 0.8, 0.2, 1])
        self.lbl_status = MDLabel(text="Status: Ready", halign="center", font_style="Subtitle2", theme_text_color="Custom", text_color=[0.5, 0.5, 0.5, 1])
        
        self.result_card.add_widget(self.lbl_ee_score)
        self.result_card.add_widget(self.lbl_ee_rating)
        self.result_card.add_widget(self.lbl_price)
        self.result_card.add_widget(self.lbl_status)
        main_layout.add_widget(self.result_card)
        
        # --- ACTION BUTTON ---
        self.btn_scan = MDRaisedButton(text="CALCULATE EE SCORE", size_hint_y=0.12, font_size=dp(18), on_press=self.calculate_ee)
        main_layout.add_widget(self.btn_scan)
        
        screen.add_widget(main_layout)
        return screen

    def calculate_ee(self, instance):
        # 1. Get data from inputs
        try:
            area = float(self.area_input.text)
            temp_out = float(self.temp_out_input.text)
            temp_in = float(self.temp_in_input.text)
            power = float(self.power_input.text)
        except ValueError:
            self.lbl_status.text = "Status: Error in input values!"
            return

        sensor_data = {
            "outside_temp": temp_out,
            "inside_temp": temp_in,
            "power_kwh": power,
            "area": area
        }

        # 2. Show loading state
        self.lbl_ee_score.text = "Calculating..."
        self.lbl_status.text = "Status: Contacting Cloud..."

        # 3. Run the Cloud/Offline Logic
        result_data = CloudOrLocalCalculator.get_ee_score(sensor_data)

        # 4. Update UI with Results
        self.lbl_ee_score.text = f"EE Score: {result_data['ee_score']}"
        self.lbl_ee_rating.text = f"Rating: {result_data['rating']}"

        # 5. Handle Online vs Offline UI
        if result_data['source'] == 'Offline':
            # OFFLINE WARNING
            self.lbl_status.text = "⚠️ OFFLINE MODE: Approximate score only."
            self.lbl_status.text_color = [1, 0.8, 0, 1] # Yellow
            self.lbl_price.text = "Price Premium: Requires Cloud"
            self.lbl_price.text_color = [0.5, 0.5, 0.5, 1] # Grey
            self.result_card.md_bg_color = [0.15, 0.15, 0.15, 1] # Dark Grey
        else:
            # ONLINE SUCCESS
            self.lbl_status.text = "☁️ Connected to Cloud (Precise)"
            self.lbl_status.text_color = [0, 0.8, 1, 1] # Blue
            if result_data['suggested_price'] is not None:
                self.lbl_price.text = f"Suggested Price: ${result_data['suggested_price']:,.2f}"
                self.lbl_price.text_color = [0.2, 0.8, 0.2, 1] # Green
            self.result_card.md_bg_color = [0.1, 0.2, 0.1, 1] # Dark Green

if __name__ == '__main__':
    ProfessionalEEMonitorApp().run()