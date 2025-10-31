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
  
  # -----------------------------------------------------------------------------
  # ------------------------- code for country table ----------------------------
  # -----------------------------------------------------------------------------
  def view_country(self):
    query = "SELECT country_id, country_name, country_type FROM country"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()

    if not rows:
      print("no country can be found")
    else:
      print("\n========= COUNTRIES =========")

      for country_id, country_name, country_type in rows:
        print(f"Country ID: {country_id}, Country Name: {country_name}, Country Type: {country_type}")

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

  # db.view_department()
  # db.view_country()
  # db.view_employees()
  # db.add_department('Sport')


if __name__ == "__main__":
  main()