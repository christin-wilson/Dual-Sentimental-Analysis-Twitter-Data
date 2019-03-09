
import csv
import os

hldv = ['Entry','Source','Positiv','Negativ','Pstv','Affil','Ngtv','Hostile','Strong','Power','Weak','Submit','Active','Passive','Pleasur','Pain','Feel','Arousal','EMOT','Virtue','Vice','Ovrst','Undrst','Academ','Doctrin','Econ@','Exch','ECON','Exprsv','Legal','Milit','Polit@','POLIT','Relig','Role','COLL','Work','Ritual','SocRel','Race','Kin@','MALE','Female','Nonadlt','HU','ANI','PLACE','Social','Region','Route','Aquatic','Land','Sky','Object','Tool','Food','Vehicle','BldgPt','ComnObj','NatObj','BodyPt','ComForm','COM','Say','Need','Goal','Try','Means','Persist','Complet','Fail','NatrPro','Begin','Vary','Increas','Decreas','Finish','Stay','Rise','Exert','Fetch','Travel','Fall','Think','Know','Causal','Ought','Perceiv','Compare','Eval@','EVAL','Solve','Abs@','ABS','Quality','Quan','NUMB','ORD','CARD','FREQ','DIST','Time@','TIME','Space','POS','DIM','Rel','COLOR','Self','Our','You','Name','Yes','No','Negate','Intrj','IAV','DAV','SV','IPadj','IndAdj','PowGain','PowLoss','PowEnds','PowAren','PowCon','PowCoop','PowAuPt','PowPt','PowDoct','PowAuth','PowOth','PowTot','RcEthic','RcRelig','RcGain','RcLoss','RcEnds','RcTot','RspGain','RspLoss','RspOth','RspTot','AffGain','AffLoss','AffPt','AffOth','AffTot','WltPt','WltTran','WltOth','WltTot','WlbGain','WlbLoss','WlbPhys','WlbPsyc','WlbPt','WlbTot','EnlGain','EnlLoss','EnlEnds','EnlPt','EnlOth','EnlTot','SklAsth','SklPt','SklOth','SklTot','TrnGain','TrnLoss','TranLw','MeansLw','EndsLw','ArenaLw','PtLw','Nation','Anomie','NegAff','PosAff','SureLw','If','NotLw','TimeSpc','FormLw','Othtags','Defined']


def display(row):
	cPos = 0
	cNeg = 0
	for i in row:
		if i in ['Positiv','Pstv'] :
			cPos += 1
		elif i in ['Negativ','Ngtv'] :
			cNeg += 1
	print "cNeg | cPos : ", cNeg, " | ", cPos

def processhd4(text):
	pwd = os.getcwd()
	csvfile = pwd+'/data/HIV-4.csv'

	text = text.upper()
	#text2=raw_input("compare with: ")
	#print re.search(text+"[^\s]+", text2)
	#print text > text2



	hivInput = csv.reader(open(csvfile, 'rU'))
	for row in hivInput:
		if text == row[0]:
			display(row)
			break	
		elif row[0].startswith( text ):
			display(row)
			print "\n"
			

text = raw_input("Enter the tweet : \n")
#print text

processhd4(text)