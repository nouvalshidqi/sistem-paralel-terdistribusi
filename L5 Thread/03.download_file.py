#import os,requests, threading, urlib.request, urlib.error, urlib.parse, time
import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time

# Assign URL yang menuju kepada source download
url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"

#fungsi untuk membangun range byte dalam setiap thread
def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst

# class untuk split buffer kepada jumlah threads, secara konkuren download sesuai jumlah thread
class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    # fungsi untuk set thread dengan url dan ukuran bytes
    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None

    # request file sesuai dengan range byte
    # inisialisasi req class
    def run(self):
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})

    # fungsi untuk mendapat data file yang di download
    def getFileData(self):
        return urllib.request.urlopen(self.req).read()


def main(url=None, splitBy=3):
    # set variable untuk menyimpan waktu saat fungsi main dijalankan
    start_time = time.time()
    
    # cek apakah variabel url menyimpan nilai selain Null
    # jika url sama dengan Null, keluar dari fungsi main
    # jika url tidak sama dengan Null, lanjutkan fungsi main
    if not url:
        print("Please Enter some url to begin download.")
        return
    
    # parsing url dengan '/' sebagai batas untuk split
    fileName = url.split('/')[-1]
    
    # request header dari dari url untuk mendapatkan ukuran byte file
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    print("%s bytes to download." % sizeInBytes)
    
    # cek apakah variabel sizeInBytes menyimpan nilai selain Null
    # jika sizeInBytes sama dengan Null, keluar dari fungsi main
    # jika sizeInBytes tidak sama dengan Null, lanjutkan fungsi main
    if not sizeInBytes:
        print("Size cannot be determined.")
        return
    
    # set list kosong dengan nama dataLst
    dataLst = []
    
    #lakukan perulangan sampai batas 3 (splitBy = 3)
    for idx in range(splitBy):
        #menentukan range byte yang harus di download oleh sebuah thread dengan fungsi buildRange
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]
        
        # set buffer Thread dengan assign hasil dari fungsi SplitBufferThreads dengan url dan range byte yang di download
        bufTh = SplitBufferThreads(url, byteRange)
        
        #start buffer thread
        bufTh.start()
        
        # join hingga thread selesai
        bufTh.join()
        
        # append semua byte ke list dataLst
        dataLst.append(bufTh.getFileData())

    # join bytes dalam list dataLst
    content = b''.join(dataLst)

    if dataLst:
        
        # cek jika file sudah ada maka hapus file
        if os.path.exists(fileName):
            os.remove(fileName)
        # menampilkam jumlah waktu dari start hingga selesai
        print("--- %s seconds ---" % str(time.time() - start_time))
        
        # write file jika belum ada file
        with open(fileName, 'wb') as fh:
            fh.write(content)
        print("Finished Writing file %s" % fileName)

#run program dengan fungsi main
if __name__ == '__main__':
    main(url)