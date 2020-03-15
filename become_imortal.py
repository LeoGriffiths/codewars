printMe = 1

def printGrid(row, col, rlen, clen):
    for r in xrange( int(row), int(row)+int(rlen) ):
        for c in xrange(int(col)+rpos,int(col)+int(clen)):
            print("{:03d} ".format(c^r), end="")
        print()


def countIt(row,col,rlen,clen,l,t):
        
    if printMe: print("countIt - row: {}, col: {}, rlen: {}, clen: {}, ".format( row,col, rlen, clen) )
    total=0
    rpos = 0
    for r in xrange( int(row), int(row)+int(rlen) ):
        i=0
        cpos = rpos
        for c in xrange(int(col)+rpos,int(col)+int(clen)):
            xor = (c^r)
            if xor > l:
                total += (xor - l)%t
                if rlen > cpos  and rpos!=cpos:
                    total += (xor - l)%t
            cpos+=1
        rpos+=1
    
    return total%t

def countLines(row, col, rlen, clen, l,t):
        
    start = (int(row)^int(col))
    start-= start%clen
    end = start+clen-1-l
    if end <= 0: return 0
    start -= l
    if start < 0: start = 0
    if printMe: print (" - start: {}, end: {}".format(start, end))
    
    diff = end - start
    segments = diff//t
    if printMe: print(" - diff: {}, segments: {}".format(diff, segments))
    seg, seg2, seg3 = 0,0,0
    
    if segments:
        seg = t*(t-1)/2
        if start%t != 0:
            # assume end is t-1
            if printMe: print(" - start%t=",start%t)
            seg2 = (t-start%t) * ( start%t + t-1) / 2
        if end%t != 0:
            # assume start is 0
            if printMe: print(" - end%t=", end%t)
            seg3 = (end%t+1) * (end%t) /2
        if (t - start%t) + end%t > t and start%t!=0:
            if printMe: print("!!!!!!!!!!!!! removing seg = ", (t - start%t) + end%t)
            segments-=1
    else:
        seg2 = (end+1-start) * (end + start) /2
        
    line = seg%t * segments%t + seg2%t + seg3%t

    s = (line%t  * (rlen%t) )%t
    
    if printMe: print(" - seg: {}, seg2: {}, seg3: {} \n   = line: {} ({})".format(seg, seg2, seg3, line, line%t))
    if printMe: print(" - line: {} * rlen: {} =  {} ({})".format(line, rlen, line*rlen, s ))
        
    return s
        


def calc_age(row, col, rlen ,clen, l, t, lvl):

    
    if printMe: print()
    if printMe: 
        print( "{}{} r={}, c={}".format(" "*lvl,lvl, row,col))
        print( "{}{} rlen={}, clen: {}".format(" "*lvl,lvl, rlen,clen))
    
    if rlen > clen:
        rlen, clen = clen, rlen
        row,col = col,row
        if printMe: print( "{} swap - r={}, c={}, rlen={}, clen: {}".format(" "*lvl, row,col,rlen,clen))

    if (rlen==clen and rlen%16==0):
        cl = countLines(row,col,rlen,clen,l,t)
        return cl
    
    if rlen <= 8 and clen <= 8:
        return countIt(row,col,rlen,clen,l,t)

    cnt = 16
    while cnt < clen:
        cnt*=2
    
    # if clen (long side) is a power of 2
    if clen==cnt:
#         if printMe: print("++++++++++ ccnt: {}".format(ccnt))
        cl = countLines(row,col,rlen,clen,l,t)
        return cl
    
    clong = cnt/2
    
    if clong > clen:
        clong = clen
    
    cnt = 16
    while cnt < rlen:
        cnt*=2
    rlong = cnt/2

    if rlong > rlen:
        rlong = rlen
    
        
    if printMe: print("{}rlong: {}, mod: {}".format(" "*lvl,rlong, rlong%16))
    if printMe: print("{}clong: {}, mod: {}".format(" "*lvl,clong, clong%16))
    
    total = 0
    
    sub = calc_age(row,col,rlong,clong,l,t,lvl+1)
    
    total += sub
    if printMe: print("{}FIRST total: {} ({})".format(" "*lvl,total, sub))  
    
    if rlen > rlong:
        sub = calc_age(row+rlong,col,rlen-rlong,clong,l,t,lvl+1)
        total += sub

        if printMe: print("{}ROWS total: {} ({})".format(" "*lvl,total, sub))
    
    if clen > clong:

        sub = calc_age(row,col+clong,rlen,clen-clong,l,t,lvl+1)
        total += sub

        if printMe: print("{}COLS total: {} ({})".format(" "*lvl,total, sub))

    return total


def elder_age(m,n,l,t):
    print( "m={}, n={}, l={}, t={}".format(m,n,l,t))
    print("test.assert_equals(elder_age({},{},{},{}), answer)".format(m,n,l,t))
    # set longer side to cols
    rows, cols = m, n
    if m > n:
        rows, cols = n, m
    
    total = calc_age(0,0,rows,cols,l,t,0)
    
    # printGrid(m,n,l,t)
    print ("total: {}, total%t: {}".format(total, total%t))

    return total%t