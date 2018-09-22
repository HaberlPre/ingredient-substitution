# Place student names and ID numbers here:
# Tanja Gehr, 1861493
# Raphael Wagner, 1829214
# Lucas Haberl, 1862621
# Silvia Ivanova, 1817043



#%% 
import time
import mysql.connector as mysql
import numpy as np
np.set_printoptions(threshold=10000)


con = mysql.connect(user='allrecipes', #the user name for authentication
                    password='pressackgasse', #password of the user
                    host='132.199.138.79', # host name or IP address of the MySQL server
                    database='allrecipes') #name of the database

cur=con.cursor()

#%% 
#meal = "almond-butter"
#meal = "mommas-pasta-and-shrimp-salad"
#meal = "easy-beef-goulash"
#meal = "chicken-and-pumpkin-goulash"
meal = "almond-butter"
#meal = "pizza"


#%% komplett unnütz weil neuer parser

#def getParsedIng():
    #cur.execute("""SELECT `name_after_processing`, `new_ingredient_id` FROM `parsed_ingredients`
    #            WHERE `new_ingredient_id` > 0 ORDER BY `new_ingredient_id`""")
"""
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


#ta = np.asarray(["['0% fat greek yogurt' '1']", "['1 percent milk' '2']"]) #shortend array
#tb = []
#for i in range(len(ta)):
#    #print(i)
#    tc = ta[i].split("' '")
#    tc[0] = tc[0].replace("['", "")
#    tc[1] = tc[1].replace("']", "")
#    tb.append(tc)
#print(tb)
#np.save('parsedIngArray', tb)

parsedArray = np.load('parsedIngArray.npy')
#print(parsedArray[1000])
"""
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
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """
                    ORDER BY `who_score` DESC LIMIT 30""") #limit shortens it significantly, currently for ease of use; AND `number_of_ratings` > 10 raus
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
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """
                    ORDER BY `who_score` ASC LIMIT 30""") #limit shortens it significantly, currently for ease of use; AND `number_of_ratings` > 10 raus
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
                        WHERE `recipe_id` = """ + recIDStr + """ """)  #get the recipe who_score from feature_rable, wieso hier + statt % ?
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
        AIList=[]
        for i in range(len(recipes)):
            recipeID = recipes[i]
            cur.execute("""SELECT `i`.`ingredient_name` FROM `ingredients` `i` 
                        WHERE `i`.`recipe_id` = '%s' """ % recipeID + """ """)
            self.ing=np.array(cur.fetchall(), dtype=str)
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
        returnArray=[]
        who = whoIngName[0][0]
        for j in range(len(Ring)):
            for i in range(len(Ring[j])):
                try:        
                    ingName=Ring[j][i][0]
                    cur.execute("""SELECT  `new_ingredient_id` FROM `parsed_ingredients`
                        WHERE `original` LIKE '%s' """ % ingName + """
                        LIMIT 1""")
                    ingId=np.array(cur.fetchall(), dtype=str)
                    List=[]
                    List.append(ingId[0][0])
                    List.append(who)
                    returnArray.append(List)
                except:
                    pass
        return(returnArray)

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
            IngID = ingArray[i][0]
            if IngID != "None":
                IngID = int(IngID)
                cur.execute("""SELECT `p`.`aisle`, `p`.`name_after_processing` FROM `parsed_ingredients` `p` 
                            WHERE `p`.`new_ingredient_id` LIKE '%s' """ % IngID + """ 
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
            if ingArray[i][0] != "None":
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
    
    mealArray=[]
    for i in range(len(newWordArray)):
        recC = getTopRankedRecipes(newWordArray[i])
        rec = recC.outRec 
        #print(rec)
        ingFromRec = getWholeParsedIngList(rec, False)    
        mealArray.append(ingFromRec)
    
    return(mealArray)
    
def getCompArray(ingArrayList, mealIng): #return array vom gericht mit höchster bool übereinstimmung und rezept/name ing
    count = [0] * len(ingArrayList)
    for i in range(len(ingArrayList)):
        for j in range(len(mealIng)):
            if mealIng[j][0] == ingArrayList[i][0]: 
                count[i] += 1
    maxC = max(count) 
    for i in range(len(count)): #wenn man mehrmals vorkommt: letzter wert
        if count[i] == maxC:
            index = i       
            
    compareArray=[]
    compareArray.append(ingArrayList[index])
    compareArray.append(mealIng)
    return(compareArray)
     
     
#%%
def getWholeParsedIngList(recArray, sub): #macht nur einen index!
    if sub: #and len(recArray) < 20:
        out = getPosMealType()
        return(out)
    else:
        WhoArrayC = getRecWho(recArray)
        WhoArray = WhoArrayC.outRec
        
        ingFromArrayC = getIngredientsFromRecipes(recArray)
        ingFromArray = ingFromArrayC.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
        arrIngName=[] #eig unnötig
        for i in range(len(ingFromArray)):
            List = np.append(WhoArray[i], ingFromArray[i])
            arrIngName.append(List)
        
        t0 = time.time()
        parsedIngArrayC = getParsedIngIdFromGIFR(ingFromArray, parsedArray, arrIngName) #arrIngArray eig nur index 0 nötig (who score)
        parsedIngArray = parsedIngArrayC.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
        t1 = time.time()
        print(t1-t0)
        
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
topRankedSub = getWholeParsedIngList(topRankedRecipes, True) #true: ing zum substituten - rezept < 20, sucht gericht (pumpkin-gulash), ; gleich für gesund etc
topRankedRec = getWholeParsedIngList(topRankedRecipes, False)
compArray = getCompArray(topRankedSub, topRankedRec)
topRankeRecdMain = getMainFkt(topRankedRec)
topRankedRecRest = getRestFkt(topRankedRec)

healthyRec = getWholeParsedIngList(HealthyRecipes, False)
unhealthyRec = getWholeParsedIngList(NotHealthyRecipes, False)
