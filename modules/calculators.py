# modules/calculators.py
import requests

class EECalculator:
    @staticmethod
    def calculate_basic(temp_out, temp_in, power_kwh, area_sqm):
        """Basic offline calculation"""
        if power_kwh <= 0 or area_sqm <= 0:
            return 0, "N/A"
        
        delta_t = abs(temp_out - temp_in)
        energy_per_sqm = power_kwh / area_sqm
        
        if energy_per_sqm == 0:
            return 999, "A+"
            
        ee_final = delta_t / energy_per_sqm
        
        if ee_final > 5.0: rating = "A (Excellent)"
        elif ee_final > 3.0: rating = "B (Good)"
        elif ee_final > 1.5: rating = "C (Average)"
        else: rating = "D (Poor)"
        
        return round(ee_final, 2), rating

class CloudOrLocalCalculator:
    @staticmethod
    def get_ee_score(sensor_data):
        cloud_url = "https://your-api.com/api/scan" # Replace with your real URL later
        
        try:
            # TRY CLOUD (Timeout 3 seconds)
            response = requests.post(cloud_url, json=sensor_data, timeout=3)
            response.raise_for_status()
            
            cloud_result = response.json()
            cloud_result['source'] = 'Cloud'
            return cloud_result
            
        except Exception:
            # OFFLINE FALLBACK
            local_ee_score, local_ee_rating = EECalculator.calculate_basic(
                temp_out=sensor_data['outside_temp'],
                temp_in=sensor_data['inside_temp'],
                power_kwh=sensor_data['power_kwh'],
                area_sqm=sensor_data['area']
            )
            
            offline_result = {
                "ee_score": local_ee_score,
                "rating": local_ee_rating,
                "suggested_price": None, 
                "premium": None,
                "source": "Offline"
            }
            return offline_result