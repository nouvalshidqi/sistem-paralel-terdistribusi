# import mpi4py
from mpi4py import MPI

# buat fungsi dekomposisi bernama local_loop 
# local_loop akan menghitung setiap bagiannya
# gunakan 4/(1+x^2), perhatikan batas awal dan akhir untuk dekomposisi
# misalkan size = 4 maka proses 0 menghitung 0-25, proses 1 menghitung 26-50, dst
def local_loop(num_steps,begin,end):
    step = 1.0/num_steps
    sum = 0
    # 4/(1+x^2)
    for i in range(begin,end):
        area = (i+0.5) * step
        sum = sum + 4.0 / (1.0 + area * area)
    print ("nilai sum : ", sum)
    return sum    

# fungsi Pi
def Pi(num_steps):
    
    # buat COMM
    comm = MPI.COMM_WORLD
    
    # dapatkan rank proses
    rank = comm.Get_rank()
    
    # dapatkan total proses berjalan
    size = comm.Get_size()
    
    # buat variabel baru yang merupakan num_steps/total proses
    variable = num_steps/size
    
    # cari local_sum
    # local_sum merupakan hasil dari memanggil fungsi local_loop
    local_sum = local_loop(num_steps, int(rank * variable), int((rank + 1) * variable))
    
    # lakukan penjumlahan dari local_sum proses-proses yang ada ke proses 0
    # bisa digunakan reduce atau p2p sum
    sum = comm.allreduce(local_sum,op=MPI.SUM)
    
    # jika saya proses dengan rank 0  maka tampilkan hasilnya
    if rank == 0:
        pi = sum / num_steps
        print ("nilai pi : ", pi)
    
# panggil fungsi utama    
if __name__ == '__main__':
    Pi(10000)
