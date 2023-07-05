from datetime import datetime




if __name__ == '__main__':
    print("ola")
    ola = '2023-01-01'.replace('-','/')
    oladatetime = datetime.strptime(ola,'%Y/%m/%d')
    print(oladatetime)
