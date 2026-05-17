import requests
BASE_URL  = "http://localhost:5000/palette"

def call (description,params,expect_status = 200):
    print ( f"Testing {description} ..." )
    r = requests.get (BASE_URL,params = params)
    data = r.json()
    status = "PASS" if r.status_code == expect_status else "FAIL"
    print ( f"{status} HTTP {r.status_code}" )
    if "colors" in data:
        print ( f"colors: {data["colors"]}" )
    else:
        print ( f"error: {data["error"]}" )


print("=== Color Palette Generator Test Program ===")

call("Triadic",
     {"base_color": "#FF5733", "harmony_rule": "triadic"})

call("Analogous (count=4)",
     {"base_color": "#FF5733", "harmony_rule": "analogous", "count": 4})

call("Monochromatic (count=5)",
     {"base_color": "#6A0DAD", "harmony_rule": "monochromatic", "count": 5})

call("Error — invalid hex",
     {"base_color": "#ZZZZZZ", "harmony_rule": "triadic"}, expect_status=400)

call("Error — unsupported rule",
     {"base_color": "#FF5733", "harmony_rule": "random"}, expect_status=400)

print("\n=== Done ===")