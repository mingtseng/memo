import re
while True:
    str = input("请输入包含邮箱地址的字符串：")
    keyword = ["@", ".com"]
    cont = 0
    for key in keyword:
        if str.find(key) != -1:
            cont += 1
        else:
            break
    if cont == 2:
        def Get_emailadd(emailstr):
            result = re.findall(r'[a-z0-9\.\_-]+\@[a-z0-9\.\_-]+\.[a-z]+', emailstr)
            result = set(result)
            print("Email Address:  ", end="")
            ea = ";".join(result)
            print(ea)
            print("一共提取到{0:^3}个邮箱地址"
                  .format(ea.count("@")))
        Get_emailadd(str)
        break
    else:
        print("输入错误，请重新输入")
        continue



