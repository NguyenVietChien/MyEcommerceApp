

my_str = 'đồ chơi'

# 👇️ encode str to bytes
my_bytes = my_str.encode('utf-8', errors='ignore')
print(my_bytes)

# 👇️ decode bytes to str
my_str_again = my_bytes.decode('utf-8', errors='ignore')
print(str(my_str_again))  # 👉️ "hello 𝘈Ḇ𝖢𝕯٤ḞԍНǏ"
