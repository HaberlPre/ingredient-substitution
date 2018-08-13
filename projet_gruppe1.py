# Place student names and ID numbers here:
# Tanja Gehr, 1861493
# Raphael Wagner, 1829214
# Lucas Haberl, 1862621
#Silvia Ivanova, 



import mysql.connector as mysql
import numpy as np
np.set_printoptions(threshold=10000)


con = mysql.connect(user='allrecipes', #the user name for authentication
                    password='pressackgasse', #password of the user
                    host='132.199.138.79', # host name or IP address of the MySQL server
                    database='allrecipes') #name of the database

cur=con.cursor()

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

#parsedArray = getParsedIng() #runtime horror
parsedArray = np.loadtxt("parsedIng.txt")
print(parsedArray)


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
        
#t1 = getTopRankedRecipes(meal)
#t11 = t1.outRec
#print(t11)

class getIngredientsFromRecipes():
    def __init__(self, recipes):
        AIList=["" for x in range(len(recipes))]
        for i in range(len(recipes)):
            recipeID = recipes[i]
            print(recipeID)
            #cur.execute("""SELECT `p`.`new_ingredient_id` FROM `parsed_ingredients` `p`, `ingredients` `i` 
            #            WHERE `i`.`recipe_id` = '%s' """ % recipeID + """ AND `i`.`id` = `p`.`id` """)
            cur.execute("""SELECT `i`.`ingredient_name` FROM `ingredients` `i` 
                        WHERE `i`.`recipe_id` = '%s' """ % recipeID + """ """)
            self.ing=np.array(cur.fetchall(),dtype=str)
            self.outIng=self.output(self.ing, i, AIList)
            print(self.ing)
            
    def output(self, ing, index, AIList):
        AIList[index] = AIList[index]+str(ing)
        
        return AIList
    
#t2 = getIngredientsFromRecipes(t11)
#t21 = t2.outIng
#print("sad")
#print(t21)
