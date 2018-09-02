# Place student names and ID numbers here:
# Tanja Gehr, 1861493
# Raphael Wagner, 1829214
# Lucas Haberl, 1862621
#Silvia Ivanova, 



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
    print(len(ing))
    parsedArray = []
    for i in range(len(ing)):
        print(i)
        if any(ing[i][1] in j for j in parsedArray):
            pass
        else:
            parsedArray.append(np.array2string(ing[i]))
    print(len(parsedArray))
    return parsedArray

#%% 
#parsedArray = getParsedIng() #runtime horror

"""
ta = np.asarray(["['0% fat greek yogurt' '1']", "['1 percent milk' '2']"]) #shortend array
tb = []
for i in range(len(ta)):
    print(i)
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
t1 = getTopRankedRecipes(meal)
t11 = t1.outRec
#print(t11)

#%% 
class getIngredientsFromRecipes():
    def __init__(self, recipes):
        #AIList=["" for x in range(len(recipes))]
        AIList=[]
        for i in range(len(recipes)):
            recipeID = recipes[i]
            print(recipeID)
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
t2 = getIngredientsFromRecipes(t11)
t21 = t2.outIng
#print("sad")
print(t21)

#%% 
class getGoodIngFromRecipes():
    def __init__(self, recipes):

        goodIng=[]
        a=False
        for i in range(len(recipes)):
            recipeID = recipes[i]
            
            cur.execute("""SELECT `i`.`ingredient_name` FROM `ingredients` `i` 
                        WHERE `i`.`recipe_id` = '%s' """ % recipeID + """ """)
            self.ingredients=np.array(cur.fetchall(),dtype=str)
           # print(self.ingredients[0][0])
            
            if "olive oil" in self.ingredients[0][0]: 
                a=True
            else:
                a=False
            
            if a:
               print()#self.ingredients[0][0]
               cur.execute("""SELECT `i`.`rank` FROM `distinct_parsed_ingredients` `i` 
                           WHERE `i`.`ingredient_name` = '%s' """ % self.ingredients[0][0] + """ """)
               self.scores=np.array(cur.fetchall())
               print(self.scores)
               
               self.resultIng=self.output(self.ingredients, self.scores, goodIng)
        
    def output(self, ingredients, scores, goodIng):
        
        #n=self.ingredients[0]
        goodIng.append(self.ingredients[0])
        #print(self.ingredients[0])
        return goodIng

#%%  

ti = getGoodIngFromRecipes(t11)
tin = ti.resultIng
#print("sad")
#print(tin)


#%%  

if "blah" in "lala blah aha": 
    print("true")
else:
    print("false")

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
t3 = getParsedIngIdFromGIFR(t21, parsedArray)
t31 = t3.outArray
#print(t31)

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

t4 = getParsedIngCount(t31)
t41 = t4.outArray
#print(t41)

#%% 
class getMainIng(): #unsortiert!!!
    def __init__(self, PAC, crit):
        self.outArray = self.output(PAC, crit)
    
    def output(self, PAC, crit):
        outArray = []         
        for i in range(len(PAC)):
            if int(PAC[i][1]) >= crit:
                outArray.append(PAC[i])    
        
        return outArray
       
def getCrit(PAC):
    sum = 0
    for i in range(len(PAC)):
        sum = sum+PAC[i][1]
    crit = sum/len(PAC)
    return round(2*crit)
    
crit = getCrit(t41)
t5 = getMainIng(t41, crit)
t51 = t5.outArray #[id, count]
print(t51)

#%% 
