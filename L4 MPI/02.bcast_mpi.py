# import mpi4py
from mpi4py import MPI

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()


# jika saya rank 0 maka saya akan melakukan broadscast
if rank == 0:
    pesan = "aku rank 0 gaiz"
    

	
# jika saya bukan rank 0 maka saya menerima pesan
else:
    pesan = None
bc = comm.bcast(pesan, root=0)
print("Saya Rank",rank,"Menerima pesan broadcast '",bc,"' dari rank 0")
	