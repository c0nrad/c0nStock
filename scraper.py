import urllib2
from debug import *
from random import randint

FAKE_DATA_MODE = False

symbolsList = ['MMM', 'ABT', 'ANF', 'ACE', 'ADBE', 'AMD', 'AES', 'AET', 'AFL', 'A', 'APD', 'AKAM', 'AA', 'ATI', 'AGN', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'ACAS', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AMGN', 'APC', 'ADI', 'BUD', 'APA', 'AIV', 'APOL', 'AAPL', 'ABI', 'AMAT', 'ADM', 'ASH', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVB', 'AVY', 'AVP', 'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BAX', 'BBT', 'BSC', 'BDX', 'BBBY', 'BMS', 'BBY', 'BIG', 'BIIB', 'HRB', 'BMC', 'BA', 'BXP', 'BSX', 'BMY', 'BRCM', 'BC', 'CHRW', 'CA', 'CPB', 'COF', 'CAH', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTX', 'CTL', 'SCHW', 'CHK', 'CVX', 'CB', 'CIEN', 'CI', 'CINF', 'CTAS', 'CSCO', 'CIT', 'C', 'CTXS', 'CCU', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CPWR', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'CVG', 'GLW', 'COST', 'CVH', 'COV', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DF', 'DE', 'DELL', 'DDR', 'DVN', 'DDS', 'DTV', 'DFS', 'D', 'RRD', 'DOV', 'DOW', 'DTE', 'DD', 'DUK', 'DYN', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EDS', 'EMC', 'EMR', 'ESV', 'ETR', 'EOG', 'EFX', 'EQR', 'EL', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FDO', 'FII', 'FDX', 'FIS', 'FITB', 'FHN', 'FE', 'FISV', 'FLR', 'F', 'FRX', 'BEN', 'FCX', 'GCI', 'GPS', 'GD', 'GE', 'GIS', 'GM', 'GGP', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOG', 'GWW', 'HAL', 'HOG', 'HAR', 'HIG', 'HAS', 'HNZ', 'HES', 'HPQ', 'HD', 'HON', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'IACI', 'ITW', 'IR', 'TEG', 'INTC', 'ICE', 'IBM', 'IFF', 'IGT', 'IP', 'IPG', 'INTU', 'ITT', 'JBL', 'JEC', 'JNS', 'JDSU', 'JNJ', 'JCI', 'JNY', 'JPM', 'JNPR', 'KBH', 'K', 'KEY', 'KMB', 'KIM', 'KLAC', 'KSS', 'KR', 'LLL', 'LH', 'LM', 'LEG', 'LEN', 'LUK', 'LXK', 'LLY', 'LTD', 'LNC', 'LLTC', 'LMT', 'LOW', 'LSI', 'MTB', 'M', 'MTW', 'MRO', 'MAR', 'MMC', 'MAS', 'MAT', 'MBI', 'MKC', 'MCD', 'MHP', 'MCK', 'MWV', 'MDT', 'WFR', 'MRK', 'MDP', 'MET', 'MTG', 'MCHP', 'MU', 'MSFT', 'MIL', 'MOLX', 'TAP', 'MON', 'MNST', 'MCO', 'MS', 'MUR', 'MYL', 'NBR', 'NOV', 'NSM', 'NTAP', 'NYT', 'NWL', 'NEM', 'GAS', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NUE', 'NVDA', 'NYX', 'OXY', 'ODP', 'OMX', 'OMC', 'ORCL', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'BTU', 'JCP', 'POM', 'PEP', 'PKI', 'PFE', 'PCG', 'PNW', 'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'QLGC', 'QCOM', 'DGX', 'STR', 'RSH', 'RTN', 'RF', 'RAI', 'RHI', 'ROK', 'COL', 'RDC', 'R', 'SWY', 'SNDK', 'SLB', 'SSP', 'SEE', 'SHLD', 'SRE', 'SHW', 'SIAL', 'SPG', 'SLM', 'SNA', 'SO', 'LUV', 'SE', 'S', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SYK', 'STI', 'SVU', 'SYMC', 'SNV', 'SYY', 'TROW', 'TGT', 'TE', 'TLAB', 'THC', 'TDC', 'TER', 'TEX', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TJX', 'TMK', 'RIG', 'TEL', 'TYC', 'TSN', 'USB', 'UNP', 'UIS', 'UNH', 'UPS', 'X', 'UTX', 'UNM', 'UST', 'VFC', 'VLO', 'VAR', 'VRSN', 'VZ', 'VNO', 'VMC', 'WMT', 'WAG', 'DIS', 'WM', 'WAT', 'WFT', 'WLP', 'WFC', 'WEN', 'WU', 'WY', 'WHR', 'WMB', 'WIN', 'WYN', 'XEL', 'XRX', 'XLNX', 'XL', 'YHOO', 'YUM', 'ZMH', 'ZION']     

def getStockData(symbolsList = symbolsList):  
    if FAKE_DATA_MODE:
        errorMessage("Using fake data mode")
        data = []
        for symbol in symbolsList:
            data.append ( (symbol, randint(50,55) ) )
        return data

    data = ""
    for x in range(0, len(symbolsList), 200):
        symbolGroup = "+".join(symbolsList[x:x+200])
        # name(n), symbol(s), the latest value(l1), open(o) close value(p)
        URL = "http://download.finance.yahoo.com/d/quotes.csv?s="+symbolGroup+"&f=sl1&e=.csv"
        data += urllib2.urlopen(URL).read()

    # Put data from ["\"AA\",3454"] -> [("AA", 34.3)]
    out = []
    for line in data.split("\n"):
        line = line.strip()
        if line == "": continue

        line = line.split(',')
        (symbol, value) = (line[0], line[1])
        out.append( (symbol.strip("\""), float(value) ) )
    return out

if __name__ == "__main__":
    data = getStockData()
    print data