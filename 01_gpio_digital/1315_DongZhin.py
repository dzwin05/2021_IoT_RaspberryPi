print('값 2개를 입력하세요...')

a = input()
b = input()

print('연산을 입력하세요')
print('+는 1, -는 2, *는 3, /는 4')

x = int(input())

if x==1:
  pls = a+b
  print(pls)
elif x==2:
  print(a-b)
elif x==3:
  print(a*b)
elif x==4:
  print(a/b)
print('끝___')
print(a)