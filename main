# Changhong Wen
# Purpose: This is the updated Pet chooser assignment



import pymysql.cursors
import logging
from creds import username, password, hostname, database
from pets import Pets

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_pets(cursor) -> list:
    """Fetch all pets from the database and return a list of Pets objects."""
    sql_select = """
    SELECT
        pets.id,
        pets.name AS pet_name,
        pets.age,
        types.animal_type,
        owners.name AS owner_name
    FROM
        pets
    JOIN
        types ON pets.animal_type_id = types.id
    JOIN
        owners ON pets.owner_id = owners.id;
    """
    try:
        cursor.execute(sql_select)
        pets_list = [
            Pets(
                pet_id=row['id'],
                name=row['pet_name'],
                species=row['animal_type'],
                age=row['age'],
                owner=row['owner_name']
            )
            for row in cursor
        ]
        logging.info("Pet data fetched successfully.")
        return pets_list
    except Exception as e:
        logging.error("Error while fetching pet data", exc_info=True)
        return []


def display_pets(pets: list) -> None:
    """Display a list of pet names for selection."""
    if not pets:
        print("No pets available to display.")
        return

    print("\nPlease choose a pet from the list below:\n")
    for index, pet in enumerate(pets, start=1):
        print(f"[{index}] {pet.name}")
    print("\n[Q] Quit")


def get_user_choice() -> str:
    """Get user input and return the choice."""
    return input("\nChoice: ").strip()


def edit_pet(cursor, pet: Pets) -> None:
    """Edit pet's name and age."""
    print(f"\nYou have chosen to edit {pet.name}.\n")

    # Edit Name
    new_name = input("New name: [ENTER == no change] ").strip()
    if new_name.lower() == 'quit':
        print("Goodbye!")
        exit()
    if new_name:
        pet.name = new_name
        cursor.execute("UPDATE pets SET name = %s WHERE id = %s", (new_name, pet.pet_id))
        print("Pet name has been updated.")

    # Edit Age
    try:
        new_age = input("New age: [ENTER == no change] ").strip()
        if new_age.lower() == 'quit':
            print("Goodbye!")
            exit()
        if new_age:
            new_age = int(new_age)
            pet.age = new_age
            cursor.execute("UPDATE pets SET age = %s WHERE id = %s", (new_age, pet.pet_id))
            print("Pet age has been updated.")
    except ValueError:
        print("Invalid input for age. No changes made to age.")


def main():
    print("Starting the program...")

    # Connect to the database
    try:
        with pymysql.connect(
                host=hostname,
                user=username,
                password=password,
                db=database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
        ) as myConnection:
            logging.info("Successfully connected to the database.")

            # Fetch data and create pet objects
            while True:
                with myConnection.cursor() as cursor:
                    pets = fetch_pets(cursor)
                    if not pets:
                        print("No pets found in the database.")
                        return

                # Display pets and handle user selection
                while True:
                    display_pets(pets)
                    choice = get_user_choice()

                    if choice.lower() == 'q':
                        print("Goodbye!")
                        return

                    try:
                        choice_index = int(choice) - 1
                        if 0 <= choice_index < len(pets):
                            selected_pet = pets[choice_index]
                            print(f"\nYou have chosen {selected_pet}\n")
                            option = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet? ").strip().lower()

                            if option == 'q':
                                print("Goodbye!")
                                return
                            elif option == 'c':
                                break  # Go back to list of pets
                            elif option == 'e':
                                with myConnection.cursor() as cursor:
                                    edit_pet(cursor, selected_pet)
                                    myConnection.commit()
                                    print("Updates saved.")
                                    break  # After editing, go back to list of pets
                            else:
                                print("Invalid option. Please choose C, Q, or E.")
                        else:
                            print("\nInvalid choice. Please select a valid number from the list or 'Q' to quit.")
                    except ValueError:
                        print("\nInvalid choice. Please enter a number corresponding to a pet or 'Q' to quit.")
                    except Exception as e:
                        logging.error("Unexpected error during user selection", exc_info=True)

    except pymysql.MySQLError as e:
        logging.error("Database connection error", exc_info=True)
    except Exception as e:
        logging.error("An unexpected error occurred in the program", exc_info=True)
    finally:
        print("Program has ended.")


if __name__ == "__main__":
    main()
