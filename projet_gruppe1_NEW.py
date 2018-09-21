# Place student names and ID numbers here:
# Tanja Gehr, 1861493
# Raphael Wagner, 1829214
# Lucas Haberl, 1862621
# Silvia Ivanova, 1817043



#%% 
#import time
import mysql.connector as mysql
import numpy as np
np.set_printoptions(threshold=10000)


con = mysql.connect(user='allrecipes', #the user name for authentication
                    password='pressackgasse', #password of the user
                    host='132.199.138.79', # host name or IP address of the MySQL server
                    database='allrecipes') #name of the database

cur=con.cursor()

#%% 
meal = "chicken-and-pumpkin-goulash"
#meal = "almond-butter"
#meal = "pizza"

#%%
def getParsedIng():
    cur.execute("""SELECT `name_after_processing`, `new_ingredient_id` FROM `parsed_ingredients`
                WHERE `new_ingredient_id` > 0 ORDER BY `new_ingredient_id`""")
    ing = np.array(cur.fetchall(),dtype=str)
    parsedArray = []
    for i in range(len(ing)):
        #print(i)
        if any(ing[i][1] in j for j in parsedArray):
            pass
        else:
            parsedArray.append(np.array2string(ing[i]))
    #print(len(parsedArray))
    return parsedArray

#%% 
#parsedArray = getParsedIng() #runtime horror

"""
ta = np.asarray(["['0% fat greek yogurt' '1']", "['1 percent milk' '2']"]) #shortend array
tb = []
for i in range(len(ta)):
    #print(i)
    tc = ta[i].split("' '")
    tc[0] = tc[0].replace("['", "")
    tc[1] = tc[1].replace("']", "")
    tb.append(tc)
#print(tb)
np.save('parsedIngArray', tb)
"""
parsedArray = np.load('parsedIngArray.npy')
#print(parsedArray[1000])

#%%
stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
             "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
             "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
             "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
             "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
             "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their",
             "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
             "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's",
             "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
             "yourself", "yourselves", "easy", "mommas"]
#stopwords from https://www.ranks.nl/stopwords

#%%
class getTopRankedRecipes():
    def __init__(self, inputString):
        recipestring='%'+inputString+'%'
        cur.execute("""SELECT  `f`.`recipe_id` FROM `feature_table` `f`
                    WHERE `f`.`recipe_id` LIKE '%s' """ % recipestring + """
                    ORDER BY `f`.`avg_rating` DESC LIMIT 30""") #limit shortens it significantly, currently for ease of use,  AND `f`.`number_of_ratings` > 10 raus, chrashte bei nur einem rezept
        self.rec=np.array(cur.fetchall(),dtype=str)
        self.outRec=self.output(self.rec)
        
    def output(self, rec):
        #print(ing)
        RList=[]
        for i in range(len(rec)):
            RList.append(np.array2string(rec[i]))
        for i in range(len(RList)):
            RList[i] = RList[i].replace("['", "")
            RList[i] = RList[i].replace("']", "")
        return RList
 
#%%        
topRankedRecipesClass = getTopRankedRecipes(meal)
topRankedRecipes = topRankedRecipesClass.outRec #format: liste mit ids = links
#print(topRankedRecipes)

#%% 
class getHealthyRecipes():
    def __init__(self, inputString):
        recipestring='%'+inputString+'%'
        cur.execute("""SELECT  `recipe_id` FROM `feature_table`
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """ AND `number_of_ratings` > 10
                    ORDER BY `who_score` DESC LIMIT 30""") #limit shortens it significantly, currently for ease of use
        self.rec=np.array(cur.fetchall(),dtype=str)
        self.outRec=self.output(self.rec)
        
    def output(self, rec):
        #print(ing)
        RList=[]
        for i in range(len(rec)):
            RList.append(np.array2string(rec[i]))
        for i in range(len(RList)):
            RList[i] = RList[i].replace("['", "")
            RList[i] = RList[i].replace("']", "")
        return RList
 
#%%        
HealthyRecipesClass = getHealthyRecipes(meal)
HealthyRecipes = HealthyRecipesClass.outRec #format: liste mit ids = links
#print(bestRankedRecipes)

#%% 
class getNotHealthyRecipes():
    def __init__(self, inputString):
        recipestring='%'+inputString+'%'
        cur.execute("""SELECT  `recipe_id` FROM `feature_table`
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """ AND `number_of_ratings` > 10
                    ORDER BY `who_score` ASC LIMIT 30""") #limit shortens it significantly, currently for ease of use 
        self.rec=np.array(cur.fetchall(),dtype=str)
        self.outRec=self.output(self.rec)
        
    def output(self, rec):
        #print(ing)
        RList=[]
        for i in range(len(rec)):
            RList.append(np.array2string(rec[i]))
        for i in range(len(RList)):
            RList[i] = RList[i].replace("['", "")
            RList[i] = RList[i].replace("']", "")
        return RList
 
