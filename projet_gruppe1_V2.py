# Place student names and ID numbers here:
# Tanja Gehr, 1861493
# Raphael Wagner, 1829214
# Lucas Haberl, 1862621
#Silvia Ivanova, 1817043



#%% 

import mysql.connector as mysql
import numpy as np
np.set_printoptions(threshold=10000)


con = mysql.connect(user='allrecipes', #the user name for authentication
                    password='pressackgasse', #password of the user
                    host='132.199.138.79', # host name or IP address of the MySQL server
                    database='allrecipes') #name of the database

cur=con.cursor()

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
class getRankedRecipes():
    def __init__(self, inputString):
        recipestring='%'+inputString+'%'
        cur.execute("""SELECT  `recipe_id` FROM `feature_table`
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """ AND `who_score` >= 3
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
rankedBestRecipesClass = getRankedRecipes(meal)
rankedBestRecipes = rankedBestRecipesClass.outRec #format: liste mit ids = links
#print(rankedBestRecipes)


#%% 
class getWorstRankedRecipes():
    def __init__(self, inputString):
        recipestring='%'+inputString+'%'
        cur.execute("""SELECT  `recipe_id` FROM `feature_table`
                    WHERE `recipe_id` LIKE '%s' """ % recipestring + """ AND `who_score` <= 3
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
worstRankedRecipesClass = getWorstRankedRecipes(meal)
worstRankedRecipes =  worstRankedRecipesClass.outRec #format: liste mit ids = links
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
bestFsa = getRecWho(rankedBestRecipes)
bestFsaRec = bestFsa.outRec #array with the who_scores of each recipe from the rankedBestRecipes
#print(bestFsaRec)

 
#%%
worstFsa = getRecWho(worstRankedRecipes)
worstFsaRec = worstFsa.outRec #array with the who_scores of each recipe from the rankedBestRecipes
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
ingFromBestRecipesClass = getIngredientsFromRecipes(rankedBestRecipes)
ingFromBestRecipes = ingFromBestRecipesClass.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
#print(ingFromBestRecipes)

arrBestWhoIngName=[]
for i in range(len(ingFromBestRecipes)):
    List = np.append(bestFsaRec[i], ingFromBestRecipes[i])
    arrBestWhoIngName.append([List])  
#print(arrBestWhoIngName)



#%%     
ingFromWorstRecipesClass = getIngredientsFromRecipes(worstRankedRecipes)
ingFromWorstRecipes = ingFromWorstRecipesClass.outIng #format: liste mit listen (ing für ein je ein rezept; nächstes rezept...)
#print(ingFromWorstRecipes)

arrWorstWhoIngName=[]
for i in range(len(ingFromWorstRecipes)):
    List = np.append(worstFsaRec[i], ingFromWorstRecipes[i])
    arrWorstWhoIngName.append([List])  
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
parsedingFromBestRecipesClass = getParsedIngIdFromGIFR(ingFromBestRecipes, parsedArray)
parsedingFromBestRecipes = parsedingFromBestRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedingFromBestRecipes)

arrBestWhoId=[]
for i in range(len(bestFsaRec)):
    List = np.append(bestFsaRec[i], parsedingFromBestRecipes[i])
    arrBestWhoId.append([List])  # [bestFsa ing_id]
#print(arrBestWhoId) 

 
#%%
parsedIngFromWorstRecipesClass = getParsedIngIdFromGIFR(ingFromWorstRecipes, parsedArray)
parsedIngFromWorstRecipes = parsedIngFromWorstRecipesClass.outArray #format: liste mit allen new ing id (parseding table) von obigen ing
#print(parsedIngFromWorstRecipes)

arrWorstWhoId=[]
for i in range(len(worstFsaRec)):
    List = np.append(worstFsaRec[i], parsedIngFromWorstRecipes[i])
    arrWorstWhoId.append([List])  # [bestFsa ing_id]
#print(arrWorstWhoId) 


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
parsedIngCountFromBestRecipesClass = getParsedIngCount(parsedingFromBestRecipes)
parsedIngCountBestRec = parsedIngCountFromBestRecipesClass.outArray #liste mit new ing id und häufigkeit
#print(parsedIngCountBestRec)

arrBestIdCountFsa=[]
for i in range(len(arrBestWhoIngName)):
    List = np.append(parsedIngCountBestRec[i], arrBestWhoIngName[i])
    arrBestIdCountFsa.append(List[0:3])  #get only the first 3 elements of the array, the rest are the ingredients of the recipe, which we do not need now
#print(arrBestIdCountFsa)


#%% 
parsedIngCountFromWorstRecipesClass = getParsedIngCount(parsedIngFromWorstRecipes)
parsedIngCountWorstRec = parsedIngCountFromWorstRecipesClass.outArray #liste mit new ing id und häufigkeit
#print(parsedIngCountBestRec)

arrWorstIdCountFsa=[]
for i in range(len(arrWorstWhoIngName)):
    List = np.append(parsedIngCountWorstRec[i], arrWorstWhoIngName[i])
    arrWorstIdCountFsa.append(List[0:3])  #get only the first 3 elements of the array, the rest are the ingredients of the recipe, which we do not need now
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
critBestRec = getCrit(parsedIngCountBestRec) #kritische zahl, ab wann ein ing main wird
MainIngBestRec = getMainIng(parsedIngCountBestRec, critBestRec)
MainBestIng = MainIngBestRec.outArray #format: liste mit new ing id, count
#print(MainBestIng[0])
arrBestIdCountFsa=[]
for i in range(len(ingFromBestRecipes)):
    List = np.append(parsedIngCountBestRec[i], arrBestWhoIngName[i][0][0])
    arrBestIdCountFsa.append([List])
#print(arrBestIdCountFsa)


#%% 
critWorstRec = getCrit(parsedIngCountWorstRec) #kritische zahl, ab wann ein ing main wird
worstMainIngClass = getMainIng(parsedIngCountWorstRec, critWorstRec)
worstMainIng = worstMainIngClass.outArray #format: liste mit new ing id, count
#print(worstMainIng[0])
arrWorstIdCountFsa=[]
for i in range(len(ingFromWorstRecipes)):
    List = np.append(parsedIngCountWorstRec[i], arrWorstWhoIngName[i][0][0])
    arrWorstIdCountFsa.append(List)


arrWorstIdCountFsaList = np.array(arrWorstIdCountFsa).tolist()
arrWorstIdCountFsa=sorted(arrWorstIdCountFsaList, key = lambda x: int(x[1]))
#print(arrWorstIdCountFsa)


#%% 
#gets the [ingr_id, ingr_probability] of the ing that are not in main ing
class getRestIng():
    def __init__(self, parsedIng, mainIng):
        self.outArray = self.output(parsedIng, mainIng)
    
    def output(self, parsedIng, mainIng):
        outArray = [] 
        boolContained = [s in mainIng for s in  parsedIng] #array with boolean values if some ing of the current recipe is in the main ing or not 
        #print(boolContained)
        for e in range(len(boolContained)):
            if not boolContained[e]: 
                outArray.append(parsedIng[e])
        return outArray
 
#%% 
restBestIngClass = getRestIng(parsedIngCountBestRec, arrBestIdCountFsa)
restBestIng = restBestIngClass.outArray
#print((restBestIng[1]))

arrBestIdCountFsa=[]
for i in range(len(restBestIng)):
    List = np.append(restBestIng[i], arrBestWhoIngName[0])
    arrBestIdCountFsa.append(List[0:3])
#print(arrBestIdCountFsa)
    
bestIngList = np.array(arrBestIdCountFsa).tolist()
print(bestIngList)

#%% 
restWorstIngClass = getRestIng(parsedIngCountWorstRec, arrWorstIdCountFsa)
worstMainIng = restWorstIngClass.outArray
#print(worstMainIng)


arrWorstIdCountFsa=[]
for i in range(len(worstMainIng)):
    List = np.append(worstMainIng[i], arrWorstWhoIngName[0])
    arrWorstIdCountFsa.append(List[0:3])
#print(arrWorstIdCountFsa)

worstIngList = np.array(arrWorstIdCountFsa).tolist()

print(worstIngList)