# Place student names and ID numbers here:
# Tanja Gehr, 1861493
# Raphael Wagner, 1829214
# Lucas Haberl, 1862621
# Silvia Ivanova, 1817043



#%% 
import time
import mysql.connector as mysql
import numpy as np
from scipy import spatial
from itertools import groupby
from difflib import SequenceMatcher
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
meal = "chicken-and-pumpkin-goulash"
#meal = "pizza"
wordArray = []

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
             "yourself", "yourselves"]
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
            
    def output(self, ing, AIList):
        AIList.append(ing)
        
        return AIList

#%% 
class getParsedIngIdFromGIFR(): #hier früher parsedArray
    def __init__(self, Ring, whoIngName):
        self.outArray = self.output(Ring, whoIngName)
    
    def output(self, Ring, whoIngName):
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
            
    def output(self, data, ingArray, i):
        aisle, name = data.split("', '")
        aisle = aisle.replace("[['", "")
        name = name.replace("']]", "")
        ingArray[i].append(aisle)
        ingArray[i].append(name)
        return ingArray
        
#%%
class removeSpices():
    def __init__(self, ingArray, appendSpicesInNewArray = False):
        self.outArray = self.output(ingArray, appendSpicesInNewArray)
        
    def output(self, ingArray, appendSpicesInNewArray):
        outArray = []
        noSpices = []
        spices = []
        for i in range(len(ingArray)):
            if ingArray[i][0] != "None":
                if "Spices and Seasonings" not in ingArray[i][3]:
                    noSpices.append(ingArray[i])
                else:
                    spices.append(ingArray[i])
        if not appendSpicesInNewArray:
            outArray.extend(noSpices)
        else:
            outArray.append(noSpices)
            outArray.append(spices)
        return outArray
    
#%%
def getPosMealType():
    orgWordArray = meal.split("-")
    newWordArray=[]
    for i in range(len(orgWordArray)):
        if orgWordArray[i] not in stopwords:
            newWordArray.append(orgWordArray[i])
    
    global wordArray
    wordArray = newWordArray
    
    mealArray=[]
    for i in range(len(newWordArray)):
        recC = getTopRankedRecipes(newWordArray[i]) #evtl andere query
        rec = recC.outRec 
        ingFromRec = getWholeParsedIngList(rec, False)
        mealArray.append(ingFromRec)
    
    return(mealArray)
    
def getCompArray(ingArrayList, mealIng): #return array vom gericht mit höchster bool übereinstimmung und rezept/name ing
    count = [0] * len(ingArrayList)
    for i in range(len(ingArrayList)):
        for j in range(len(ingArrayList[i])):
            for k in range(len(mealIng)):
                if int(mealIng[k][0]) == int(ingArrayList[i][j][0]): 
                    count[i] += 1
        if count[i] != 0:
            count[i] = len(ingArrayList[i]) / count[i]
        else:
            count[i] = 100
    #print(count)
    maxC = min(count) #weil division: min = max übereinstimmung
    for i in range(len(count)): #wenn man mehrmals vorkommt: letzter wert
        if count[i] == maxC:
            index = i       
            
    compareArray=[]
    compareArray.append(ingArrayList[index])
    compareArray.append(mealIng)
    compareArray.append(wordArray[index])
    return(compareArray)
     
     
#%%
def getWholeParsedIngList(recArray, sub, mustRemoveSpices = True): #macht nur einen index!
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
        
        parsedIngArrayC = getParsedIngIdFromGIFR(ingFromArray, arrIngName) #arrIngArray eig nur index 0 nötig (who score)
        parsedIngArray = parsedIngArrayC.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
        
        parsedIngArrayCountC = getParsedIngCount(parsedIngArray)
        parsedIngArrayCount = parsedIngArrayCountC.outArray #liste mit new ing id und häufigkeit
        
        parsedIngAisleNameC = addAisleAndName(parsedIngArrayCount)
        parsedIngAisleName = sorted(parsedIngAisleNameC.outIng, key = lambda x: int(x[2]))
        
        if not mustRemoveSpices:
            return parsedIngAisleName
        
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
def getAvgWho(healthyRec, unhealthyRec): 
    
    if(len(unhealthyRec)>len(healthyRec)):
        for i in range(len(unhealthyRec)):
            for j in range(len(healthyRec)):
                if float(unhealthyRec[i][0]) == float(healthyRec[j][0]):
                    unhealthyRecWho = float(unhealthyRec[i][1])
                    healthyRecWho = float(healthyRec[j][1])
                    avgRecWho = (healthyRecWho + unhealthyRecWho)/2
                    unhealthyRec[i][1] = str(avgRecWho)
                    healthyRec[j][1] = str(avgRecWho)
    else:
        for i in range(len(healthyRec)):
            for j in range(len(unhealthyRec)):
                if float(unhealthyRec[i][0]) == float(healthyRec[j][0]):
                    unhealthyRecWho = float(unhealthyRec[i][1])
                    healthyRecWho = float(healthyRec[j][1])
                    avgRecWho = (healthyRecWho + unhealthyRecWho)/2
                    unhealthyRec[i][1] = str(avgRecWho)
                    healthyRec[j][1] = str(avgRecWho)
                    
