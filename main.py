import time
time.sleep(2) # Give Android 2 seconds to initialize the display before loading KivyMD
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
import requests

# --- CLOUD / OFFLINE CALCULATOR ---
class CloudOrLocalCalculator:
    @staticmethod
    def get_ee_score(sensor_data):
        cloud_url = "https://your-api.com/api/scan" 
        try:
            response = requests.post(cloud_url, json=sensor_data, timeout=3)
            response.raise_for_status()
            cloud_result = response.json()
            cloud_result['source'] = 'Cloud'
            return cloud_result
        except Exception:
            delta_t = abs(sensor_data['outside_temp'] - sensor_data['inside_temp'])
            energy_per_sqm = sensor_data['power_kwh'] / sensor_data['area']
            if energy_per_sqm == 0: energy_per_sqm = 0.01
            ee_final = delta_t / energy_per_sqm
            
            if ee_final > 5.0: rating = "A (Excellent)"
            elif ee_final > 3.0: rating = "B (Good)"
            elif ee_final > 1.5: rating = "C (Average)"
            else: rating = "D (Poor)"
            
            return {"ee_score": round(ee_final, 2), "rating": rating, "suggested_price": None, "premium": None, "source": "Offline"}

# --- MAIN APP UI ---
class ProfessionalEEMonitorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        title = MDLabel(text="EE Inspector Pro", halign="center", font_style="H4", size_hint_y=0.08)
        main_layout.add_widget(title)
        
        input_card = MDCard(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=0.25, elevation=2, radius=[dp(15)])
        self.area_input = MDTextField(hint_text="Apartment Area (m2)", input_filter="int", text="80")
        self.temp_out_input = MDTextField(hint_text="Outside Temp (C)", input_filter="float", text="35")
        self.temp_in_input = MDTextField(hint_text="Inside Temp (C)", input_filter="float", text="24")
        self.power_input = MDTextField(hint_text="HVAC Power (kWh)", input_filter="float", text="1.2")
        
        input_card.add_widget(MDLabel(text="Scan Parameters", font_style="H6"))
        input_card.add_widget(self.area_input)
        input_card.add_widget(self.temp_out_input)
        input_card.add_widget(self.temp_in_input)
        input_card.add_widget(self.power_input)
        main_layout.add_widget(input_card)
        
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
        
        self.btn_scan = MDRaisedButton(text="CALCULATE EE SCORE", size_hint_y=0.12, font_size=dp(18), on_press=self.calculate_ee)
        main_layout.add_widget(self.btn_scan)
        
        screen.add_widget(main_layout)
        return screen

    def calculate_ee(self, instance):
        try:
            area = float(self.area_input.text)
            temp_out = float(self.temp_out_input.text)
            temp_in = float(self.temp_in_input.text)
            power = float(self.power_input.text)
        except ValueError:
            self.lbl_status.text = "Status: Error in input values!"
            return

        sensor_data = {"outside_temp": temp_out, "inside_temp": temp_in, "power_kwh": power, "area": area}
        self.lbl_ee_score.text = "Calculating..."
        self.lbl_status.text = "Status: Contacting Cloud..."

        result_data = CloudOrLocalCalculator.get_ee_score(sensor_data)

        self.lbl_ee_score.text = f"EE Score: {result_data['ee_score']}"
        self.lbl_ee_rating.text = f"Rating: {result_data['rating']}"

        if result_data['source'] == 'Offline':
            self.lbl_status.text = "OFFLINE MODE: Approximate score only."
            self.lbl_status.text_color = [1, 0.8, 0, 1]
            self.lbl_price.text = "Price Premium: Requires Cloud"
            self.lbl_price.text_color = [0.5, 0.5, 0.5, 1]
        else:
            self.lbl_status.text = "Connected to Cloud (Precise)"
            self.lbl_status.text_color = [0, 0.8, 1, 1]
            if result_data['suggested_price'] is not None:
                self.lbl_price.text = f"Suggested Price: ${result_data['suggested_price']:,.2f}"

if __name__ == '__main__':
    ProfessionalEEMonitorApp().run()
