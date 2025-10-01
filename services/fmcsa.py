import requests
import os
import time
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
        self._cache = {}  # Simple in-memory cache
        self._cache_ttl = 300  # 5 minutes cache

    def verify_mc_number(self, mc_number) -> Dict:
        """
        Verify MC number using FMCSA API (docket-number endpoint)
        Accepts both string and numeric MC numbers
        """
        try:
            # Convert to string if it's a number
            if isinstance(mc_number, (int, float)):
                mc_number = str(int(mc_number))
            elif not isinstance(mc_number, str):
                mc_number = str(mc_number)
            
            clean_mc = mc_number.replace('MC-', '').replace('MC', '').strip()
            
            # Check cache first
            cache_key = f"mc_{clean_mc}"
            if cache_key in self._cache:
                cached_result, cached_time = self._cache[cache_key]
                if time.time() - cached_time < self._cache_ttl:
                    logger.info(f"Using cached result for MC: {clean_mc}")
                    return cached_result
            url = f"{self.base_url}/docket-number/{clean_mc}?webKey={self.api_token}"

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            logger.info(f"Querying FMCSA API for MC: {clean_mc}")
            start_time = time.time()

            response = requests.get(url, headers=headers, timeout=5)  # Reduced timeout
            
            end_time = time.time()
            logger.info(f"FMCSA API response time: {end_time - start_time:.2f} seconds")

            if response.status_code == 200:
                data = response.json()
                content = data.get('content', [])
                if not content:
                    return {
                        "eligible": False,
                        "mc_number": clean_mc,
                        "status": "not_found",
                        "message": "MC number not found in FMCSA database"
                    }
                # Pass the first carrier record to processor
                result = self._process_carrier_data(content[0].get('carrier', {}), clean_mc)
                # Cache the result
                self._cache[cache_key] = (result, time.time())
                return result
            elif response.status_code == 404:
                result = {
                    "eligible": False,
                    "mc_number": clean_mc,
                    "status": "not_found",
                    "message": "MC number not found in FMCSA database"
                }
                # Cache negative results too
                self._cache[cache_key] = (result, time.time())
                return result
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

    def _process_carrier_data(self, carrier: Dict, mc_number: str) -> Dict:
        """Process FMCSA API carrier data dict"""
        try:
            legal_name = carrier.get('legalName', 'Unknown')
            dba_name = carrier.get('dbaName', '')
            operating_status = carrier.get('statusCode', 'Unknown')
            out_of_service_date = carrier.get('oosDate')

            is_active = operating_status.upper() == 'A'
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