from z3 import *


def fewest_coins(coins, target):
    if target < 0:
        raise ValueError("There can't be negative change values")

    s = Solver()
    coin_var = []
    equation_1 = IntVal(0)
    equation_2 = IntVal(0)
    min_coins = Int("min_coins")

    # Check if the value is identical to one of the coins on the list
    for i in coins:
        if i == target:
            s.add(Int("Coin" + str(i)) == 1, Int("Coin" + str(i)) > 0)
            if s.check() == sat:
                return s.model()
            else:
                return None

    # Fill in the solver with the necessary constraints
    for i in range(len(coins)):
        coin_var.append(Int("Coin" + str(coins[i])))
        s.add(coin_var[i] >= 0)
        equation_1 += coins[i] * coin_var[i]
        equation_2 += coin_var[i]

    # Ensure big coins replace a collection of smaller coins during count
    for i in range(len(coins) - 1):
        if coins[i + 1] % coins[i] != 0:
            s.add(coin_var[i] < (coins[i + 1] // coins[i] + 1))
        else:
            s.add(coin_var[i] < (coins[i + 1] // coins[i]))

    s.add(equation_1 == target,
          equation_2 == min_coins,
          min_coins > 0,
          )

#    for i in range(target):
#        temp = s.__copy__()
#        temp.add(min_coins == i)
#        print(temp)

    print(s)
    if s.check() == sat:
        return s.model()

    return None



def find_fewest_coins(coins, target):
    if target < 0:
        raise ValueError("cannot find negative change values")
    min_coins_required = [1e9] * (target + 1)
    last_coin = [0]*(target + 1)
    min_coins_required[0] = 0
    last_coin[0] = -1
    for change in range(1, target + 1):
        final_result = min_coins_required[change]
        for coin in coins:
            if coin <= change:
                result = min_coins_required[change - coin] + 1
                if result < final_result:
                    final_result = result
                    last_coin[change] = change - coin
        min_coins_required[change] = final_result
    if min_coins_required[target] == 1e9:
        raise ValueError("no combination can add up to target")
    else:
        last_coin_value = target
        array = []
        while last_coin[last_coin_value] != -1:
            array.append(last_coin_value-last_coin[last_coin_value])
            last_coin_value = last_coin[last_coin_value]
        return array

if __name__ == "__main__":
    print(fewest_coins([1, 5, 10, 21, 25], 63))
    print(find_fewest_coins([1, 4, 15, 20, 50], 23))