

file = r'C:\Users\YuLap\Downloads\output_decrypted.pptx'
with open(file, 'rb') as f, open('out.txt', 'w') as o:
    data = f.read()
    print(data)
    print(len(data))
    o.write(str(data))
#
# nulbits = 13
# file_with_0_b = r'C:\Users\YuLap\Downloads\output_decrypted.pptx'
# with open(file_with_0_b, 'rb') as with0:
#     data = with0.read()
#     for i in range(13):
#         data = data[:-1]
#
# with open(file_with_0_b, 'wb') as without0:
#     without0.write(data)

# file = r'C:\Users\YuLap\Downloads\Лекція 1. Вступ.pptx'
# with open(file, 'rb') as f, open('org.txt', 'w') as o:
#     data = f.read()
#     print(data)
#     print(len(data))
#     o.write(str(data))