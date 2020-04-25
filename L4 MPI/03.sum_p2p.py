# import mpi4py
from mpi4py import MPI

# import library random untuk generate angka integer secara random
import random

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# generate angka integer secara random untuk setiap proses
random_int = random.randint(1,7)

# jika saya adalah proses dengan rank 0 maka:
# saya menerima nilai dari proses 1 s.d proses dengan rank terbesar
# menjumlah semua nilai yang didapat (termasuk nilai proses saya)
if rank == 0:
    sum = random_int
    print("Nilai saya ",sum)
    for i in range(1,size):
        nilai = comm.recv(source=i)
        print("Mendapatkan Nilai",nilai,"dari Rank",i)
        sum += nilai
    print("NILAI TOTAL = ",sum)
	
# jika bukan proses dengan rank 0, saya akan mengirimkan nilai proses saya ke proses dengan rank=0
else:
    comm.send(random_int, dest=0)
    print("Mengirim Nilai",random_int,"untuk Rank 0")
	
