import colorsys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    hsv = rgb_to_hsv(rgb)
    return hsv

def rgb_to_hsv(rgb_color):
    r, g, b = [x / 255.0 for x in rgb_color]
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val

    if delta == 0:
        hue = 0
    elif max_val == r:
        hue = 60 * ((g - b) / delta % 6)
    elif max_val == g:
        hue = 60 * ((b - r) / delta + 2)
    elif max_val == b:
        hue = 60 * ((r - g) / delta + 4)

    saturation = 0 if max_val == 0 else delta / max_val
    value = max_val

    return round(hue), round(saturation * 100), round(value * 100)

def hex_to_hue(hex_color):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    max_val, min_val = max(r, g, b), min(r, g, b)

    if max_val == min_val:
        hue = 0
    elif max_val == r:
        hue = 60 * ((g - b) / (max_val - min_val))
    elif max_val == g:
        hue = 60 * ((b - r) / (max_val - min_val)) + 120
    else:
        hue = 60 * ((r - g) / (max_val - min_val)) + 240

    hue = (hue + 360) % 360
    return hue

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
def is_grayscale(rgb, tolerance=10):
    return abs(rgb[0] - rgb[1]) <= tolerance and abs(rgb[1] - rgb[2]) <= tolerance and abs(rgb[0] - rgb[2]) <= tolerance

def is_low_brightness(rgb, brightness_threshold=50):
    return all(value < brightness_threshold for value in rgb)

def is_low_value_hsv(hex_color, value_threshold=0.0, value_upper_threshold=0.4):
    rgb = hex_to_rgb(hex_color)
    hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    return value_threshold < hsv[2] < value_upper_threshold

def is_low_saturation_hsv(hex_color, saturation_threshold=0.1):
    rgb = hex_to_rgb(hex_color)
    hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    return hsv[1] < saturation_threshold

def is_neutral_color(hex_color1,hex_color2, brightness_threshold=100,
                     value_threshold=0.05, value_upper_threshold=0.5,
                     saturation_threshold=0.1):
    rgb1 = hex_to_rgb(hex_color1)
    rgb2 = hex_to_rgb(hex_color2)
    is_neutral1 = is_grayscale(rgb1) or is_low_brightness(rgb1, brightness_threshold) or is_low_value_hsv(hex_color1, value_threshold, value_upper_threshold) or is_low_saturation_hsv(hex_color1, saturation_threshold)
    is_neutral2 = is_grayscale(rgb2) or is_low_brightness(rgb2, brightness_threshold) or is_low_value_hsv(hex_color2, value_threshold, value_upper_threshold) or is_low_saturation_hsv(hex_color2, saturation_threshold)

    if is_neutral1 and is_neutral2:
        return "netrals"
    elif is_neutral1 or is_neutral2:
        return "netral"
    else:
        return False
def is_analogous(color1, color2, threshold=25):
    hsv1 = hex_to_hsv(color1)
    hsv2 = hex_to_hsv(color2)

    hue1, _, _ = hsv1
    hue2, _, _ = hsv2

    hue_diff = abs(hue1 - hue2)
    if(hue_diff <= threshold):
      return ("analogous")


def is_pastel_color(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    hsv_color = colorsys.rgb_to_hsv(rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0)
    saturation, value = hsv_color[1], hsv_color[2]
    saturation_threshold_low = 0.1
    saturation_threshold = 0.6
    value_threshold_low = 0.6
    value_threshold = 1.0
    is_pastel = saturation_threshold_low < saturation < saturation_threshold and value_threshold > value > value_threshold_low

    if (is_pastel):
        return ("pastel")
    else:
        return False


def are_colors_complementary(hex_color1, hex_color2, tolerance=15):
    hue1 = hex_to_hue(hex_color1)
    hue2 = hex_to_hue(hex_color2)
    hue_difference = abs(hue1 - hue2)
    complementary_condition = abs(hue_difference - 180) <= tolerance

    if(complementary_condition):
      return ("complementary")
    else:
      return False


def is_monochromatic(hex_color1, hex_color2, brightness_threshold=70, color_threshold=80):
    color1 = hex_to_rgb(hex_color1)
    color2 = hex_to_rgb(hex_color2)
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    brightness_diff = abs((r1 + g1 + b1) / 3 - (r2 + g2 + b2) / 3)

    color_diff = max(abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))

    brightness_threshold = brightness_threshold
    color_threshold = color_threshold

    if (brightness_diff <= brightness_threshold and color_diff <= color_threshold):
        return ("monokromatik")
    else:
        return False