#%%
class getRecWithHigherWHO():    
    def __init__(self, recString, recArray):
        RList=[]
        cur.execute("""SELECT `recipe_id` FROM `feature_table` WHERE `recipe_id` LIKE  '%""" + recString + """%' AND `who_score`> """+ recArray[0][1] +""" ORDER BY `who_score` DESC LIMIT 50""") #limit shortens it significantly, currently for ease of use; AND `number_of_ratings` > 10 raus
        self.recIds=np.array(cur.fetchall(), dtype=str)
        self.outIds=self.output(self.recIds, RList)
            
    def output(self, recIds, RList):
        for item in recIds:
            RList.append(item)
        
        return RList
    
#%%
def getMostSimilarRec(compareArray, startRec):
    recWithHigherWhoC = getRecWithHigherWHO(compareArray[2], startRec)#compareArray[2] = String des neuen Ingredient-Pools
    recWithHigherWho = recWithHigherWhoC.outIds    
    
    baseRecIng = startRec #ingredients des Ursprungsrezepts
    
    recIngWithHigherWho = [] #alle ing der rezepte mit höherer who als Ursprungsrezept
    for i in range(len(recWithHigherWho)):
        recIngWithHigherWho.append(getWholeParsedIngList(recWithHigherWho[i], False))
    
    allIngFromRec = []
    allIngFromRec.append(baseRecIng)
    allIngFromRec.extend(recIngWithHigherWho) #neues Array da dann richtig formatiert
            
    ingPool = compareArray[0] #alle Ingredients des neuen Ingredient-Pools
    
    vectorList = np.zeros((len(allIngFromRec),len(ingPool)))
    
    for i in range(len(allIngFromRec)):
        for j in range(len(allIngFromRec[i])):
            for k in range(len(ingPool)):
                if allIngFromRec[i][j][0] == ingPool[k][0]:
                    vectorList[i][k] = 1
    
    baseRecVector = vectorList[0]
    
    maxSimilarity = 0
    index = 0
    
    for i in range(len(vectorList[1:])):
        if np.any(vectorList[i+1]):
            similarity = 1 - spatial.distance.cosine(baseRecVector, vectorList[i+1])
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                index = i
    
    return(allIngFromRec[index+1])

#%%
def substituteWithRecipe(startingRecipe, recForSubstitution, strictSubstitution = False): #noch nicht fertig
    newRecipe = []
    stRec = startingRecipe
    subRec = recForSubstitution
    
    for stIng in stRec:
        for subIng in subRec[:]:
            if stIng[0] == subIng[0]:
                subRec.remove(subIng)
                
    stRec.sort(key=lambda x:x[3])
    subRec.sort(key=lambda x:x[3])
    
    stAisleGroups = []
    stAisleUniqueKeys = []
    subAisleGroups = []
    subAisleUniqueKeys = []
    for key, group in groupby(stRec, lambda x:x[3]):
        stAisleGroups.append(list(group))
        stAisleUniqueKeys.append(key)
    for key, group in groupby(subRec, lambda x:x[3]):
        subAisleGroups.append(list(group))
        subAisleUniqueKeys.append(key)
    
    
    for stPosition, stKey in enumerate(stAisleUniqueKeys[:]):
        for subPosition, subKey in enumerate(subAisleUniqueKeys):
            if stKey == subKey:
                thisAisle = compareIngLists(stAisleGroups[stPosition], subAisleGroups[subPosition], strictSubstitution)
                newRecipe.extend(thisAisle)
                stAisleUniqueKeys.remove(stKey)
    
    for key in stAisleUniqueKeys:
        for i in range(len(stAisleGroups)):
            if stAisleGroups[i][0][3] == key:
               for item in stAisleGroups[i]:
                   newRecipe.append(item)
    return newRecipe

