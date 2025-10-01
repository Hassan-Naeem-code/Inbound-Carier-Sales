# MC Number Conversion Feature

## Overview
The `/verify_mc` and `/webhook/happyrobot` endpoints now support MC numbers in multiple formats and automatically convert them to the correct string format for FMCSA API verification.

## Supported MC Number Formats

### Input Formats Accepted:
- **Integer**: `123456`
- **Float**: `123456.0` 
- **String**: `"123456"`
- **String with prefix**: `"MC-123456"` or `"MC 123456"`

### Output Format:
All MC numbers are normalized to clean string format: `"123456"`

## API Examples

### /verify_mc Endpoint

**Integer Input:**
```json
POST /verify_mc
{
  "mc_number": 123456
}
```

**String Input:**
```json  
POST /verify_mc
{
  "mc_number": "MC-123456"
}
```

**Both return the same normalized response:**
```json
{
  "eligible": true,
  "mc_number": "123456",
  "status": "verified",
  "legal_name": "Example Trucking LLC"
}
```

### /webhook/happyrobot Endpoint

**Integer MC Number:**
```json
POST /webhook/happyrobot
{
  "mc_number": 123456,
  "equipment_type": "Dry Van",
  "origin": "Chicago, IL",
  "destination": "Dallas, TX"
}
```

**String MC Number:**
```json
POST /webhook/happyrobot  
{
  "mc_number": "654321",
  "equipment_type": "Refrigerated", 
  "origin": "Los Angeles, CA",
  "destination": "Phoenix, AZ"
}
```

## HappyRobot Integration

This feature is particularly useful for HappyRobot workflows where MC numbers might be extracted as integers from voice recognition or form inputs.

### Example HappyRobot API Call:
```json
{
  "mc_number": 123456  // ← Can be sent as integer
}
```

The API will automatically convert this to `"123456"` for FMCSA verification.

## Implementation Details

### Conversion Logic:
1. **Integer/Float → String**: `str(int(value))`
2. **String → Cleaned String**: Remove "MC-", "MC", and whitespace
3. **Error Handling**: Invalid types raise validation errors

### Validation:
- Pydantic validator ensures type conversion before processing
- FMCSA service handles additional cleaning (prefixes, whitespace)
- Maintains backward compatibility with existing string inputs

## Testing

Run the MC conversion tests:
```bash
python -m pytest test_api.py::test_mc_number_conversion -v
```

Or test manually:
```bash
python test_mc_conversion.py
```

## Benefits

1. **Flexible Input**: Accepts numbers from voice AI, forms, or APIs
2. **Consistent Processing**: All formats normalized to clean strings
3. **Backward Compatible**: Existing string inputs work unchanged
4. **Error Prevention**: Automatic conversion prevents type mismatches
5. **HappyRobot Friendly**: Works seamlessly with voice recognition systems