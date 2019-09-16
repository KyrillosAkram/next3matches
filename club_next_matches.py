import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def fetch_results(search_term, number_results, language_code='en'):
	assert isinstance(search_term, str), 'Search term must be a string'
	assert isinstance(number_results, int), 'Number of results must be an integer'
	escaped_search_term = search_term.replace(' ', '+')
	google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
	response = requests.get(google_url, headers=USER_AGENT)
	response.raise_for_status()
	return search_term, response.text



online=True

#online=False
if online == True:
	club_name=input("Enter the club name\t:\t")
	print("\rgoogling ...",end='')
	keyword, html = fetch_results(club_name+' next match', 10, 'en')
	print("\rreading data ...",end='')
	bsoj=BeautifulSoup(html,'lxml')
else:
	#html=open("D:\\MyLab\\Space\\matchesFromGoogle\\ahly next smatch - Google Search.html")#windows
	html=open("/mnt/369071E49071AB4F/MyLab/Space/matchesFromGoogle/man_city.html")#linux
	bsoj=BeautifulSoup(html,"lxml")

#club position in his league
try:
	club_position=bsoj.find("span",{"class":"mKwiob imso-ani"}).get_text()
except:
	club_position="not found"
#scraping the club names home and away from the main div
club_names_1=bsoj.findAll("div",{"class":"ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx"})
match1home=club_names_1[0].get_text()
match1away=club_names_1[1].get_text()

#scraping the club names home and away from the secondary divs
club_names_2_3=bsoj.findAll("div",{"class":"ellipsisize kno-fb-ctx"})
match2home=club_names_2_3[0].get_text()
match2away=club_names_2_3[1].get_text()
match3home=club_names_2_3[2].get_text()
match3away=club_names_2_3[3].get_text()

#scraping the next match info ,date and time
info=bsoj.findAll("span",{"class":"imso-ln"})
match1info=info[0].get_text()

try:
	match1info=match1info+' '+ bsoj.findAll("div",{"class":"imso_mh__s-t-c"})[0].get_text()

except:
	pass

match1datetime=bsoj.findAll("span",{"class":"imso_mh__lr-dt-ds"})[0].get_text()

match1={					#storing match details
	"home":match1home,
	"away":match1away,
	"info":match1info,
	"date":match1datetime
	}

#scraping the next next matches info ,date and time
####for match 2
match2code=bsoj.find("td",{"class":"liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-right-border"})
try:
	match2info=match2code.find("div",{"class":"imspo_mt__lg-st-co"}).get_text()
except:
	match2info="not found"
match2date=match2code.find("div",{"class":"imspo_mt__pm-inf imspo_mt__date imso-medium-font"}).get_text()
match2date=match2date+"  "+match2code.find("div",{"class":"imspo_mt__ndl-p imspo_mt__pm-inf imso-medium-font"}).get_text()

match2={					#storing match details
	"home":match2home,
	"away":match2away,
	"info":match2info,
	"date":match2date
	}


####for match 3
match3code=bsoj.find("td",{"class":"liveresults-sports-immersive__match-tile imso-hov"})
try:
	match3info=match3code.find("div",{"class":"imspo_mt__lg-st-co"}).get_text()
except:
	match3info="not found"
match3date=match3code.find("div",{"class":"imspo_mt__pm-inf imspo_mt__date imso-medium-font"}).get_text()
match3date=match3date+"  "+match3code.find("div",{"class":"imspo_mt__ndl-p imspo_mt__pm-inf imso-medium-font"}).get_text()

match3={					#storing match details
	"home":match3home,
	"away":match3away,
	"info":match3info,
	"date":match3date
	}
matches=[match1,match2,match3]
spaces="  "
print("\r                                   \n\n%s\n"%(club_position))
for match in matches:
	print("+--------------------------------------------------------------------------------------+")
	print("|      [ Home ]    %20s    VS    %-20s    [ Away ]      |"%(match["home"],match["away"]))
	print("|%86s|"%(spaces))
	print("| Info :\t%-71s|"%(match["info"]))
	print("| Date :\t%-71s|"%(match["date"]))
	print("+--------------------------------------------------------------------------------------+\n")