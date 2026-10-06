def main():
    
    amount_due = 50
    inserted_coins = 0
    
    while inserted_coins < 50:
        print(f"Amount Due: {amount_due}")
    
        coin = int(input("Insert Coin: "))

        if coin == 25 or coin == 10 or coin == 5:
            inserted_coins += coin
            amount_due = 50 - inserted_coins
            
        print(f"Change Owed: {50 - inserted_coins}")
    
if __name__ == "__main__":
    main()
    