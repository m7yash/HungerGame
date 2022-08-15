# <METADATA>
SOLUZION_VERSION = "0.0"
PROBLEM_NAME = "Hunger Crisis Simulation"
PROBLEM_VERSION = "0.0"
PROBLEM_AUTHORS = ['YASH MISHRA',
                   'JOSHUA CHOW' 'ASHWATH SRIKANTH', 'EDWARD ZHANG']
PROBLEM_CREATION_DATE = "10-SEPTEMBER-2021"

# </METADATA>

# <COMMON_DATA>

Costs = {
    'cashAssist': 100000,
    'gmoResearch':  1000000,
    'foodStorage': 250000,
    'farmerEducation': 250000,
    'landRestoration': 750000,
    'foodWasteAwareness': 50000,
    'doNothing': 0
}


BadEvents = [
    'flood',
    'wildfire',
    'pest',
    'hurricane'
]

"""
boosts: gmoResearch, foodStorage, farmerEducation, landRestoration, foodWasteAwareness
"""
boosts = [[0, 0], [0, 0], [0, 0], [0, 0], [
    0, 0]]  # [foodBoostQuantity, boostYear]

boost_message = ''
tk_message = ''

# </COMMON_DATA>

# <COMMON_CODE>


class State:

    def __init__(self, old=None):
        self.money = 2000000
        self.dead = 0
        self.np = 850000
        self.mmp = 100000
        self.smp = 50000
        self.year = 0
        self.food = 100000  # how many people can be fed
        self.militaryBudget = 4000000
        self.chooseBudget = False

        if not old is None:
            self.money = old.money
            self.dead = old.dead
            self.np = old.np
            self.mmp = old.mmp
            self.smp = old.smp
            self.year = old.year
            self.food = old.food
            self.militaryBudget = old.militaryBudget
            self.chooseBudget = old.chooseBudget

    def can_move(self, operatorType):
        if operatorType in ("moneyForHunger", "moneyForMilitary"):
            # it's time to choose the budget
            return self.year % 4 == 0 and not self.chooseBudget

        # if operatorType is one of the fundable initiatives:
        return self.money >= Costs[operatorType]

    def move(self, operatorType):
        global boosts
        global tk_message
        global boost_message

        tk_message = ''
        boost_message = ''

        news = State(old=self)  # Make a copy of the current state.

        if operatorType in ("cashAssist", "gmoResearch", "foodStorage", "farmerEducation", "foodWasteAwareness", "landRestoration", "doNothing"):
            news.year += 1
            news.chooseBudget = False

            print("===============")

            news.money -= Costs[operatorType]
            if operatorType == "cashAssist":
                news.food += 40000
                print("You fed 40,000 people through immediate cash assistance.\n")
            elif operatorType == "gmoResearch":
                boosts[0][0] += 500
                boosts[0][1] += 1
                print("You've invested in GMO research. The boost to your food supply every year will increase linearly. Investing in gmoResearch again will increase its boost.\n")
            elif operatorType == "foodStorage":
                boosts[1][0] += 4000
                boosts[1][1] += 1
                print("You've invested in better food storage. The boost to your food supply will be constant every year. Investing in foodStorage again will increase its boost.\n")
            elif operatorType == "farmerEducation":
                boosts[2][0] += 9000
                boosts[2][1] += 1
                print("You've invested in farmer education. The boost to your food supply will decrease every year. Investing in farmerEducation again will increase its boost.\n")
            elif operatorType == "landRestoration":
                boosts[3][0] += 10
                boosts[3][1] += 1
                print("You've invested in land restoration. The boost to your food supply will grow exponentially every year. Investing in landRestoration again will increase its boost.\n")
            elif operatorType == "foodWasteAwareness":
                boosts[4][0] += 1000
                boosts[4][1] += 1
                print("You've started a food waste awareness campaign. The boost to your food supply will be constant every year. Investing in food waste awareness again will increase its boost.\n")
            elif operatorType == "doNothing":
                print("You did nothing this year.")

            totalBoostForThisYear = 0

            # gmoResearch
            # If boosted once so far: 500 for year 1, 1,000 for year 2, 1,500 for year 3
            if boosts[0][1] != 0:
                add = boosts[0][0] * boosts[0][1]
                news.food += add
                boost_message += "  from gmoResearch: " + str(add) + " food\n"
                totalBoostForThisYear += add
                boosts[0][1] += 1

            # foodStorage
            # 4,000 per year if boosted once so far
            if boosts[1][1] != 0:
                add = boosts[1][0]
                news.food += add
                boost_message += "  from foodStorage: " + str(add) + " food\n"
                totalBoostForThisYear += add
                boosts[1][1] += 1

            # farmerEducation
            # If boosted once so far: 9000 for year 1, 4500 for year 2, 3000 for year 3, 360 for year 25, etc...
            if boosts[2][1] != 0:
                add = round(boosts[2][0] / boosts[2][1])
                news.food += add
                boost_message += "  from farmerEducation: " + \
                    str(add) + " food\n"
                totalBoostForThisYear += add
                boosts[2][1] += 1

            # landRestoration
            # If boosted once so far: 10 for year 1, 40 for year 2, 90 for year 3, 6250 for year 25, etc...this kind of encourages them to boost climate change multiple times for huge effects...
            if boosts[3][1] != 0:
                add = boosts[3][0] * (boosts[3][1] ** 2)
                news.food += add
                boost_message += "  from landRestoration: " + \
                    str(add) + " food\n"
                totalBoostForThisYear += add
                boosts[3][1] += 1

            # foodWasteAwareness
            # 1000 a year if boosted once so far
            if boosts[4][1] != 0:
                add = boosts[4][0]
                news.food += add
                boost_message += "  from foodWasteAwareness: " + \
                    str(add) + " food\n"
                totalBoostForThisYear += add
                boosts[4][1] += 1

            boost_message += f"  --Total boost for this year: {totalBoostForThisYear} food--"

            moveUp = news.smp if news.food >= news.smp else news.food
            news.smp -= moveUp
            news.food -= moveUp
            news.dead += news.smp
            news.smp = 0

            moveUp_mmp = news.mmp if news.food >= news.mmp else news.food
            news.np += moveUp_mmp
            news.mmp -= moveUp_mmp
            news.food -= moveUp_mmp
            news.smp += news.mmp

            news.mmp = 0

            news.mmp += moveUp

            print("{:,}".format(news.dead) + " people have died.")

        else:  # for budget proposal operators
            news.chooseBudget = True
            if operatorType == 'moneyForHunger':
                news.money += 1500000
            elif operatorType == 'moneyForMilitary':
                news.militaryBudget += 1500000

        print("===============")
        if news.year == 11:
            news.food += 5000
            tk_message = "Good News! An NGO has donated 5000 meals to your country!"
        if news.year % 7 == 0 and news.year != 0:
            tk_message = badEvent(news, news.year, "natural disaster")
        if news.year % 5 == 0 and news.year != 0 and news.year != 30:
            tk_message = badEvent(news, news.year, "war")

        return news

    def describe_state(self):
        # Produces a textual description of a state.
        # Produces a textual description of a state.
        txt = "\nNormal population: "+"{:,}".format(self.np)+"\n"
        txt += "Moderate Malnutrition population: " + \
            "{:,}".format(self.mmp)+"\n"
        txt += "Severe Malnutrition population: "+"{:,}".format(self.smp)+"\n"
        txt += "Death toll: "+"{:,}".format(self.dead)+"\n"
        txt += "Food Initiative Budget: "+"{:,}".format(self.money)+"\n"
        txt += "Military Budget: "+"{:,}".format(self.militaryBudget)+"\n"
        txt += "Food Supply (number of people that can be fed): " + \
            "{:,}".format(self.food)+"\n"
        txt += "Year: "+str(self.year + 2021)+"\n"

        if self.year % 4 == 0:
            txt += "BUDGET YEAR\n"

        txt += tk_message + '\n'

        return txt

    def is_goal(self):
        '''
        1. If dead >= 200,000 people: LOSE
        '''
        if self.dead >= 200000:
            return True
        '''
        2. If year == 30: WIN
        '''
        if self.year == 30:
            return True
        return False

    def __eq__(self, s2):
        if self.money != s2.money:
            return False
        if self.dead != s2.dead:
            return False
        if self.np != s2.np:
            return False
        if self.mmp != s2.mmp:
            return False
        if self.smp != s2.smp:
            return False
        if self.year != s2.year:
            return False
        if self.food != s2.food:
            return False
        if self.militaryBudget != s2.militaryBudget:
            return False
        if self.chooseBudget != s2.chooseBudget:
            return False
        return True

    def __str__(self):
        global boost_message
        global tk_message
        # Produces a textual description of a state.
        txt = "\nNormal population: "+"{:,}".format(int(self.np))+"\n"
        txt += "Moderate Malnutrition population: " + \
            "{:,}".format(self.mmp)+"\n"
        txt += "Severe Malnutrition population: "+"{:,}".format(self.smp)+"\n"
        txt += "Death toll: "+"{:,}".format(self.dead)+"\n"
        txt += "----------------------------\n"
        txt += "Food Initiative Budget: "+"{:,}".format(self.money)+"\n"
        txt += "Military Budget: "+"{:,}".format(self.militaryBudget)+"\n"
        txt += "----------------------------\n"
        txt += "Food Supply Remaining(number of people that can be fed): " + \
            "{:,}".format(self.food)+"\n"
        txt += boost_message + '\n'
        txt += "----------------------------\n"
        txt += f"Year: {self.year + 2021}. Years since start: {self.year}\n"
        txt += "Goal: 2051\n"

        if self.year % 4 == 0:
            txt += "BUDGET YEAR\n"

        txt += tk_message + '\n'

        if self.is_goal():
            txt += self.goal_message() + '\n'

        return txt

    def __hash__(self):
        return (str(self)).__hash__()

    def goal_message(self):
        if self.dead >= 200000:
            return f"YOU LOSE! {self.dead} people have died."
        else:
            return "YOU WIN! YOU MADE IT THROUGH THE 30 YEARS WITHOUT LOSING 200,000 PEOPLE."


