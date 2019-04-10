# tab
def packTab(t):
    return ';'.join(map(str, t))

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def parseTab(t):
    return map(num, t.split(';'))

# parse tab line
def parseTabWithName(line):
    name, tab = line.split('\t')
    if tab == '\n':
        return name, []
    tabT = map(float, tab.split(';'))
    return name, tabT



# peak
def packInterval(st, en):
    return str(st)+';'+str(en)

def parseInterval(s):
    return map(num, s.split(';'))

def packPeaks(sts, ws):
    ss = [packInterval(st+1, st+ws) for st in sts]
    return ' '.join(ss)

def parsePeaks(s):
    return map(parseInterval, s.split(' '))

def packPval(pval):
    return ' '.join(map(str, pval))

def parsePval(ps):
    return map(float, ps.split(' '))

def packTranscriptPeaks(ws, name, st, pval, times):
    if len(st) == 0:
        return ""
    return '\t'.join([name, packPeaks(st, ws), packPval(pval), packPval(times)]) + '\n'


def parseTranscriptPeaks(ps):
    name, peaks, pv, times = ps.split('\t')
    return name, parsePeaks(peaks), parsePval(pv.strip()), parsePval(times.strip())


def packIndividualPeak(name, st, en, pval, enrichScore, relEnrich):
    allFields=map(str, [name, st, en, pval, enrichScore, relEnrich])
    return '\t'.join(allFields)
if __name__ == "__main__":
	print "OK"
