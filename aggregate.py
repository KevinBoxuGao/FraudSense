import os
import csv

# ['Android 7.0', 'iOS 11.1.2', '', 'Mac OS X 10_11_6', 'Windows 10', 'Android', 'Linux', 'iOS 11.0.3', 'Mac OS X 10_7_5', 'Mac OS X 10_12_6', 'Mac OS X 10_13_1', 'iOS 11.1.0', 'Mac OS X 10_9_5', 'Windows 7', 'Windows 8.1', 'Mac', 'iOS 10.3.3', 'Mac OS X 10.12', 'Mac OS X 10_10_5', 'Mac OS X 10_11_5', 'iOS 9.3.5', 'Android 5.1.1', 'Android 7.1.1', 'Android 6.0', 'iOS 10.3.1', 'Mac OS X 10.9', 'iOS 11.1.1', 'Windows Vista', 'iOS 10.3.2', 'iOS 11.0.2', 'Mac OS X 10.11', 'Android 8.0.0', 'iOS 10.2.0', 'iOS 10.2.1', 'iOS 11.0.0', 'Mac OS X 10.10', 'Mac OS X 10_12_3', 'Mac OS X 10_12', 'Android 6.0.1', 'iOS', 'Mac OS X 10.13', 'Mac OS X 10_12_5', 'Mac OS X 10_8_5', 'iOS 11.0.1', 'iOS 10.0.2', 'Android 5.0.2', 'Windows XP', 'iOS 11.2.0', 'Mac OS X 10.6', 'Windows 8', 'Mac OS X 10_6_8', 'Mac OS X 10_11_4', 'Mac OS X 10_12_1', 'iOS 10.1.1', 'Mac OS X 10_11_3', 'Mac OS X 10_12_4', 'Mac OS X 10_13_2', 'Android 4.4.2', 'Mac OS X 10_12_2', 'Android 5.0', 'func', 'Android 7.1.2', 'Android 8.1.0', 'other', 'Mac OS X 10_13_3', 'iOS 11.2.1', 'iOS 11.2.5', 'Windows', 'iOS 11.2.2', 'iOS 11.3.0', 'iOS 11.2.6', 'Mac OS X 10_13_4', 'Mac OS X 10_13_5', 'iOS 11.4.0', 'iOS 11.3.1', 'iOS 11.4.1']
# agg Android X.X(.X) as android
# agg Windows X(.X) as windows
# agg iOS X.X.X as ios
# agg Mac OS X X_X_X as osx
def interpret_os_identifier(o_id):
    o_id = o_id.lower()
    if "android" in o_id:
        return "android"
    elif "windows" in o_id:
        return "windows"
    elif "ios" in o_id:
        return "ios"
    elif "mac os x" in o_id:
        return "osx"
    elif 'linux' in o_id:
        return "linux"
    elif o_id != '':
        return "other"
    return "unknown"


