h = input('Enter hex: ').lstrip('#')
rgb = list(int(h[i:i+2], 16) for i in (0, 2, 4))
[print(round(i/255*1000), end=", ") for i in rgb]