def is_triadic_color(hex1, hex2, tolerance=10):
    hue1 = hex_to_hue(hex1)
    hue2 = hex_to_hue(hex2)

    diff1 = abs(hue1 - hue2)
    diff2 = abs(hue2 - hue1)

    within_tolerance = lambda x: 120 - tolerance <= x <= 120 + tolerance

    pure_triadic = (within_tolerance(min(diff1, diff2)) or within_tolerance(max(diff1, diff2))) or (diff1 % 120 == 0 and within_tolerance(diff2 % 120)) or (diff2 % 120 == 0 and within_tolerance(diff1 % 120))

    if(pure_triadic):
      return ("triadic")
    else:
      return False
def is_tetradic_color(hex1, hex2,tolerance=10 ):
    hue1 = hex_to_hue(hex1)
    hue2 = hex_to_hue(hex2)

    diff1 = abs(hue1 - hue2)
    diff2 = abs(hue2 - hue1)

    within_tolerance = lambda x: 90 - tolerance <= x <= 90 + tolerance

    tetradic_relationship = (within_tolerance(min(diff1, diff2)) or within_tolerance(max(diff1, diff2))) or (diff1 % 90 == 0 and within_tolerance(diff2 % 90)) or (diff2 % 90 == 0 and within_tolerance(diff1 % 90))


    if(tetradic_relationship):
      return ("tetradic")
    else:
      return False


def is_good_combination(hex_color1, hex_color2):
    verdict = []
    verdict.append(is_neutral_color(hex_color1,hex_color2))
    verdict.append(is_pastel_color(hex_color1))
    verdict.append(is_pastel_color(hex_color2))
    verdict.append(are_colors_complementary(hex_color1, hex_color2))
    verdict.append(is_triadic_color(hex_color1, hex_color2))
    verdict.append(is_tetradic_color(hex_color1, hex_color2))
    verdict.append(is_monochromatic(hex_color1, hex_color2))
    verdict.append(is_analogous(hex_color1, hex_color2))

    valid_verdicts = [v for v in verdict if v is not None and v is not False]
    message= "kombinasi Warna tersebut sudah baik karena kombinasi tersebut masuk dalam teori " + ", ".join(valid_verdicts)
    if valid_verdicts:
        return valid_verdicts
    else:
        return False

def recommend_outfit(top, bottom):
    if top == 'Tshirts':
        return 'Casual'
    elif top == 'Shirts':
        if bottom == 'Jeans':
            return 'Smart Casual'
        elif bottom == 'pants':
            return 'Formal'
        elif bottom == 'Shorts':
            return 'Smart Casual'
        elif bottom == 'Skirts':
            return 'Formal'
    elif top == 'Jackets':
        return 'Casual'
    elif top == 'Dresses':
        return 'Formal'
    elif top == 'Longsleeve':
        return 'Casual'
    elif top == 'Hoodie':
        return 'Casual'
    elif top == 'Tops':
        return 'Casual'
    else:
        return 'unrecognized pattern'


