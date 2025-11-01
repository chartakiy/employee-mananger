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
        print(f"Employee ID: {employee_id}, Employee Name: {employee_first_name} {employee_last_name}, Country Name: {country_name}, Department Name: {department_name}, Salary: {salary}, Email: {email}")

    return rows


def main():
  db = DataConnect()

  db.view_department()
  # db.view_country()
  # db.view_employees()
  # db.add_department('Sport')


if __name__ == "__main__":
  main()