#%%        
NotHealthyRecipesClass = getNotHealthyRecipes(meal)
NotHealthyRecipes = NotHealthyRecipesClass.outRec #format: liste mit ids = links
#print(worstRankedRecipes)


#%%
class getRecWho():
    def __init__(self, recID):
        RList=[]
        
        for i in range(len(recID)):
            recIDStr = ("'" + recID[i] + "'")
            recIDStr = recIDStr.replace("['", "")
            recIDStr = recIDStr.replace("']", "")
            cur.execute("""SELECT  `who_score` FROM `feature_table`
                        WHERE `recipe_id` = """ + recIDStr + """ """)  #get the recipe who_score from feature_rable
            self.rec=np.array(cur.fetchall(),dtype=str)
            RList.append(self.rec[0])
        self.outRec=self.output(RList)
        
    def output(self, rl):
        RList=[]
        for i in range(len(rl)):
            RList.append(rl[0])
        return RList

#%% 
class getIngredientsFromRecipes():
    def __init__(self, recipes):
        #AIList=["" for x in range(len(recipes))]
        AIList=[]
        for i in range(len(recipes)):
            recipeID = recipes[i]
            #print(recipeID)
            #cur.execute("""SELECT `p`.`new_ingredient_id` FROM `parsed_ingredients` `p`, `ingredients` `i` 
            #            WHERE `i`.`recipe_id` = '%s' """ % recipeID + """ AND `i`.`id` = `p`.`id` """)
            cur.execute("""SELECT `i`.`ingredient_name` FROM `ingredients` `i` 
                        WHERE `i`.`recipe_id` = '%s' """ % recipeID + """ """)
            self.ing=np.array(cur.fetchall(),dtype=str)
            self.outIng=self.output(self.ing, AIList)
            #print(self.ing)
            
    def output(self, ing, AIList):
        AIList.append(ing)
        
        return AIList

#%% 

class getParsedIngIdFromGIFR():
    def __init__(self, Ring, Ping, whoIngName):
        self.outArray = self.output(Ring, Ping, whoIngName)
    
    def output(self, Ring, Ping, whoIngName):
        outArray = []
        res=[]
        #print(arrBestWhoIngName[8][1:len(arrBestWhoIngName)])
        for i in range(len(whoIngName)):
            for j in range(len(whoIngName[i])-1):
                #print("j: "+str(j))
                for k in range(len(Ping)):
                    #print("k: "+str(k))
                    if str(Ping[k][0]) in [whoIngName[i][j+1]] :
                        outArray.append(Ping[k][1])
                        #outArray.append(Ping[k][0])
                        outArray.append(whoIngName[i][0])
        for m in range(0,len(outArray),2):
            res.append(outArray[m:2+m])
        return res

#%%
class getParsedIngCount():
    def __init__(self, PA):
        self.outArray = self.output(PA)
        
    def output(self, PA):
        uniqueIdArray  = []
        for i in range(len(PA)):
            if PA[i] not in uniqueIdArray:
                uniqueIdArray.append(PA[i])
                
        outArray = [[0 for x in range(2)] for y in range(len(uniqueIdArray))] 
        for i in range(len(outArray)):
            outArray[i][0] = uniqueIdArray[i]
            for j in range(len(PA)):
                if outArray[i][0][0] == PA[j][0]: #uniqueIdArray[i][0] === ingr_id
                    
                    #print(outArray[i][0][0])  #outArray[i][1] === count
                    outArray[i][1] = outArray[i][1] + 1
            uniqueIdArray[i].append(str(outArray[i][1]))
        return uniqueIdArray

#%% 
class getMainIng(): #unsortiert!!!
    def __init__(self, PAC, critBestRec):
        self.outArray = self.output(PAC, critBestRec)
    
    def output(self, PAC, critBestRec):
        outArray = []         
        for i in range(len(PAC)):
            if int(PAC[i][2]) >= critBestRec:
                outArray.append(PAC[i])  
        return outArray
       
