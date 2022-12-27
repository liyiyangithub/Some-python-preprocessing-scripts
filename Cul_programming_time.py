import time


start =time.time()
# your pragrama
sum=0
for i in range(1000000):
    sum=sum+i
#print(sum)

end=time.time()

print('Running time: %s Seconds'%(end-start))

