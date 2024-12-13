'''PreProcessing functions to crop and padd 784 and 1568 hexa codes'''


def crop1568(l):
    ans=[]
    for i in range(len(l)):
        s=l[i]
        ans.append(s[:1568])
    return ans    


# def padd784(l):
#     l=crop784(l)
#     for i in range(len(l)):
#         if(len(l[i])!=784):
#             zeroes=784-len(l[i])
#             for j in range(zeroes+1):
#                 l[i]+="0"
#     return l



def padd1568(l):
    l=crop1568(l)
    for i in range(len(l)):
        if(len(l[i])!=1568):
            zeroes=1568-len(l[i])
            for j in range(zeroes+1):
                l[i]+="0"
        else:
            return l

def chunker(final,chunks):
    chunks=[]
    for i in range(0,len(final),len(final)//chunks):
        chunk=[]
        for j in range(i,i+len(final)//chunks):
            if(j>=len(final)):
                break
            else:
                chunk.append(final[j])
        if(chunk==[]):
            break
        else:
            chunks.append(chunk)
    return chunks