def getCrit(PAC):
    sum = 0
    for i in range(len(PAC)):
        sum = sum+int(PAC[i][2])
    critBestRec = sum/len(PAC)
    return round(2*critBestRec)

class getRestIng(): #unsortiert!!!
    def __init__(self, PAC, critBestRec):
        self.outArray = self.output(PAC, critBestRec)
    
    def output(self, PAC, critBestRec):
        outArray = []         
        for i in range(len(PAC)):
            if int(PAC[i][2]) < critBestRec:
                outArray.append(PAC[i])  
        return outArray

#%% 
#adds aisle to ing array
"""output: new ing id, count, who score, aisle, name"""
class addAisleAndName():
    def __init__(self, ingArray): #nicht perfekt
        for i in range(len(ingArray)):
            IngID = int(ingArray[i][0])
            cur.execute("""SELECT `p`.`aisle`, `p`.`name_after_processing` FROM `parsed_ingredients` `p` 
                        WHERE `p`.`new_ingredient_id` = '%s' """ % IngID + """ 
                        LIMIT 1""")
            self.data = str(np.array(cur.fetchall(), dtype=str).tolist())
            self.outIng = self.output(self.data, ingArray, i)
            #print(self.data)
            
    def output(self, data, ingArray, i):
        aisle, name = data.split("', '")
        aisle = aisle.replace("[['", "")
        name = name.replace("']]", "")
        ingArray[i].append(aisle)
        ingArray[i].append(name)
        return ingArray
        
#%%
class removeSpices():
    def __init__(self, ingArray):
        self.outArray = self.output(ingArray)
        
    def output(self, ingArray):
        outArray = []
        for i in range(len(ingArray)):
            if "Spices and Seasonings" not in ingArray[i][3]:
                outArray.append(ingArray[i])
        return outArray
    
#%%
def getPosMealType():
    orgWordArray = meal.split("-")
    newWordArray=[]
    for i in range(len(orgWordArray)):
        if orgWordArray[i] not in stopwords:
            newWordArray.append(orgWordArray[i])                      
    
    ingArray=[]
    for i in range(len(newWordArray)):
        recC = getTopRankedRecipes(newWordArray[i]) #evtl abdere fkt als top ranked?
        rec = recC.outRec 
        ingFromRec = getWholeParsedIngList(rec, False)
        ingArray.append(ingFromRec)        
    
    return(ingArray)

#%%
def getWholeParsedIngList(recArray, sub):
    if len(recArray) < 20 and sub:
        out = getPosMealType()
        return(out)
    else:
        WhoArrayC = getRecWho(recArray)
        WhoArray = WhoArrayC.outRec
        
        ingFromArrayC = getIngredientsFromRecipes(recArray)
        ingFromArray = ingFromArrayC.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
        arrIngName=[]
        for i in range(len(ingFromArray)):
            List = np.append(WhoArray[i], ingFromArray[i])
            arrIngName.append(List)
            
        parsedIngArrayC = getParsedIngIdFromGIFR(ingFromArray, parsedArray, arrIngName)
        parsedIngArray = parsedIngArrayC.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
        
        parsedIngArrayCountC = getParsedIngCount(parsedIngArray)
        parsedIngArrayCount = parsedIngArrayCountC.outArray #liste mit new ing id und häufigkeit
        
        parsedIngAisleNameC = addAisleAndName(parsedIngArrayCount)
        parsedIngAisleName = sorted(parsedIngAisleNameC.outIng, key = lambda x: int(x[2]))
        
        parsedIngNoSpiceC = removeSpices(parsedIngAisleName)
        parsedIngNoSpice = parsedIngNoSpiceC.outArray
        
        return(parsedIngNoSpice)
    
def getMainFkt(ingArray):
    crit = getCrit(ingArray)
    mainIngC = getMainIng(ingArray, crit)
    mainIng = mainIngC.outArray #format: liste mit new ing id, count etc
    return(mainIng)

def getRestFkt(ingArray):
    crit = getCrit(ingArray)
    restIngC = getRestIng(ingArray, crit)
    restIng = restIngC.outArray #format: liste mit new ing id, count etc
    return(restIng)
    
#%%
topRanked = getWholeParsedIngList(topRankedRecipes, False) #true: ing zum substituten - rezept < 20, sucht gericht (pumpkin-gulash), ; gleich für gesund etc
#topRankedMain = getMainFkt(topRanked)
#topRankedRest = getRestFkt(topRanked)
