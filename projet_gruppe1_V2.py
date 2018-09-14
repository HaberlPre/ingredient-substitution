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
t0 = time.time()

meal = "pizza"

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
class getTopRankedRecipes():
    def __init__(self, inputString):
        recipestring='%'+inputString+'%'
        cur.execute("""SELECT  `f`.`recipe_id` FROM `feature_table` `f`
                    WHERE `f`.`recipe_id` LIKE '%s' """ % recipestring + """ AND `f`.`number_of_ratings` > 10
                    ORDER BY `f`.`avg_rating` DESC LIMIT 25""") #limit shortens it significantly, currently for ease of use
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
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """ AND `who_score` >= 3 AND `number_of_ratings` > 10
                    ORDER BY `who_score` DESC LIMIT 20""") #limit shortens it significantly, currently for ease of use
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
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """ AND `who_score` <= 3 AND `number_of_ratings` > 10
                    ORDER BY `who_score` ASC LIMIT 20""") #limit shortens it significantly, currently for ease of use 
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
topRankedWho = getRecWho(topRankedRecipes)
topRankedWhoRec = topRankedWho.outRec
#print(topRankedWhoRec)
    
#%%        
bestWho = getRecWho(HealthyRecipes)
bestWhoRec = bestWho.outRec #array with the who_scores of each recipe from the best recipes
#print(bestFsaRec)

 
#%%
worstWho = getRecWho(NotHealthyRecipes)
worstWhoRec = worstWho.outRec #array with the who_scores of each recipe from the worst recipes
#print(worstFsaRec)

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
ingFromTopRecipesClass = getIngredientsFromRecipes(topRankedRecipes)
ingFromTopRecipes = ingFromTopRecipesClass.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
#print(ingFromTopRecipes)

arrTopRankedIngName = []
for i in range(len(ingFromTopRecipes)):
    List = np.append(topRankedWhoRec[i], ingFromTopRecipes[i])
    arrTopRankedIngName.append(List)
#print(arrTopRankedIngName)
    
#%%     
ingHealthyRecipesClass = getIngredientsFromRecipes(HealthyRecipes)
ingHealthyRecipes = ingHealthyRecipesClass.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
#print(ingFromBestRecipes)

arrBestWhoIngName=[]
for i in range(len(ingHealthyRecipes)):
    List = np.append(bestWhoRec[i], ingHealthyRecipes[i])
    arrBestWhoIngName.append(List)  
#print(arrBestWhoIngName)
"""wird überschrieben"""


#%%     
ingNotHealthyRecipesClass = getIngredientsFromRecipes(NotHealthyRecipes)
ingNotHealthyRecipes = ingNotHealthyRecipesClass.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
#print(ingFromWorstRecipes)

arrWorstWhoIngName=[]
for i in range(len(ingNotHealthyRecipes)):
    List = np.append(worstWhoRec[i], ingNotHealthyRecipes[i])
    arrWorstWhoIngName.append(List)  
#print(arrWorstWhoIngName)


#%% 

class getParsedIngIdFromGIFR():
    def __init__(self, Ring, Ping):
        self.outArray = self.output(Ring, Ping)
    
    def output(self, Ring, Ping):
        outArray = []
        for i in range(len(Ring)):
            #print("i: "+str(i))
            for j in range(len(Ring[i])):
                #print("j: "+str(j))
                for k in range(len(Ping)):
                    #print("k: "+str(k))
                    if str(Ping[k][0]) in Ring[i][j]:
                        outArray.append(Ping[k][1])
        return outArray
 
#%% 
tparsedArray0 = time.time()
        
parsedIngFromTopRecipesClass = getParsedIngIdFromGIFR(ingFromTopRecipes, parsedArray)
parsedIngFromTopRecipes = parsedIngFromTopRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngFromTopRecipes)

arrTopRankedWhoId = []
for i in  range(len(topRankedWhoRec)):
    List = np.append(topRankedWhoRec[i], parsedIngFromTopRecipes[i])
    arrTopRankedWhoId.append(List)
#print(arrTopRankedWhoId)

#%%    
parsedIngHealthyRecipesClass = getParsedIngIdFromGIFR(ingHealthyRecipes, parsedArray)
parsedIngHealthyRecipes = parsedIngHealthyRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngFromBestRecipes)

arrBestWhoId=[]
for i in range(len(bestWhoRec)):
    List = np.append(bestWhoRec[i], parsedIngHealthyRecipes[i])
    arrBestWhoId.append(List)  # [bestFsa ing_id]
#print(arrBestWhoId) 
"""nutzen?"""
 
#%%
parsedIngNotHealthyRecipesClass = getParsedIngIdFromGIFR(ingNotHealthyRecipes, parsedArray)
parsedIngNotHealthyRecipes = parsedIngNotHealthyRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngFromWorstRecipes)

arrWorstWhoId=[]
for i in range(len(worstWhoRec)):
    List = np.append(worstWhoRec[i], parsedIngNotHealthyRecipes[i])
    arrWorstWhoId.append(List)  # [bestFsa ing_id]
