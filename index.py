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
  
  def edit_department(self, department_id, department_name):
    departments = self.view_department()
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
  
  def delete_department(self, department_id, department_name):
    departments = self.view_department()

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
  
  def add_employee(self, employee_first_name, employee_last_name, country_name, department_name, salary, email, phone_number):
    query = """
      INSERT INTO employees (employee_first_name, employee_last_name, country_name, department_name, salary, email, phone_number)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    self.cursor.execute(query, (employee_first_name, employee_last_name, country_name, department_name, salary, email, phone_number))
    self.connection.commit()
    print(f"Employee {employee_first_name} {employee_last_name} has been added successfully")
  
  def edit_employee(self, employee_id, employee_first_name, employee_last_name, country_name, department_name, salary, email, phone_number):
    employees = self.view_employees()
    if not employees:
      return
    
    try:
      print(f"\nEditing Employee '{employee_first_name} {employee_last_name}'")
      new_employee_first_name = input("New Employee First Name (or leave blank to keep current): ").strip()
      if not new_employee_first_name:
        new_employee_first_name = employee_first_name

      new_employee_last_name = input("New Employee Last Name (or leave blank to keep current): ").strip()
      if not new_employee_last_name:
        new_employee_last_name = employee_last_name
      
      new_country_name = input("New Employee Country Name (or leave blank to keep current): ").strip()
      if not new_country_name:
        new_country_name = country_name
      
      new_department_name = input("New Employee Department Name (or leave blank to keep current): ").strip()
      if not new_department_name:
        new_department_name = department_name
      
      new_salary = input("New Employee Salary (or leave blank to keep current): ").strip()
      if not new_salary:
        new_salary = salary
      
      new_email = input("New Employee Email (or leave blank to keep current): ").strip()
      if not new_email:
        new_email = email
      
      new_phone_number = input("New Employee Phone Number (or leave blank to keep current): ").strip()
      if not new_phone_number:
        new_phone_number = phone_number

      query = """
        UPDATE employees 
        SET employee_first_name = %s, employee_last_name = %s, country_name = %s, department_name = %s, salary = %s, email = %s, phone_number = %s
        WHERE employee_id = %s 
      """
      self.cursor.execute(query, (new_employee_first_name, new_employee_last_name, new_country_name, new_department_name, new_salary, new_phone_number))
      self.connection.commit()
      print("Employee updated successfully")
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

def main():
  db = DataConnect()

  # db.view_department()
  # db.view_country()
  # db.add_country("Greenland", "Republic")
  # db.view_employees()
  # db.add_department('Sport')

  # db.delete_country(3, 'Germany')
  # db.edit_country(4, 'Greenladnd', "Republic")


if __name__ == "__main__":
  main()