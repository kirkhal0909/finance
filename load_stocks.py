import datetime,os
from threading import Thread
from yahoo_fin import stock_info as si

arrow = '''  ||
  ||
__||__
\    /
 \  /
  \/'''

arrow = "\n".join(['\t\t\t\t'+line for line in arrow.split('\n')])
print(arrow) 

def getTime():
    return str(datetime.datetime.now())

def getPriceVolume(sym):
    table = si.get_quote_table(sym)
    return format(table['Quote Price'],'.2f'), table['Volume']

def appendToFile(fileName,text):
    file = open(fileName,'a')
    file.write(text+'\n')
    file.close()

def uploadStocksInfo(sym='yndx.me',doPrintStats=True):
    if doPrintStats:
        global arrow
    print('Process uploading stocks '+sym+' is start working\n')
    folder = 'stocks/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    file = folder+sym+'.txt'
    if not os.path.exists(file):
        appendToFile(file,'datetime\t'+'price\t'+'volume')
    lastPrice, lastVolume = 0,0
    high = True
    while True:
        #print(price,lastPrice)
        connected = False
        while not connected:
            try:
                price, volume = getPriceVolume(sym)
                connected = True
            except:
                print('Some error with getPrice()')
                connected = False
        
        if price != lastPrice:# or volume != lastVolume:
            out = getTime()+'\t'+str(price)+'\t'+str(volume)
            if doPrintStats:
                #print(price,type(price))
                checkPrice = float(price)
                checkLastPrice = float(lastPrice)
                if checkPrice<checkLastPrice and high:
                    high = False
                    #print('-------------------------------------------------')
                    print()
                elif checkPrice>checkLastPrice and not high:
                    high = True
                    #print(arrow)
                    print()
                print(out)
            appendToFile(file,out)
            lastPrice, lastVolume = price, volume

def threadUploader(sym):
    thread = Thread(target=uploadStocksInfo, args=(sym, False,))
    thread.start()

threadUploader('plzl.me')
uploadStocksInfo('yndx.me')
        
