from app import db
class Employee(db.Model):
    
    # Create an Employee table
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    job_title = db.Column(db.String(60))
    years_of_experience = db.Column(db.Integer)
    salary = db.Column(db.Float)

    
    def __init__(self,first_name,last_name,department_id,
                  job_title,years_of_experience,salary):

                  self.first_name = first_name
                  self.last_name = last_name
                  self.department_id = department_id
                  self.job_title = job_title
                  self.years_of_experience = years_of_experience
                  self.salary = salary
        

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'department': Department.query.get(self.department_id).name,
            'job_title': self.job_title,
            'years_of_experience': self.years_of_experience,
            'salary' : self.salary



            
        }



class Department(db.Model):

    # Create a Department table 
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'no_of_employees': self.employees.count()
            
        }
    def __init__(self,name):
        self.name = name