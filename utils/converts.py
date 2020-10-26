
def outputConvertRGB( y, i, q):
        # convertion values
        r_raw = y + 0.948262 * i + 0.624013 * q
        g_raw = y - 0.276066 * i - 0.639810 * q
        b_raw = y - 1.105450 * i + 1.729860 * q

        r_raw[r_raw < 0] = 0
        r_raw[r_raw > 1] = 1
        g_raw[g_raw < 0] = 0
        g_raw[g_raw > 1] = 1
        b_raw[b_raw < 0] = 0
        b_raw[b_raw > 1] = 1
        return (r_raw, g_raw, b_raw)