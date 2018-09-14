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
#%% 
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
                    ORDER BY `f`.`avg_rating` DESC LIMIT 20""") #limit shortens it significantly, currently for ease of use
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
#print(bestWhoRec)
#%%
worstWho = getRecWho(NotHealthyRecipes)
worstWhoRec = worstWho.outRec #array with the who_scores of each recipe from the worst recipes
#print(worstWhoRec)
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
#print(ingHealthyRecipes)

arrBestWhoIngName=[]
for i in range(len(ingHealthyRecipes)):
    List = np.append(bestWhoRec[i], ingHealthyRecipes[i])
    arrBestWhoIngName.append(List)  
#print(arrBestWhoIngName)
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
    def __init__(self, Ring, Ping, arrBestWhoIngName):
        self.outArray = self.output(Ring, Ping, arrBestWhoIngName)
    
    def output(self, Ring, Ping, arrBestWhoIngName):
        outArray = []
        res=[]
        #print(arrBestWhoIngName[8][1:len(arrBestWhoIngName)])
        for i in range(len(arrBestWhoIngName)):
            for j in range(len(arrBestWhoIngName[i])-1):
                #print("j: "+str(j))
                for k in range(len(Ping)):
                    #print("k: "+str(k))
                    if str(Ping[k][0]) in arrBestWhoIngName[i][j+1] :
                        outArray.append(Ping[k][1])
                        #outArray.append(Ping[k][0])
                        outArray.append(arrBestWhoIngName[i][0])
        for m in range(0,len(outArray),2):
            res.append(outArray[m:2+m])
        return res
 #%% 
tparsedArray0 = time.time()
#%% 
parsedIngFromTopRecipesClass = getParsedIngIdFromGIFR(ingFromTopRecipes, parsedArray, arrTopRankedIngName)
parsedIngFromTopRecipes = parsedIngFromTopRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngFromTopRecipes)

#%%    
parsedIngHealthyRecipesClass = getParsedIngIdFromGIFR(ingHealthyRecipes, parsedArray, arrBestWhoIngName)
parsedIngHealthyRecipes = parsedIngHealthyRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngHealthyRecipes)
#%%    
parsedIngNotHealthyRecipesClass = getParsedIngIdFromGIFR(ingNotHealthyRecipes, parsedArray, arrWorstWhoIngName)
parsedIngNotHealthyRecipes = parsedIngNotHealthyRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngNotHealthyRecipes)

#%% 
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
                if outArray[i][0][0] == PA[j][0]: #uniqueIdArray[i][0] === ingr_id
                    
                    #print(outArray[i][0][0])  #outArray[i][1] === count
                    outArray[i][1] = outArray[i][1] + 1
            uniqueIdArray[i].append(str(outArray[i][1]))
        return uniqueIdArray
#%%
parsedIngCountFromTopRecipesClass = getParsedIngCount(parsedIngFromTopRecipes)
parsedIngCountFromTopRecipes = parsedIngCountFromTopRecipesClass.outArray #liste mit new ing id und häufigkeit
#print(parsedIngCountFromTopRecipes)
#%% 
parsedIngCountHealthyRecipesClass = getParsedIngCount(parsedIngHealthyRecipes)
parsedIngCountHealthyRec = parsedIngCountHealthyRecipesClass.outArray #liste mit new ing id und häufigkeit
#print((parsedIngCountHealthyRec))
#%% 
parsedIngCountNotHealthyRecipesClass = getParsedIngCount(parsedIngNotHealthyRecipes)
parsedIngCountNotHealthyRec = parsedIngCountNotHealthyRecipesClass.outArray #liste mit new ing id und häufigkeit
#print((parsedIngCountNotHealthyRec))
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
#%%
critValueTopRec = getCrit(parsedIngCountFromTopRecipes) #kritische zahl, ab wann ein ing main wird
MainTopIngClass = getMainIng(parsedIngCountFromTopRecipes, critValueTopRec)
MainTopIng = MainTopIngClass.outArray #format: liste mit new ing id, count
#print(MainTopIng)


#%% #kritische zahl, ab wann ein ing main wird
critValueHealthyRec = getCrit(parsedIngCountHealthyRec)
mainIngHealthyRecClass = getMainIng(parsedIngCountHealthyRec, critValueHealthyRec)
mainIngHealthyRec = mainIngHealthyRecClass.outArray
#print(mainIngHealthyRec)
#%% #kritische zahl, ab wann ein ing main wird
critValueNotHealthyRec = getCrit(parsedIngCountNotHealthyRec)
critNotHealthyRec = getCrit(parsedIngCountNotHealthyRec) #kritische zahl, ab wann ein ing main wird
mainIngNotHealthyRecClass = getMainIng(parsedIngCountNotHealthyRec, critValueNotHealthyRec)
mainIngNotHealthyRec = mainIngNotHealthyRecClass.outArray #format: liste mit new ing id, count
#print(mainIngNotHealthyRec)
#%% 
class getRestIng(): #unsortiert!!!
    def __init__(self, PAC, critBestRec):
        self.outArray = self.output(PAC, critBestRec)
    
    def output(self, PAC, critBestRec):
        outArray = []         
        for i in range(len(PAC)):
            if int(PAC[i][2]) < critBestRec:
                outArray.append(PAC[i])  
        return outArray
       
def getCrit(PAC):
    sum = 0
    for i in range(len(PAC)):
        sum = sum+int(PAC[i][2])
    critBestRec = sum/len(PAC)
    return round(2*critBestRec)
#%%
critValueTopRec = getCrit(parsedIngCountFromTopRecipes)
restIngTopRecClass = getRestIng(parsedIngCountFromTopRecipes, critValueTopRec)
restIngTopRec = restIngTopRecClass.outArray
#print(restIngTopRec)
#%%
#print(parsedIngCountHealthyRec[5][0][2])
critValueHealthyRec = getCrit(parsedIngCountHealthyRec) #kritische zahl, ab wann ein ing main wird
restIngHealthyRecClass = getRestIng(parsedIngCountHealthyRec, critValueHealthyRec)
restIngHealthyRec = restIngHealthyRecClass.outArray #format: liste mit new ing id, count
#print(restIngHealthyRec)

#%% 
critValueNotHealthyRec = getCrit(parsedIngCountNotHealthyRec) #kritische zahl, ab wann ein ing main wird
restIngNotHealthyRecClass = getRestIng(parsedIngCountNotHealthyRec, critValueNotHealthyRec)
restIngNotHealthyRec = restIngNotHealthyRecClass.outArray #format: liste mit new ing id, count
#print(restIngNotHealthyRec)
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
mainTopRankedAisleAndNameClass = addAisleAndName(MainTopIng)
mainTopRankedAisleAndName =sorted(mainTopRankedAisleAndNameClass.outIng, key = lambda x: int(x[2]))
print(mainTopRankedAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

restTopRankedAisleAndNameClass = addAisleAndName(restIngTopRec)
restTopRankedAisleAndName = sorted(restTopRankedAisleAndNameClass.outIng, key = lambda x: int(x[2]))
print(restTopRankedAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

mainHealthyAisleAndNameClass = addAisleAndName(mainIngHealthyRec)
mainHealthyAisleAndName = sorted(mainHealthyAisleAndNameClass.outIng, key = lambda x: int(x[2]))
print(mainHealthyAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

restHealthyAisleAndNameClass = addAisleAndName(restIngHealthyRec)
restHealthyAisleAndName = sorted(restHealthyAisleAndNameClass.outIng, key = lambda x: int(x[2]))
print(restHealthyAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

mainNotHealthyAisleAndNameClass = addAisleAndName(mainIngNotHealthyRec)
mainNotHealthyAisleAndName = sorted(mainNotHealthyAisleAndNameClass.outIng, key = lambda x: int(x[2]))
print(mainNotHealthyAisleAndName)
print("--------------------------------------------------------------------------------------------------------------")

restNotHealthyAisleAndNameClass = addAisleAndName(restIngNotHealthyRec)
restNotHealthyAisleAndName = sorted(restNotHealthyAisleAndNameClass.outIng, key = lambda x: int(x[2]))
print(restNotHealthyAisleAndName)
#%%
tstop = time.time()
print("--------full time:-----------")
print(tstop-t0)
print("------parsedArrayTime:-------")
print(tparsedArray1 - tparsedArray0)