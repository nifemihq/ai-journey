library_data = "  janet adebayo #:#   the fire next time #:# non-fiction #:# 12/07/25  ,  OBINNA CHUKWU #:# purple hibiscus #:# fiction #:# 12/07/25 , aisha Bello#:# Children of Blood and Bone #:# Fantasy&Sci-Fi #:# 12/07/25,   thomas okon#:#deep work#:#non-fiction #:#12/07/25, MARYAM TAIWO#:#Think and Grow Rich#:#self-help #:#12/07/25 ,Tunde Cole #:#dune #:#Sci-Fi&Fantasy #:#12/07/25,  chioma Nwafor#:# Becoming #:#non-fiction #:# 12/07/25"

# print(f"""
# LIBRARY DATA: 
# {library_data}
# """)

clean = library_data.replace('#:#','|').split(',')
# print(clean)

clean = [[x.strip() for x in i.split('|')] for i in clean]
# print(clean)

clean = [[x.title() if x == i[0] or x == i[1] else x.lower() for x in i] for i in clean]
# print(clean)

genres_raw = [i[2].split('&') for i in clean]
# print(genres_raw)

genres = [x for i in genres_raw for x in i]
print(genres)

def count_genre(genres):
      non_fic = 0
      fic = 0
      fan = 0
      sci = 0
      self = 0
      for i in genres:
            if i == 'non-fiction':
                  non_fic += 1
            elif i == 'fiction':
                  fic += 1
            elif i == 'fantasy':
                  fan += 1
            elif i == 'sci-fi':
                  sci += 1
            elif i == 'self-help':
                  self += 1
      print(f"""
GENRE COUNT:

1) Non-fiction - {non_fic}
2) Fiction - {fic}
3) Fantasy - {fan}
4) Science-fiction - {sci}
5) Self-help - {self}
""")

count_genre(genres)

print(f"\n{clean}")

for i in clean:
      print(f"\n{i[0]} borrowed {i[1]} ({i[2]}) on {i[3]}.")