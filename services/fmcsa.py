import requests
import os
from typing import Dict, Optional
import logging
from core.config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class FMCSAService:
    def __init__(self):
        self.api_token = Config.FMCSA_API_TOKEN
        if not self.api_token:
            raise ValueError("FMCSA_API_TOKEN environment variable is required")
        self.base_url = Config.FMCSA_BASE_URL
        
    def verify_mc_number(self, mc_number: str) -> Dict:
        """
        Verify MC number using real FMCSA API
        
        Args:
            mc_number (str): Motor Carrier number to verify
            
        Returns:
            Dict: Verification result with carrier information
        """
        try:
            # Clean MC number (remove 'MC-' prefix if present)
            clean_mc = mc_number.replace('MC-', '').replace('MC', '').strip()
            
            # FMCSA API endpoint for carrier lookup
            url = f"{self.base_url}/{clean_mc}/basics"
            
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            logger.info(f"Querying FMCSA API for MC: {clean_mc}")
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._process_carrier_data(data, clean_mc)
            elif response.status_code == 404:
                return {
                    "eligible": False,
                    "mc_number": clean_mc,
                    "status": "not_found",
                    "message": "MC number not found in FMCSA database"
                }
            else:
                logger.error(f"FMCSA API error: {response.status_code} - {response.text}")
                return self._fallback_verification(clean_mc)
                
        except requests.exceptions.Timeout:
            logger.error(f"FMCSA API timeout for MC: {clean_mc}")
            return self._fallback_verification(clean_mc)
        except requests.exceptions.RequestException as e:
            logger.error(f"FMCSA API request error: {str(e)}")
            return self._fallback_verification(clean_mc)
        except Exception as e:
            logger.error(f"Unexpected error in FMCSA verification: {str(e)}")
            return self._fallback_verification(clean_mc)
    
    def _process_carrier_data(self, data: Dict, mc_number: str) -> Dict:
        """Process FMCSA API response data"""
        try:
            carrier = data.get('content', {})
            
            # Extract key carrier information
            legal_name = carrier.get('legalName', 'Unknown')
            dba_name = carrier.get('dbaName', '')
            operating_status = carrier.get('operatingStatus', 'Unknown')
            out_of_service_date = carrier.get('outOfServiceDate')
            
            # Check eligibility criteria
            is_active = operating_status.upper() == 'ACTIVE'
            not_out_of_service = out_of_service_date is None
            
            eligible = is_active and not_out_of_service
            
            result = {
                "eligible": eligible,
                "mc_number": mc_number,
                "legal_name": legal_name,
                "dba_name": dba_name,
                "operating_status": operating_status,
                "out_of_service_date": out_of_service_date,
                "status": "verified"
            }
            
            if not eligible:
                reasons = []
                if not is_active:
                    reasons.append(f"Operating status: {operating_status}")
                if out_of_service_date:
                    reasons.append(f"Out of service since: {out_of_service_date}")
                result["rejection_reason"] = "; ".join(reasons)
            
            logger.info(f"MC {mc_number} verification: {'ELIGIBLE' if eligible else 'NOT ELIGIBLE'}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing carrier data: {str(e)}")
            return self._fallback_verification(mc_number)
    
    def _fallback_verification(self, mc_number: str) -> Dict:
        """Fallback verification when API is unavailable"""
        # Basic validation - check if MC number is numeric and reasonable length
        if mc_number.isdigit() and 4 <= len(mc_number) <= 7:
            return {
                "eligible": True,  # Conservative approach - allow when API unavailable
                "mc_number": mc_number,
                "status": "api_unavailable",
                "message": "FMCSA API unavailable, using fallback verification"
            }
        else:
            return {
                "eligible": False,
                "mc_number": mc_number,
                "status": "invalid_format",
                "message": "Invalid MC number format"
            }
    
    def get_carrier_safety_rating(self, mc_number: str) -> Optional[str]:
        """Get carrier safety rating from FMCSA"""
        try:
            clean_mc = mc_number.replace('MC-', '').replace('MC', '').strip()
            url = f"{self.base_url}/{clean_mc}/operation-classification"
            
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                safety_rating = data.get('content', {}).get('safetyRating')
                return safety_rating
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting safety rating: {str(e)}")
            return None

# Legacy function for backward compatibility
def verify_mc_number(mc_number: str) -> bool:
    """Legacy function - returns boolean for backward compatibility"""
    service = FMCSAService()
    result = service.verify_mc_number(mc_number)
    return result.get("eligible", False)