# ['samsung browser 6.2', 'mobile safari 11.0', 'chrome 62.0', '', 'chrome 62.0 for android', 'edge 15.0', 'mobile safari generic', 'chrome 49.0', 'chrome 61.0', 'edge 16.0', 'safari generic', 'edge 14.0', 'chrome 56.0 for android', 'firefox 57.0', 'chrome 54.0 for android', 'mobile safari uiwebview', 'chrome', 'chrome 62.0 for ios', 'firefox', 'chrome 60.0 for android', 'mobile safari 10.0', 'chrome 61.0 for android', 'ie 11.0 for desktop', 'ie 11.0 for tablet', 'mobile safari 9.0', 'chrome generic', 'other', 'chrome 59.0 for android', 'firefox 56.0', 'android webview 4.0', 'chrome 55.0', 'opera 49.0', 'ie', 'chrome 55.0 for android', 'firefox 52.0', 'chrome 57.0 for android', 'chrome 56.0', 'chrome 46.0 for android', 'chrome 58.0', 'firefox 48.0', 'chrome 59.0', 'samsung browser 4.0', 'edge 13.0', 'chrome 53.0 for android', 'chrome 58.0 for android', 'chrome 60.0', 'mobile safari 8.0', 'firefox generic', 'Generic/Android 7.0', 'mobile', 'Samsung/SM-G532M', 'chrome 50.0 for android', 'chrome 51.0 for android', 'chrome 63.0', 'chrome 52.0 for android', 'chrome 51.0', 'firefox 55.0', 'edge', 'opera', 'chrome generic for android', 'aol', 'samsung browser 5.4', 'Samsung/SCH', 'silk', 'chrome 57.0', 'firefox 47.0', 'chrome 63.0 for android', 'Samsung/SM-G531H', 'chrome 43.0 for android', 'waterfox', 'Nokia/Lumia', 'chrome 63.0 for ios', 'puffin', 'Microsoft/Windows', 'cyberfox', 'Generic/Android', 'samsung', 'opera generic', 'chrome 49.0 for android', 'ZTE/Blade', 'safari', 'android browser 4.0', 'samsung browser 5.2', 'palemoon', 'maxthon', 'line', 'LG/K-200', 'iron', 'BLU/Dash', 'seamonkey', 'firefox 58.0', 'chrome 64.0 for android', 'chrome 64.0', 'firefox 59.0', 'chrome 64.0 for ios', 'M4Tel/M4', 'comodo', 'Lanix/Ilium', 'samsung browser generic', 'chromium', 'opera 51.0', 'Inco/Minion', 'samsung browser 7.0', 'Mozilla/Firefox', 'samsung browser 4.2', 'samsung browser 6.4', 'chrome 65.0', 'chrome 65.0 for android', 'chrome 65.0 for ios', 'Cherry', 'icedragon', 'android', 'edge 17.0', 'chrome 66.0', 'chrome 66.0 for android', 'safari 11.0', 'safari 9.0', 'safari 10.0', 'google', 'chrome 66.0 for ios', 'google search application 48.0', 'opera 52.0', 'firefox 60.0', 'opera 53.0', 'samsung browser 3.3', 'google search application 49.0', 'facebook', 'firefox mobile 61.0', 'chrome 67.0', 'chrome 69.0', 'chrome 67.0 for android']
# -aggregating chrome XX.X for android to chrome for android
# -aggregating chrome XX.X to chrome
# -aggregating firefox XX.X to firefox
# -aggregating samsung browser X.X to samsung browser
# -aggregating chrome XX.X for ios to chrome for ios
# -aggregating safari XX.X to safari
# -aggregating opera XX.X to opera
# -aggregating google search application XX.X to google search application
# -aggregating mobile safari XX.X to mobile safari
# -aggregating edge XX.X as edge
# -aggregating ie XX.X for tablet as ie for tablet
# -aggregating ie XX.X for desktop as ie for desktop
def interpret_browser_identifier(b_id):
    if "chrome" in b_id:
        if "android" in b_id:
            return "chrome for android"
        elif "ios" in b_id:
            return "chrome for ios"
        else:
            return "chrome"
    elif "firefox" in b_id:
        return "firefox"
    elif "safari" in b_id:
        if "mobile" in "safari":
            return "mobile safari"
        else:
            return "safari"
    elif "ie" in b_id:
        if "desktop" in b_id:
            return "ie for desktop"
        else:
            return "ie for tablet"
    elif "edge" in b_id:
        return "edge"
    elif "opera" in b_id:
        return "opera"
    elif "samsung browser" in b_id:
        return "samsung browser"
    elif "google search application" in b_id:
        return "google search application"
    elif "android browser" in b_id:
        return "android browser"
    elif '' == b_id:
        return "unknown"
    else:
        return "other"
    

def interpret_device_info(d_inf):
    d_inf = d_inf.lower()
    if d_inf == '':
        return "unknown"
    for value in values.keys():
        if value in d_inf:
            return value
    else:
        return "other"

