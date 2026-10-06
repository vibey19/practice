def find_calories(fruit):
    fruits = ['apple', 'avocado', 'banana', 'cantaloupe', 'grapefruit', 'grapes', 'honeydew melon', 'kiwifruit', 'lemon', 'lime', 'nectarine', 'orange','peach', 'pear', 'pineapple', 'plums', 'strawberries', 'sweet cherries', 'tangerine', 'watermelon']
    
    calorie_tab = [130, 50, 110, 50, 60, 90, 50, 90, 15, 20, 60, 80, 60, 100, 50, 70, 50, 100, 50, 80]
    
    calories = None
    for fruit_found,calories in zip(fruits,calorie_tab):
        if fruit_found == fruit:   
            return calories
    return ""

def main():
    fruit = input("Enter the fruit: ").lower()
    calories = find_calories(fruit)
    print(calories)
    
if __name__ == "__main__":
    main()