#print(arrWorstWhoId) 

tparsedArray1 = time.time()

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
                if outArray[i][0] == PA[j]:
                    outArray[i][1] = outArray[i][1] + 1
        return outArray
    
#%%
parsedIngCountFromTopRecipesClass = getParsedIngCount(parsedIngFromTopRecipes)
parsedIngCountFromTopRecipes = parsedIngCountFromTopRecipesClass.outArray #liste mit new ing id und häufigkeit
#print(parsedIngCountFromTopRecipes)

arrTopRankedIdCountWho = []
for i in range(len(arrTopRankedIngName)):
    List = np.append(parsedIngCountFromTopRecipes[i], arrTopRankedIngName[i])
    arrTopRankedIdCountWho.append(List[0:3])
#print(arrTopRankedIdCountWho)
    
#%% 
"""alle healthy"""
parsedIngCountHealthyRecipesClass = getParsedIngCount(parsedIngHealthyRecipes)
parsedIngCountHealthyRec = parsedIngCountHealthyRecipesClass.outArray #liste mit new ing id und häufigkeit
#print(parsedIngCountBestRec)

arrBestIdCountWho=[]
for i in range(len(arrBestWhoIngName)):
    List = np.append(parsedIngCountHealthyRec[i], arrBestWhoIngName[i])
    arrBestIdCountWho.append(List[0:3])  #get only the first 3 elements of the array, the rest are the ingredients of the recipe, which we do not need now
#print(arrBestIdCountFsa)


#%% 
"""alle not healthy"""
parsedIngCountNotHealthyRecipesClass = getParsedIngCount(parsedIngNotHealthyRecipes)
parsedIngCountNotHealthyRec = parsedIngCountNotHealthyRecipesClass.outArray #liste mit new ing id und häufigkeit
#print(parsedIngCountBestRec)

arrWorstIdCountWho=[]
for i in range(len(arrWorstWhoIngName)):
    List = np.append(parsedIngCountNotHealthyRec[i], arrWorstWhoIngName[i])
    arrWorstIdCountWho.append(List[0:3])  #get only the first 3 elements of the array, the rest are the ingredients of the recipe, which we do not need now
#print(arrWorstIdCountFsa)


#%% 
class getMainIng(): #unsortiert!!!
    def __init__(self, PAC, critBestRec):
        self.outArray = self.output(PAC, critBestRec)
    
    def output(self, PAC, critBestRec):
        outArray = []         
        for i in range(len(PAC)):
            if int(PAC[i][1]) >= critBestRec:
                outArray.append(PAC[i])  
        return outArray
       
def getCrit(PAC):
    sum = 0
    for i in range(len(PAC)):
        sum = sum+PAC[i][1]
    critBestRec = sum/len(PAC)
    return round(2*critBestRec)

#%%
critTopRanked = getCrit(parsedIngCountFromTopRecipes) #kritische zahl, ab wann ein ing main wird
MainTopIngClass = getMainIng(parsedIngCountFromTopRecipes, critTopRanked)
MainTopIng = MainTopIngClass.outArray #format: liste mit new ing id, count
#print(MainTopIng)
arrTopIngCountWhoMain = []
for i in range(len(MainTopIng)):
    List = np.append(MainTopIng[i], arrTopRankedIngName[i][0][0])
    arrTopIngCountWhoMain.append(List)
#print(arrTopIngCountWhoMain)

arrTopIngCountWhoMainList = np.array(arrTopIngCountWhoMain).tolist()
#print(arrTopIngCountWhoMainList)

#%%  
""" healthy main """
critHealthyRec = getCrit(parsedIngCountHealthyRec) #kritische zahl, ab wann ein ing main wird
mainIngHealthyRecClass = getMainIng(parsedIngCountHealthyRec, critHealthyRec)
mainIngHealthyRec = mainIngHealthyRecClass.outArray #format: liste mit new ing id, count
#print(mainIngBestRec)
arrBestIdCountWhoMain=[]
for i in range(len(mainIngHealthyRec)):
    List = np.append(mainIngHealthyRec[i], arrBestWhoIngName[i][0][0])
    arrBestIdCountWhoMain.append(List)
#print(arrBestIdCountFsa)


arrBestIdCountWhoMainList = np.array(arrBestIdCountWhoMain).tolist()
#print(arrBestIdCountFsa)




#%% 
""" not healthy main """
critNotHealthyRec = getCrit(parsedIngCountNotHealthyRec) #kritische zahl, ab wann ein ing main wird
mainIngNotHealthyRecClass = getMainIng(parsedIngCountNotHealthyRec, critNotHealthyRec)
mainIngNotHealthyRec = mainIngHealthyRecClass.outArray #format: liste mit new ing id, count
#print(mainIngBestRec[0])
arrWorstIdCountWhoMain=[]
for i in range(len(mainIngNotHealthyRec)):
    List = np.append(mainIngNotHealthyRec[i], arrWorstWhoIngName[i][0][0])
    arrWorstIdCountWhoMain.append(List)


