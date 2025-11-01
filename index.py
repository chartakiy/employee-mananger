# hw:
# department nomi jadval bor, uning title, id columnlari bor
# country jadvali bor, uning name, country_type bor
# employees jadvali bor, uning name, last_name, country, department, salary, email, phone numberi bor 
# 3 jadval uchun CRUD - create, read, update, delete
# managerda xodimlarni country va departmenti orqali search qilish imkoniyati

import psycopg2

class DataConnect:
  def __init__(self):
    self.connection = psycopg2.connect(
      dbname = 'n71__23_10',
      user = 'johnibek',
      password = '123john',
      host = 'localhost',
      port = 5433
    )
    self.cursor = self.connection.cursor()
    print("successfully connected to the database")

  # -----------------------------------------------------------------------------
  # ------------------------- code for department table -------------------------
  # -----------------------------------------------------------------------------
  def view_department(self):
    query = "SELECT department_id, department_name FROM department"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()

    if not rows:
      print("no department can be found")
    else:
      print("\n========= DEPARTMENTS =========")

      for department_id, department_name in rows:
        print(f"Department ID: {department_id}, Department Name: {department_name}")

    return rows

  def add_department(self, department_name):
    query = "INSERT INTO department(department_name) VALUES (%s)"
    self.cursor.execute(query, (department_name, ))
    self.connection.commit()
    print(f"Department {department_name} has been added successfully")
  
  def edit_department(self, info):
    departments = self.view_department()
    department_id, department_name = info

    if not departments:
      return
    
    try:
      new_department_name = input("New Department Name (or leave blank to keep current): ").strip()
      if not new_department_name:
        new_department_name = department_name

      query = "UPDATE department SET department_name=%s WHERE department_id=%s"
      self.cursor.execute(query, (new_department_name, department_id))
      self.connection.commit()
      print("Department updated successfully")
    except Exception as e:
      print(f"Error in edition: {e}")
  
  def delete_department(self, info):
    departments = self.view_department()
    department_id, department_name = info

    if not departments:
      return
    
    confirm = input(f"Are you sure you want to delete department '{department_name}' (y/n): ").lower().strip()
    if confirm != 'y':
        print("Deletion cancelled")
        return
    
    try:
      query = "DELETE FROM department WHERE department_id = %s"
      self.cursor.execute(query, (department_id, ))
      self.connection.commit()

      if self.cursor.rowcount > 0:
          print(f"Department '{department_name}' has been deleted.")
      else:
          print(f"No department found with ID {department_id}.")

    except psycopg2.IntegrityError:
      self.connection.rollback()
      print("Cannot delete this department because it is referenced by employees.")

    except Exception as e:
      print(f"Error happened while deletion: {e}")
  
  # -----------------------------------------------------------------------------
  # ------------------------- code for country table ----------------------------
  # -----------------------------------------------------------------------------
  def view_country(self):
    query = "SELECT country_id, country_name FROM country ORDER BY country_id"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()

    if not rows:
        print("No countries found.")
    else:
        print("\n========= COUNTRIES =========")
        for country_id, country_name in rows:
            print(f"Country ID: {country_id}, Country Name: {country_name}")
    return rows

  def add_country(self, country_name, country_type):
    query = "INSERT INTO country(country_name, country_type) VALUES (%s, %s)"
    self.cursor.execute(query, (country_name, country_type))
    self.connection.commit()
    print(f"Country {country_name} has been added successfully")
  
  def edit_country(self, country_id, country_name, country_type):
    countries = self.view_country()
    if not countries:
      return
    
    try:
      print(f"\nEditing country '{country_name}'")
      new_country_name = input("New Country Name (or leave blank to keep current): ").strip()
      if not new_country_name:
        new_country_name = country_name
      new_country_type = input("New Country Type (or leave blank to keep current): ").strip()
      if not new_country_type:
        new_country_type = country_type

      query = """
        UPDATE country 
        SET country_name = %s, country_type = %s
        WHERE country_id = %s
      """
      self.cursor.execute(query, (new_country_name, new_country_type, country_id))
      self.connection.commit()
      print("Country updated successfully")
    except Exception as e:
      print(f"Error in edition: {e}")
  
  def delete_country(self, country_id, country_name):
    countries = self.view_country()

    if not countries:
      return
    
    confirm = input(f"Are you sure you want to delete country '{country_name}' (y/n): ").lower().strip()
    if confirm != 'y':
        print("Deletion cancelled")
        return
    
    try:
      query = "DELETE FROM country WHERE country_id = %s"
      self.cursor.execute(query, (country_id, ))
      self.connection.commit()

      if self.cursor.rowcount > 0:
          print(f"Country '{country_name}' has been deleted.")
      else:
          print(f"No country found with ID {country_id}.")

    except psycopg2.IntegrityError:
      self.connection.rollback()
      print("Cannot delete this country because it is referenced by employees.")

    except Exception as e:
      print(f"Error happened while deletion: {e}")

  # -----------------------------------------------------------------------------
  # ------------------------- code for employees table --------------------------
  # -----------------------------------------------------------------------------
  def view_employees(self):
    query = """
      SELECT e.employee_id, e.employee_first_name, e.employee_last_name, c.country_name, d.department_name, e.salary, e.email, e.phone_number from employees e
      LEFT JOIN country c ON e.country_id = c.country_id
      LEFT JOIN department d ON e.department_id = d.department_id
      ORDER BY employee_id
    """
    self.cursor.execute(query)
    rows = self.cursor.fetchall()

    if not rows:
      print("no employee can be found")
    else:
      print("\n========= EMPLOYEES =========")

      for employee_id, employee_first_name, employee_last_name, country_name, department_name, salary, email, phone_number in rows:
        print(f"Employee ID: {employee_id}, Employee Name: {employee_first_name} {employee_last_name}, Country Name: {country_name}, Department Name: {department_name}, Salary: {salary}, Email: {email}, Phone Number: {phone_number}")

    return rows
  
  def add_employee(self, employee_first_name, employee_last_name, country_id, department_id, salary, email, phone_number):
    query = """
      INSERT INTO employees (employee_first_name, employee_last_name, country_id, department_id, salary, email, phone_number)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    self.cursor.execute(query, (employee_first_name, employee_last_name, country_id, department_id, salary, email, phone_number))
    self.connection.commit()
    print(f"Employee {employee_first_name} {employee_last_name} has been added successfully")

  def edit_employee(self, employee_id, first_name, last_name, country_id, department_id, salary, email, phone_number):
    employees = self.view_employees()
    if not employees:
      return
    
    try:
      print(f"\nEditing Employee '{first_name} {last_name}'")

      new_first = input("New First Name (or leave blank): ").strip() or first_name
      new_last = input("New Last Name (or leave blank): ").strip() or last_name
      new_salary = input("New Salary (or leave blank): ").strip() or salary
      new_email = input("New Email (or leave blank): ").strip() or email
      new_phone = input("New Phone (or leave blank): ").strip() or phone_number

      print("\n--- Select New Country ---")
      countries = self.view_country()
      new_country_id_input = input("Enter Country ID (or leave blank to keep current): ").strip()
      new_country_id = int(new_country_id_input) if new_country_id_input else country_id

      print("\n--- Select New Department ---")
      departments = self.view_department()
      new_dept_id_input = input("Enter Department ID (or leave blank to keep current): ").strip()
      new_dept_id = int(new_dept_id_input) if new_dept_id_input else department_id

      query = """
        UPDATE employees
        SET employee_first_name = %s,
          employee_last_name = %s,
          country_id = %s,
          department_id = %s,
          salary = %s,
          email = %s,
          phone_number = %s
        WHERE employee_id = %s
      """
      self.cursor.execute(query, (new_first, new_last, new_country_id, new_dept_id, new_salary, new_email, new_phone, employee_id))
      self.connection.commit()
      print("Employee updated successfully.")
    except Exception as e:
      print(f"Error in edition: {e}")
  
  def delete_employee(self, employee_id, employee_first_name, employee_last_name):
    employees = self.view_employees()

    if not employees:
      return
    
    confirm = input(f"Are you sure you want to delete employee '{employee_first_name}, {employee_last_name}' (y/n): ").lower().strip()
    if confirm != 'y':
        print("Deletion cancelled")
        return
    
    try:
      query = "DELETE FROM employees WHERE employee_id = %s"
      self.cursor.execute(query, (employee_id, ))
      self.connection.commit()

      if self.cursor.rowcount > 0:
          print(f"Employee {employee_first_name} {employee_last_name} has been deleted.")
      else:
          print(f"No employee found with ID {employee_id}.")

    except Exception as e:
      print(f"Error happened while deletion: {e}")

def department_manager(db):
  while True:
    print("\n ======================= Department Manager =======================")
    print("1. View Departments\n2. Add a department\n3. Edit a department\n4. Delete a department\n5. Go Back")
    choice = input("enter your choice: ")
    if choice == "1":
      db.view_department()

    elif choice == "2":
      department_name = input("Department Name: ")
      db.add_department(department_name)

    elif choice == "3":
      departments = db.view_department()

      if departments:
        try:
          edit_d_id = int(input("Enter the Department ID you want to edit: "))
          for dept in departments:
            if dept[0] == edit_d_id:
              db.edit_department((dept[0], dept[1]))
              break
            else:
                print("No department found with that ID.")
        except ValueError:
          print("Please Enter a valid number")
    
    elif choice == "4":
      departments = db.view_department()

      if departments:
        try:
          del_d_id = int(input("Enter the Department ID you want to delete: "))
          for dept in departments:
            if dept[0] == del_d_id:
              db.delete_department((dept[0], dept[1]))
              break
            else:
                print("No department found with that ID.")
        except ValueError:
          print("Please Enter a valid number")
    
    elif choice == "5":
      break
    
    else:
      print("Invalid choice. Try again.")
        

def countries_manager(db):
  while True:
    print("\n ======================= Country Manager =======================")
    print("1. View Countries\n2. Add a Country\n3. Edit a Country\n4. Delete a Country\n5. Go Back")
    
    choice = input("Enter your choice: ").strip()
    
    if choice == "1":
      db.view_country()

    elif choice == "2":
      country_name = input("Country Name: ").strip()
      country_type = input("Country Type: ").strip()
      db.add_country(country_name, country_type)

    elif choice == "3":
      countries = db.view_country()
      if countries:
        try:
          edit_c_id = int(input("Enter the Country ID you want to edit: "))
          for country in countries:
            if country[0] == edit_c_id:
              self_query = "SELECT country_type FROM country WHERE country_id = %s"
              db.cursor.execute(self_query, (edit_c_id,))
              result = db.cursor.fetchone()
              if result:
                country_type = result[0]
                db.edit_country(country[0], country[1], country_type)
              else:
                print("Country type not found for that ID.")
              break
          else:
            print("No country found with that ID.")
        except ValueError:
          print("Please enter a valid number.")

    elif choice == "4":
      countries = db.view_country()
      if countries:
        try:
          del_c_id = int(input("Enter the Country ID you want to delete: "))
          for country in countries:
            if country[0] == del_c_id:
              db.delete_country(country[0], country[1])
              break
          else:
            print("No country found with that ID.")
        except ValueError:
          print("Please enter a valid number.")

    elif choice == "5":
      break

    else:
      print("Invalid choice. Try again.")

def employees_manager(db):
  while True:
    print("\n ======================= Employees Manager =======================")
    print("1. View Employees\n2. Add an Employee\n3. Edit an Employee\n4. Delete an Employee\n5. Go Back")
    
    choice = input("Enter your choice: ").strip()

    if choice == "1":
      db.view_employees()

    elif choice == "2":
      first_name = input("First Name: ").strip()
      last_name = input("Last Name: ").strip()

      print("\n--- Choose Country ---")
      countries = db.view_country()
      country_id = int(input("Enter Country ID: ").strip())

      print("\n--- Choose Department ---")
      departments = db.view_department()
      department_id = int(input("Enter Department ID: ").strip())

      salary = input("Salary: ").strip()
      email = input("Email: ").strip()
      phone = input("Phone Number: ").strip()

      db.add_employee(first_name, last_name, country_id, department_id, salary, email, phone)

    elif choice == "3":
      employees = db.view_employees()
      if employees:
        try:
          edit_e_id = int(input("Enter the Employee ID you want to edit: "))
          for emp in employees:
            if emp[0] == edit_e_id:
              country_query = "SELECT country_id FROM country WHERE country_name = %s"
              db.cursor.execute(country_query, (emp[3],))
              country_id = db.cursor.fetchone()[0] if db.cursor.rowcount > 0 else None

              dept_query = "SELECT department_id FROM department WHERE department_name = %s"
              db.cursor.execute(dept_query, (emp[4],))
              department_id = db.cursor.fetchone()[0] if db.cursor.rowcount > 0 else None

              db.edit_employee(emp[0], emp[1], emp[2], country_id, department_id, emp[5], emp[6], emp[7])
              break
          else:
            print("No employee found with that ID.")
        except ValueError:
          print("Please enter a valid number.")

    elif choice == "4":
      employees = db.view_employees()
      if employees:
        try:
          del_e_id = int(input("Enter the Employee ID you want to delete: "))
          for emp in employees:
            if emp[0] == del_e_id:
              db.delete_employee(emp[0], emp[1], emp[2])
              break
          else:
            print("No employee found with that ID.")
        except ValueError:
          print("Please enter a valid number.")

    elif choice == "5":
      break
    else:
      print("Invalid choice. Try again.")

def search_mode(db):
  while True:
    print("\n ======================= Search Mode =======================")
    print("1. Search employees by Country")
    print("2. Search employees by Department")
    print("3. Go Back")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
      country_name = input("Enter Country Name: ").strip()
      query = """
        SELECT e.employee_id, e.employee_first_name, e.employee_last_name, c.country_name, 
               d.department_name, e.salary, e.email, e.phone_number
        FROM employees e
        LEFT JOIN country c ON e.country_id = c.country_id
        LEFT JOIN department d ON e.department_id = d.department_id
        WHERE LOWER(c.country_name) = LOWER(%s)
      """
      db.cursor.execute(query, (country_name,))
      rows = db.cursor.fetchall()

      if not rows:
        print(f"No employees found from country '{country_name}'.")
      else:
        print(f"\nEmployees from '{country_name}':")
        for employee_id, first, last, country, dept, salary, email, phone in rows:
          print(f"ID: {employee_id}, Name: {first} {last}, Country: {country}, Department: {dept}, Salary: {salary}, Email: {email}, Phone: {phone}")

    elif choice == "2":
      department_name = input("Enter Department Name: ").strip()
      query = """
        SELECT e.employee_id, e.employee_first_name, e.employee_last_name, c.country_name, 
               d.department_name, e.salary, e.email, e.phone_number
        FROM employees e
        LEFT JOIN country c ON e.country_id = c.country_id
        LEFT JOIN department d ON e.department_id = d.department_id
        WHERE LOWER(d.department_name) = LOWER(%s)
      """
      db.cursor.execute(query, (department_name,))
      rows = db.cursor.fetchall()

      if not rows:
        print(f"No employees found in department '{department_name}'.")
      else:
        print(f"\nEmployees in '{department_name}' department:")
        for employee_id, first, last, country, dept, salary, email, phone in rows:
          print(f"ID: {employee_id}, Name: {first} {last}, Country: {country}, Department: {dept}, Salary: {salary}, Email: {email}, Phone: {phone}")

    elif choice == "3":
      break

    else:
      print("Invalid choice. Try again.")

def main():
  db = DataConnect()

  while True:
    print("\n ======================= Main Menu ======================= ")
    print("1. Departments\n2. Countries\n3. Employees\n4. Search mode\n5. Exit")
    
    choice = input("Choose an option: ")
    if choice == "1":
      department_manager(db)

    elif choice == "2":
      countries_manager(db)

    elif choice == "3":
      employees_manager(db)
    
    elif choice == "4":
      search_mode(db)

    elif choice == "5":
      print("Exiting the program.")
      break

    else:
      print("Invalid choice, try again.")


if __name__ == "__main__":
  main()