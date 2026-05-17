import colorsys
from flask import  Flask,request,jsonify

app = Flask(__name__)

# Helper Functions
def hex_to_hls(hex_color):
    """Convert HEX value(#RRGGBB) to (h,l,s)) in [0,1]"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)/255
    g = int(hex_color[2:4], 16)/255
    b = int(hex_color[4:6], 16)/255
    return colorsys.rgb_to_hls(r,g,b)

def hls_to_hex(h,l,s):
    """Convert (h,s,l)) in [0,1] to HEX value(#RRGGBB)"""
    h = h%1 #wrap value
    l = max(0.0,min(1.0,l))
    s = max(0.0,min(1.0,s))
    r,g,b = colorsys.hls_to_rgb(h,l,s)
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))

def is_valid_hex(value):
    """Check if the given string is a valid HEX value"""
    if not isinstance(value,str):
        return False
    v = value.lstrip('#')
    if len(v) != 6:
        return False
    try:
        int(v,16)
    except ValueError:
        return False
    return True

# Harmony Functions
def generate_triadic(hex_color):
    """Always return 3 colors: base + 120 and 140"""
    h,l,s = hex_to_hls(hex_color)
    return[hls_to_hex(h,l,s),hls_to_hex(h+1/3,l,s),hls_to_hex(h+2/3,l,s)]

def generate_analogous(hex_color,count=3):
    """
    Returns `count` colors (3–5) spread +- 30 around the base hue.
    For count=3: base +-30
    For count=4: base, +15, +30, -15
    For count=5: base +- 15, +_ 30
    """
    h,l,s = hex_to_hls(hex_color)
    step = 30/360
    if count == 3:
        offset = [-step,0,step]
    elif count == 4:
        offset = [-step/2,0,step/2,step]
    else:
        offset = [-step,-step/2,0,step/2,step]
    return [hls_to_hex(h+x,l,s) for x in offset]

def generate_monochromatic(hex_color,count=3):
    """Returns `count` colors (3–5) with the same hue, varying lightness.Always includes the base color. Lightness spread across [0.2, 0.8]."""
    h,l,s = hex_to_hls(hex_color)
    light_min = 0.2
    light_max = 0.8
    steps = [light_min+x*(light_max-light_min)/(count-1) for x in range(count)]

    #find step closest to the base lightness
    closest = 0
    min_diff = abs(steps[0] - l)
    for i in range(count):
        diff = abs(steps[i] - l)
        if diff < min_diff:
            min_diff = diff
            closest = i

    result = [hls_to_hex(h, lv, s) for lv in steps]
    result[closest] = hls_to_hex(h, l, s) # replace the closest color with the exact base color
    return result

# Route
SUPPORTED_RULES = ["triadic","analogous","monochromatic"]
@app.route('/palette',methods=['GET'])
def palette():
    base_color = request.args.get("base_color", "").strip()
    harmony_rule = request.args.get("harmony_rule", "").strip().lower()
    count_raw = request.args.get("count", None)

    #validate base color
    if not base_color:
        return jsonify({"error":"base_color is required"}),400
    if not base_color.startswith("#"):
        base_color = "#"+base_color
    if not is_valid_hex(base_color):
        return jsonify({"error":"base_color should be a valid HEX value(e.g. #FF5733)"}),400

    # validate harmony rule
    if not harmony_rule:
        return jsonify({"error":"harmony_rule is required"}),400
    if harmony_rule not in SUPPORTED_RULES:
        return jsonify({"error":"harmony_rule should be one of {}".format(SUPPORTED_RULES)}),400

    # validate count
    count = 3
    if count_raw is not None:
        try:
            count = int(count_raw)
        except ValueError:
            return jsonify({"error":"count should be an integer"}),400
        if count < 3 or count > 5:
            return jsonify({"error":"count should be between 3 and 5"}),400

    # generate palette
    if harmony_rule == "triadic":
        colors = generate_triadic(base_color)
    elif harmony_rule == "analogous":
        colors = generate_analogous(base_color,count)
    else:
        colors = generate_monochromatic(base_color,count)

    return jsonify({"colors":colors})

# entry point
if __name__ == '__main__':
    app.run(host= "0.0.0.0",port =5000,debug=True)