bitmex_key = None
bitmex_secret = None

try:
    lines = [line.rstrip('\n') for line in open('.bitmex_keys')]
    bitmex_key = lines[0]
    bitmex_secret = lines[1]
except Exception as e:
    print("couldn't get api keys, does .bitmex_keys exist?")