def get_combinations(data):
    tops = []
    bottoms = []
    dresses= []
    all_combinations = []
    recommendations = []

    for item_key, item_value in data.items():
        if item_value["type"] in ["Tshirts", "Shirts", "Jackets", "Longsleeve", "Hoodie", "Tops"]:
            tops.append(item_value)
        elif item_value["type"] == "Dresses":
            dresses.append(item_value)
        else:
            bottoms.append(item_value)

    for top in tops:
        for bottom in bottoms:
            all_combinations.append({"top": top, "bottom": bottom})

    for dress in dresses:
        all_combinations.append({"dress": dress})

    for combination in all_combinations:
        if "top" in combination and "bottom" in combination:
            top_id = combination["top"]["image_path"].split("/")[-1]
            bottom_id = combination["bottom"]["image_path"].split("/")[-1]
            top_type = combination["top"]["type"]
            bottom_type = combination["bottom"]["type"]
            result_outfit_type = recommend_outfit(top_type, bottom_type)
            result_color_combination = is_good_combination(combination["top"]["color"],
                                                           combination["bottom"]["color"])
        elif "dress" in combination:
            dress_id = combination["dress"]["image_path"].split("/")[-1]
            dress_type = combination["dress"]["type"]
            result_outfit_type = recommend_outfit(dress_type, dress_type)
            result_color_combination = is_good_combination(combination["dress"]["color"],
                                                           combination["dress"]["color"])





        if result_color_combination:
            color_theory = result_color_combination[0]
            if ("dress" in combination):
                message="Dress sangat akan memberikan tampilan feminim dan elegan, sangat cocok untuk acara formal."
            elif (result_outfit_type == "Formal" and (
                    color_theory == 'triadic' or color_theory == 'tetradic' or color_theory == 'complementary')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Formal, namun pemilihan warna perlu dipertimbangkan karena kombinasi warna anda yang termasuk dalam teori warna {color_theory} yang mengurangi kesan formal pada tampilan Anda. Lebih cocok digunakan untuk acara semi-formal."
            elif (result_outfit_type == "Smart Casual" and (
                    color_theory == 'triadic' or color_theory == 'tetradic' or color_theory == 'complementary')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Smart Casual, kombinasi warna yang baik dan akan menimbulkan kesan rapi namun tetap ceria dan berwarna karena kombinasi tersebut termasuk dalam teori warna {color_theory}"
            elif (result_outfit_type == "Casual" and (
                    color_theory == 'triadic' or color_theory == 'tetradic' or color_theory == 'complementary')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Casual, kombinasi warna yang baik dan akan menimbulkan kesan santai, ceria, dan berwarna karena kombinasi tersebut termasuk dalam teori warna {color_theory}"
            elif (result_outfit_type == "Formal" and (color_theory == 'pastel')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Formal, kombinasi warna ini akan menghasilkan kesan tenang dan santai. Lebih cocok digunakan untuk acara semi-formal."
            elif (result_outfit_type == "Smart Casual" and (color_theory == 'pastel')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Smart Casual dengan kombinasi warna yang baik dan akan menimbulkan kesan rapi, tenang, dan bersih karena kombinasi tersebut termasuk dalam teori warna {color_theory}"
            elif (result_outfit_type == "Casual" and (color_theory == 'pastel')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Casual dengan kombinasi warna yang baik dan akan menimbulkan kesan santai, tenang, dan bersih karena kombinasi tersebut termasuk dalam teori warna {color_theory}"
            elif (result_outfit_type == "Formal" and (color_theory == 'netrals')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Formal, kombinasi warna ini akan menghasilkan kesan profesional dan rapi. Sangat cocok digunakan untuk acara formal."
            elif (result_outfit_type == "Smart Casual" and (color_theory == 'netrals')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Smart Casual dengan kombinasi warna yang baik dan akan menimbulkan kesan rapi dan profesional namun lebih santai karena kombinasi tersebut termasuk dalam teori warna {color_theory}"
            elif (result_outfit_type == "Casual" and (color_theory == 'netrals')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan memberikan tampilan Casual yang santai namun tetap stylish. Kombinasi warna yang seragam menciptakan kesan yang harmonis dan dapat menjadi pilihan yang sempurna untuk aktivitas sehari-hari, seperti hangout dengan teman atau kegiatan santai lainnya."
            elif (result_outfit_type == "Formal" and (color_theory == 'netral')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Formal, kombinasi warna netral dan yang lebih berwarna akan menambah kesan elegan. Padu-padan warna netral dengan yang lebih berani akan memberikan kesan menarik dan cocok untuk acara formal yang lebih santai."
            elif (result_outfit_type == "Smart Casual" and (color_theory == 'netral')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Smart Casual dengan gabungan warna netral dan yang lebih berwarna akan menambah kesan santai dan tetap terlihat cerdas. Cocok untuk acara semi-formal atau pertemuan santai bersama teman-teman."
            elif (result_outfit_type == "Casual" and (color_theory == 'netral')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menciptakan tampilan Casual yang menarik dengan kombinasi warna netral dan berwarna. Paduan warna ini memberikan kesan santai namun tetap stylish, cocok untuk berbagai kesempatan seperti hangout atau acara santai bersama teman-teman."
            elif (result_outfit_type == "Formal" and (color_theory == 'monokromatik')):
                message = f"Tampilan formal dengan warna monokromatik pada {top_type} dan {bottom_type} menciptakan kesan elegan dan rapi. Pilih nuansa dari satu parent warna untuk penampilan yang kohesif. Ideal untuk acara resmi seperti pertemuan bisnis atau pesta formal yang memerlukan keanggunan dan keseragaman warna."
            elif (result_outfit_type == "Smart Casual" and (color_theory == 'monokromatik')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Smart Casual dengan pilihan nuansa dari satu parent warna akan menghasilkan tampilan yang santai namun tetap stylish. Cocok untuk acara semi-formal atau pertemuan santai bersama teman-teman."
            elif (result_outfit_type == "Casual" and (color_theory == 'monokromatik')):
                message = f"Tampilan {result_outfit_type} yang effortlessly stylish bisa diciptakan dengan kombinasi {top_type} dan {bottom_type} dalam warna {color_theory}. Pilih nuansa dari satu parent warna untuk tampilan santai yang tetap terlihat trendi. Cocok untuk berbagai aktivitas sehari-hari dan pertemuan santai bersama teman-teman."
            elif (result_outfit_type == "Formal" and (color_theory == 'analogous')):
                message = f"Untuk tampilan formal yang mencolok, pertimbangkan kombinasi {top_type} dan {bottom_type} dengan warna analogous. Memilih warna sejajar akan memberikan kesan yang kohesif namun tetap menarik."
            elif (result_outfit_type == "Smart Casual" and (color_theory == 'analogous')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menghasilkan look Smart Casual dengan paduan nuansa yang berdekatan pada roda warna untuk menciptakan kombinasi yang serasi dan memancarkan kesan yang cerdas namun santai. Ideal untuk acara semi-formal dan pertemuan yang santai."
            elif (result_outfit_type == "Casual" and (color_theory == 'analogous')):
                message = f"Kombinasi {top_type} dan {bottom_type} akan menciptakan tampilan Casual yang menarik dengan pilihan warna-warna yang berdekatan satu sama lain di roda warna untuk menciptakan penampilan yang menyatu dan penuh keceriaan. Cocok untuk acara santai atau kegiatan sehari-hari yang ingin tetap tampil stylish."

            if "top" in combination and "bottom" in combination:
                recommendation = {
                    "recommendation_id": len(recommendations) - 1 + 1,
                    "top": {
                        "id": top_id,
                        "type": top_type,
                        "color_hex": combination["top"]["color"],
                        "image": combination["top"]["image_path"]
                    },
                    "bottom": {
                        "id": bottom_id,
                        "type": bottom_type,
                        "color_hex": combination["bottom"]["color"],
                        "image": combination["bottom"]["image_path"]
                    },
                    "message": message
                }
            elif "dress" in combination:
                recommendation = {
                    "recommendation_id": len(recommendations) - 1 + 1,
                    "dress": {
                        "id": dress_id,
                        "type": dress_type,
                        "color_hex": combination["dress"]["color"],
                        "image": combination["dress"]["image_path"]
                    },
                    "message": message
                }
            recommendations.append(recommendation)

    return recommendations