def compareIngLists(stAisleIngs, subAisleIngs, strictSubstitution):
    comparedIngList = []
    if strictSubstitution:
        maxSimilarity = 0.6
    else:
        maxSimilarity = 0
    if len(stAisleIngs) <= len(subAisleIngs):
        for stIng in stAisleIngs:
            maxSimilarity
            index = -1
            
            for thisIndex, subIng in enumerate(subAisleIngs):
                thisSimilarity = compareStrings(stIng[4],subIng[4])
                if maxSimilarity < thisSimilarity < 1 and stIng[1] < subIng[1] and not similarToRecipeName(stIng[4]):
                    maxSimilarity = thisSimilarity
                    index = thisIndex
            if index == -1:
                comparedIngList.append(stIng)
            else:
                comparedIngList.append(subAisleIngs[index])
    else:
        for subIng in subAisleIngs:
            maxSimilarity
            index = -1
            for thisIndex, stIng in enumerate(stAisleIngs[:]):
                thisSimilarity = compareStrings(stIng[4],subIng[4])
                if maxSimilarity < thisSimilarity < 1 and stIng[1] < subIng[1] and not similarToRecipeName(stIng[4]):
                    maxSimilarity = thisSimilarity
                    index = thisIndex
            if index != -1:
                comparedIngList.append(subIng)
                del stAisleIngs[index]
        if all(isinstance(x, list) for x in stAisleIngs):
            comparedIngList.extend(stAisleIngs)
        else:
            comparedIngList.append(stAisleIngs)
    return comparedIngList

def compareStrings(a,b):
    return SequenceMatcher(None, a, b).ratio()

def similarToRecipeName(ingName):
    similarity = 0
    for partOfRecipe in wordArray:
        thisSimilarity = compareStrings(ingName,partOfRecipe)
        if thisSimilarity > similarity:
            similarity = thisSimilarity
    if similarity > 0.5:
        return True
    return False

#%%
completeStartRec = getWholeParsedIngList(topRankedRecipes[:1], False, False)
parsedIngNoSpiceC = removeSpices(completeStartRec, True)
completeStartRec = parsedIngNoSpiceC.outArray
startRec = completeStartRec[0]
topRankedSub = getWholeParsedIngList(topRankedRecipes, True) #true: ing zum substituten - rezept < 20, sucht gericht (pumpkin-gulash), ; gleich für gesund etc
topRankedRec = getWholeParsedIngList(topRankedRecipes, False)
compArray = getCompArray(topRankedSub, topRankedRec)
subRec = getMostSimilarRec(compArray, startRec)
substitutedWithRecipe = substituteWithRecipe(startRec, subRec)

recWithHigherWhoC = getRecWithHigherWHO(compArray[2], startRec)#compareArray[2] = String des neuen Ingredient-Pools
recWithHigherWho = recWithHigherWhoC.outIds

recWithHigherWhoList = []
for i in range(len(recWithHigherWho)):
    recWithHigherWhoList.append(recWithHigherWho[i][0])

recPool = getWholeParsedIngList(recWithHigherWhoList, False)

substitutedWithPool = substituteWithRecipe(substitutedWithRecipe, recPool, True)

if not (not completeStartRec[1]):
    startRec.extend(completeStartRec[1])
    substitutedWithRecipe.extend(completeStartRec[1])
    substitutedWithPool.extend(completeStartRec[1])
  
print("Startrezept: " + str(startRec))
print("Erste Sub: " + str(substitutedWithRecipe))
print("Zweite Sub: " + str(substitutedWithPool))

#%%
#healthy ing
#healthySub = getWholeParsedIngList(HealthyRecipes, True)
#healthyRec = getWholeParsedIngList(HealthyRecipes, False)
#compArray1 = getCompArray(healthySub, healthyRec)
#HealthyRecipesMain = getMainFkt(healthyRec)
#HealthyRecipesRest = getRestFkt(healthyRec)
#print(compArray1[0])
#unhealthy ing
#unhealthySub = getWholeParsedIngList(NotHealthyRecipes, True)
#unhealthyRec = getWholeParsedIngList(NotHealthyRecipes, False)
#compArray2 = getCompArray(unhealthySub, unhealthyRec)
#NotHealthyRecipesMain = getMainFkt(unhealthyRec)
#NotHealthyRecipesRest = getRestFkt(unhealthyRec)
#getAvgWho(HealthyRecipesRest, NotHealthyRecipesRest)
#print(HealthyRecipesRest)

#print("--------------Rest Healthy Ing-------------------")
#print(HealthyRecipesRest)
#print("-------------Rest Unhealthy Ing------------------")
#print(NotHealthyRecipesRest)
