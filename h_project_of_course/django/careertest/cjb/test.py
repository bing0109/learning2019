s = 'abadfsdf'
i = 0
r_s = s[:1]
while i < len(s):
    l_temp = list(s[i:i+1])
    if len(r_s) > len(s[i+1:]):
        break

    for j in s[i+1:]:
        if j not in l_temp:
            l_temp.append(j)
            print(l_temp,j)
        else:
            print(l_temp,j,'--')
            break

    if len(l_temp) > len(r_s):
        r_s = l_temp

    i += 1

print(len(r_s),r_s)

