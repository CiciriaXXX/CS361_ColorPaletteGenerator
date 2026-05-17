# Color Palette Generator — Microservice
## 1. What this microservice does
Given a base HEX color and a harmony rule, the microservice returns a set of harmonious HEX color codes computed using color theory.

**Supported harmony rules:**
- Triadic: always exactly 3 colors(base hue + 120° + 240°)
- Analogous: 3–5 colors (spread ±30° around base hue)
- Monochromatic: 3–5 colors (same hue, varying lightness)
## 2. How to REQUEST data from the microservice
**The microservice must be running before any request is made.**
```bash
# Start the microservice
pip install flask
python app.py
```
Send an **HTTP GET** request to:
```
http://localhost:5000/palette
```
**with** query-string parameters**:**
- base_color (string, required): base color in HEX format
- harmony_rule (string, required): one of triadic, analogous, monochromatic
- count (integer, optional): number of colors to return, between 3 and 5, defaults to 3; only applies to analogous and monochromatic
### Example requests
```python
import requests

# Triadic — always 3 colors
response = requests.get(
    "http://localhost:5000/palette",
    params={"base_color": "#FF5733", "harmony_rule": "triadic"}
)

# Analogous — 4 colors
response = requests.get(
    "http://localhost:5000/palette",
    params={"base_color": "#FF5733", "harmony_rule": "analogous", "count": 4}
)

# Monochromatic — default 3 colors
response = requests.get(
    "http://localhost:5000/palette",
    params={"base_color": "#6A0DAD", "harmony_rule": "monochromatic"}
)
```
## 3. How to RECEIVE data from the microservice

The microservice always responds with **JSON**.

### Success response — HTTP 200

```json
{
  "colors": ["#FF5733", "#33FF57", "#5733FF"]
}
```

### Error response — HTTP 400

```json
{
  "error": "base_color should be a valid HEX value(e.g. #FF5733)"
}
```

### Example: receiving and using the data

```python
import requests

response = requests.get(
    "http://localhost:5000/palette",
    params={"base_color": "#FF5733", "harmony_rule": "analogous", "count": 4}
)

if response.status_code == 200:
    data = response.json()
    colors = data["colors"]          # list of HEX strings, e.g. 4 items
    print(colors)
    # → ['#FF3342', '#FF5733', '#FF8A33', '#FFBD33']
else:
    error = response.json()["error"]
    print(f"Error: {error}")
```