arrWorstIdCountWhoMainList = np.array(arrWorstIdCountWhoMain).tolist()
#arrWorstIdCountWho=sorted(arrWorstIdCountWhoList, key = lambda x: int(x[1]))
#print(arrWorstIdCountFsa)



#%% 
#gets the [ingr_id, ingr_probability] of the ing that are not in main ing
class getRestIng():
    def __init__(self, PAC, critBestRec):
        self.outArray = self.output(PAC, critBestRec)
    
    def output(self, PAC, critBestRec):
        outArray = []         
        for i in range(len(PAC)):
            if int(PAC[i][1]) < critBestRec:
                outArray.append(PAC[i])  
        return outArray
       
def getCrit(PAC):
    sum = 0
    for i in range(len(PAC)):
        sum = sum+PAC[i][1]
    critBestRec = sum/len(PAC)
    return round(2*critBestRec)

#%%
restIngTopRecClass = getRestIng(parsedIngCountFromTopRecipes, critTopRanked)
restIngTopRec = restIngTopRecClass.outArray
#print(restIngTopRec)

arrTopRankedIdCountWhoRest = []
for i in range(len(arrTopRankedIngName)):
    List = np.append(restIngTopRec[i], arrTopRankedIngName[i][0][0])
    arrTopRankedIdCountWhoRest.append(List)
    
arrTopRankedIdCountWhoRestList = np.array(arrTopRankedIdCountWhoRest).tolist()
#print(arrTopRankedIdCountWhoRest)

#%%
""" healthy rest """
#critHealthyRec = getCrit(parsedIngCountHealthyRec) #kritische zahl, ab wann ein ing main wird
restIngHealthyRecClass = getRestIng(parsedIngCountHealthyRec, critHealthyRec)
restIngHealthyRec = restIngHealthyRecClass.outArray #format: liste mit new ing id, count
#print(restIngBestRec)


arrBestIdCountWhoRest=[]
for i in range(len(arrBestWhoIngName)):
    List = np.append(restIngHealthyRec[i], arrBestWhoIngName[i][0][0])
    arrBestIdCountWhoRest.append(List)
#print(arrBestIdCountFsaRest)

arrBestIdCountWhoRestList = np.array(arrBestIdCountWhoRest).tolist()
#print(arrBestIdCountWhoRestList)


#%% 
""" not healthy rest """
#critWorstRecRest = getCrit(parsedIngCountNotHealthyRec) #kritische zahl, ab wann ein ing main wird
restIngNotHealhtyRecClass = getRestIng(parsedIngCountNotHealthyRec, critNotHealthyRec)
restIngNotHealthyRec = restIngNotHealhtyRecClass.outArray #format: liste mit new ing id, count

arrWorstIdCountWhoRest=[]
for i in range(len(arrWorstWhoIngName)):
    List = np.append(restIngNotHealthyRec[i], arrWorstWhoIngName[i][0][0])
    arrWorstIdCountWhoRest.append(List)
#print(arrWorstIdCountFsaRest)

arrWorstIdCountWhoRestList = np.array(arrWorstIdCountWhoRest).tolist() #ListRest
#arrWorstIdCountWhoRest=sorted(arrWorstIdCountWhoListRest, key = lambda x: int(x[1]))
#print(arrWorstIdCountWhoRestList)

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
mainTopRankedAisleAndNameClass = addAisleAndName(arrTopIngCountWhoMainList)
mainTopRankedAisleAndName = mainTopRankedAisleAndNameClass.outIng
print(mainTopRankedAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

restTopRankedAisleAndNameClass = addAisleAndName(arrTopRankedIdCountWhoRestList)
restTopRankedAisleAndName = restTopRankedAisleAndNameClass.outIng
print(restTopRankedAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

mainHealthyAisleAndNameClass = addAisleAndName(arrBestIdCountWhoMainList)
mainHealthyAisleAndName = mainHealthyAisleAndNameClass.outIng
print(mainHealthyAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

restHealthyAisleAndNameClass = addAisleAndName(arrBestIdCountWhoRestList)
restHealthyAisleAndName = restHealthyAisleAndNameClass.outIng
print(restHealthyAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

mainNotHealthyAisleAndNameClass = addAisleAndName(arrWorstIdCountWhoMainList)
mainNotHealthyAisleAndName = mainNotHealthyAisleAndNameClass.outIng
print(mainNotHealthyAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

restNotHealthyAisleAndNameClass = addAisleAndName(arrWorstIdCountWhoRestList)
restNotHealthyAisleAndName = restNotHealthyAisleAndNameClass.outIng
print(restNotHealthyAisleAndName)
#%%
tstop = time.time()
print("full time:")
print(tstop-t0)
print("parsedArrayTime:")
print(tparsedArray1 - tparsedArray0)