if __name__ == "__main__":
    os.chdir("data/")

    data = []

    with open("train_identity.csv", "r") as file:
        pfile = csv.reader(file)
        for row in pfile:
            data.append(row)

    # PROXY STATUS VALUES
    index = data[0].index("id_23")
    proxy_status_values = []

    for row in data[1:]:
        if row[index] not in proxy_status_values:
            proxy_status_values.append(row[index])

    # ['', 'IP_PROXY:TRANSPARENT', 'IP_PROXY:ANONYMOUS', 'IP_PROXY:HIDDEN']
    # using as [unknown, none, transparent, anon]


    # OS IDENTIFIERS
    index = data[0].index("id_30")
    os_identifiers = []

    for row in data[1:]:
        if row[index] not in os_identifiers:
            os_identifiers.append(row[index])


    os_identifiers_parsed = list(set([interpret_os_identifier(b_id) for b_id in os_identifiers]))
    # using as [unknown, other, ...]


    # BROWSER IDENTIFIERS
    index = data[0].index("id_31")
    browser_identifiers = []

    for row in data[1:]:
        if row[index] not in browser_identifiers:
            browser_identifiers.append(row[index])


    browser_identifiers_parsed = list(set([interpret_browser_identifier(b_id) for b_id in browser_identifiers]))
    # using as [unkown, other, ...]


    # DEVICE RESOLUTIONS
    index = data[0].index("id_33")
    device_resolutions = []

    for row in data[1:]:
        if row[index] not in device_resolutions:
            device_resolutions.append(row[index])

    # ['2220x1080', '1334x750', '', '1280x800', '1366x768', '1920x1080', '1680x1050', '1136x640', '5120x2880', '2880x1800', '1920x1200', '2560x1600', '2048x1536', '1024x768', '1280x720', '2560x1440', '2208x1242', '2001x1125', '1440x900', '1600x900', '2672x1440', '1280x1024', '960x540', '2732x2048', '2436x1125', '2048x1152', '2960x1440', '1024x600', '855x480', '4096x2304', '2160x1440', '2562x1442', '801x480', '2736x1824', '3441x1440', '2880x1620', '3840x2160', '1638x922', '1280x768', '1360x768', '1280x960', '3440x1440', '1152x720', '1280x1025', '3360x2100', '2304x1296', '1152x864', '3200x1800', '2112x1188', '2224x1668', '2400x1350', '2000x1125', '1600x1000', '2560x1080', '1728x972', '3000x2000', '1024x640', '3840x2400', '2304x1440', '1280x600', '1400x1050', '1600x1200', '3201x1800', '1356x900', '1344x756', '1624x1080', '1536x864', '1800x1125', '1920x1281', '2961x1442', '1366x1024', '1344x840', '3360x1890', '1536x1152', '1200x675', '1480x720', '2400x1600', '3200x2000', '1281x801', '960x640', '1776x1000', '2048x1280', '2049x1152', '1138x640', '2160x1215', '2880x1440', '0x0', '2520x1575', '5760x3240', '3843x2163', '1184x720', '1440x810', '2076x1080', '1600x837', '1093x615', '1281x721', '1152x648', '2392x1440', '2048x1080', '2735x1825', '1680x945', '1805x1015', '5760x1080', '2816x1584', '4500x3000', '1684x947', '1440x960', '1364x768', '3072x1728', '5040x3150', '7500x5000', '768x576', '1768x992', '1658x946', '1200x720', '1239x697', '1188x720', '1232x800', '1920x1280', '1264x924', '1400x900', '3240x2160', '2961x1440', '1422x889', '1848x1155', '3360x1050', '3840x1080', '2010x1080', '2160x1350', '1440x720', '1280x712', '1512x945', '1296x774', '1368x768', '3520x1980', '800x600', '1700x960', '2560x1800', '6400x3600', '2368x1440', '1824x1026', '1912x1025', '600x450', '3840x1600', '1760x990', '2700x1800', '1371x857', '1776x1080', '2552x1337', '3600x2250', '2560x1700', '2816x1760', '1440x800', '1440x803', '1920x1018', '6016x3384', '1280x620', '1281x720', '1720x1440', '1408x880', '640x360', '1920x975', '976x600', '1062x630', '2800x1575', '6720x3780', '1440x759', '1120x700', '1921x1081', '1280x1023', '1279x1023', '1441x901', '1679x1049', '1680x1051', '2220x1081', '1920x1079', '1919x1199', '1680x1049', '1365x768', '1919x1079', '1919x1200', '1919x1080', '1366x767', '1584x990', '2880x1442', '1281x800', '1229x691', '1600x1024', '1600x899', '1536x960', '1502x844', '1920x1201', '1439x809', '1408x792', '1279x1024', '1599x900', '1920x1081', '921x691', '3841x2161', '1921x1080', '480x320', '1888x941', '2049x1536', '2160x1439', '1707x960', '1024x767', '1365x767', '3001x2000', '3839x2160', '1916x901', '3838x2158', '1599x899', '3199x1800', '1511x944', '2737x1825', '2736x1823', '2735x1823', '2559x1439', '2400x1500', '2882x1442', '1729x973', '1727x971', '1023x767', '1918x1080', '1439x900', '4499x2999', '1280x740', '2999x2000', '1024x552', '1440x899', '2255x1503', '1025x768', '1280x732', '3839x2159', '3840x2162', '3696x2310', '2159x1439', '2256x1504', '1439x899', '2159x1440', '1359x768', '1092x614', '2048x1278', '2591x1619', '4200x2625', '2710x1440', '1272x960', '1023x768', '3838x2160', '2100x1312', '1360x767', '1024x819', '1502x845', '2561x1442', '2559x1440', '2160x1081', '1920x1279', '2160x1080', '1596x710', '1496x844', '1280x900']
    # using as [unknown, ...]


    # DEVICE TYPE
    index = data[0].index("DeviceType")
    device_types = []

    for row in data[1:]:
        if row[index] not in device_types:
            device_types.append(row[index])

    # ['mobile', 'desktop', '']
    # using as [unknown, ...]


    # DEVICE INFO
    index = data[0].index("DeviceInfo")
    device_infos = []

    for row in data[1:]:
        if row[index] not in device_infos:
            device_infos.append(row[index])

    # recognizing:
    values = {'windows':'windows', 'mac':'mac', 'ios':'ios', 'samsung':'samsung', 'moto':'moto', 'xt':'motoroka', 'nexus':'nexus', 'android':'android', 'lg':'lg', 'moto':'moto', 'huawei':'huawei', 'htc':'htc', 'pixel':'pixel', 'sm':'samsung', 'redmi':'redmi', 'lenovo':'lenovo', 'linux':'linux', 'ilium':'ilium', 'zte':'zte', 'z9':'z9', 'blade':'blade', 'lm':'lg'}


    dev_info_parsed = list(set([interpret_device_info(b_id) for b_id in device_infos]))

    datat = []
    with open("train_transaction.csv", "r") as file:
        pfile = csv.reader(file)
        ctr = 0
        for row in pfile:
            ctr += 1
            datat.append(row)
            if ctr>100000:
                break

    index = datat[0].index("P_emaildomain")
    email_domains = []

    for row in datat[1:]:
        if row[index] not in email_domains:
            email_domains.append(row[index])

    index = datat[0].index("R_emaildomain")

    for row in datat[1:]:
        if row[index] not in email_domains:
            email_domains.append(row[index])

    email_domains[0] = 'unknown'
    email_domains.append("other")