def badEvent(newState, year, eventType) -> str:
    message = ''
    if eventType == "natural disaster":
        event = BadEvents[year//7 - 1]
        if event == 'flood':
            newState.food = int(newState.food * 0.7)
            return f"A flood has destroyed some of your crops! Only 70% of your food supply remains."
        elif event == 'wildfire':
            newState.food = int(newState.food * 0.7)
            return f"Wildfires have ravaged your country. Only 70% of your food supply remains."
        elif event == 'pest':
            newState.food = int(newState.food * 0.6)
            return f"Pests have infested many of your farms! Only 60% of your food supply remains."
        elif event == 'hurricane':
            newState.food = int(newState.food * 0.4)
            return f"A hurricane has swept through your city! Only 40% of your food supply remains."
    else:  # eventType == war
        opponentBudget = round(1e6 * year ** 0.5)
        if opponentBudget > newState.militaryBudget:

            message = f"Your opponent had a military budget of {opponentBudget} while you only had a military budget of {newState.militaryBudget}. You lost the war."
            newState.militaryBudget = 0
            message += f" Your military budget is now {newState.militaryBudget}."
            temp = round(0.20 * newState.np)
            newState.np -= temp
            newState.smp += temp
            message += f" 20% of your normal population has been moved down to severe malnutrition population."
            return message
        elif opponentBudget == newState.militaryBudget:

            message = f"Both you and your opponent had a military budget of {opponentBudget} so you were able to barely defend your country."
            newState.militaryBudget = 0
            message += f" Your military budget is now {newState.militaryBudget}."
            temp = round(0.05 * newState.np)
            newState.np -= temp
            newState.smp += temp
            message += f" 5% of your normal population has been moved down to severe malnutrition population."
            return message
        else:

            message = f"Your opponent only had a military budget of {opponentBudget} while you had a military budget of {newState.militaryBudget}. You won the war."
            newState.militaryBudget -= opponentBudget
            message += f" Your military budget is now the difference between the two budgets: ${newState.militaryBudget}."
            temp = round(0.03 * newState.np)
            newState.np -= temp
            newState.smp += temp
            message += f" 3% of your normal population has been moved down to severe malnutrition population."
            return message


def copy_state(s):
    return State(old=s)


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
# </COMMON_CODE>


# <INITIAL_STATE>
INITIAL_STATE = State()
# </INITIAL_STATE>

# <OPERATORS>
phi0 = Operator("Cash Based Assistance (Immediate one-time increase in food supply, COST: $100,000)",
                lambda s: s.can_move("cashAssist"),
                lambda s: s.move("cashAssist"))

phi1 = Operator("GMO Research (Food supply boost increases linearly every year, COST: $1,000,000)",
                lambda s: s.can_move("gmoResearch"),
                lambda s: s.move("gmoResearch"))

phi2 = Operator("Better Food Storage (Constant food supply boost every year, COST: $250,000)",
                lambda s: s.can_move("foodStorage"),
                lambda s: s.move("foodStorage"))

phi3 = Operator("Farmer Education (Food supply boost halves every year, COST: $500,000)",
                lambda s: s.can_move("farmerEducation"),
                lambda s: s.move("farmerEducation"))

phi4 = Operator("Land Restoration (Food supply boost grows exponentially every year, COST: $750,000)",
                lambda s: s.can_move("landRestoration"),
                lambda s: s.move("landRestoration"))

phi5 = Operator("Food Waste Awareness Campaign (Small constant food supply boost every year, COST: $50,000)",
                lambda s: s.can_move("foodWasteAwareness"),
                lambda s: s.move("foodWasteAwareness"))

phi6 = Operator("Do Nothing (The year will pass by, COST: $0)",
                lambda s: s.can_move("doNothing"),
                lambda s: s.move("doNothing"))

phi7 = Operator("Allocate money for the hunger initiatives (Increase the food initiative budget by $1,500,000)",
                lambda s: s.can_move("moneyForHunger"),
                lambda s: s.move("moneyForHunger"))

phi8 = Operator("Allocate money to the military (Increase the military budget by $1,500,000)",
                lambda s: s.can_move("moneyForMilitary"),
                lambda s: s.move("moneyForMilitary"))


OPERATORS = [phi0, phi1, phi2, phi3, phi4, phi5, phi6, phi7, phi8]
# </OPERATORS>

# <GOAL_MESSAGE_FUNCTION> (optional)


def GOAL_MESSAGE_FUNCTION(s): return s.goal_message()
# </GOAL_MESSAGE_FUNCTION>

# <STATE_VIS>

# </STATE_VIS>
