import imp
from xml.dom.minidom import Identified
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


####Configurations
app = Flask(__name__)
app.secret_key = b'123456'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Crud_Task'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jszxyeresdlick:89ebf25c07e1738f376693cb1b6ce66eab84980c324bfabb1f5b7e25ae47ce41@ec2-44-195-100-240.compute-1.amazonaws.com:5432/d5tloei57vlptg'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


###### MODELS ######
from models import Employee,Department

####Salary Computation 
def compute_salary(years_of_experience,title):
    salary = 12000
    match (title):
        case 'Junior Software Developer':
            salary = salary + years_of_experience*salary*0.1
        case 'Senior Software Developer':
            salary = salary + years_of_experience*salary*0.2
        case 'Data Engineer':
            salary = salary + years_of_experience*salary*0.2
        case 'Intern':
            salary = 3000
        case _:
            salary = salary
    return salary



##GET ALL DEPARTMENTS
@app.route('/',methods = ['GET'])
def show_departments():
    if request.method == 'GET':
        return render_template('departments/departments.html',departments = Department.query.all())
    
        
##EDIT DEPARTMENT
@app.route('/edit_department/<int:id>',methods = ['GET','POST'])
def edit_department(id):
    if request.method == 'POST':
        name = request.form['name']
        
        
        if db.session.query(Department).filter(Department.name == name).count() == 0:
            db.session.query(Department).filter_by(id=id).update(dict(name = name))

            db.session.commit()
            
            
            return render_template('departments/departments.html'
            ,departments = Department.query.all())
            
    
        return render_template('departments/edit_department.html'
        ,department = Department.query.get(id),message = "Department Name Already Exists")
    return render_template('departments/edit_department.html'
        ,department = Department.query.get(id))

##DELETE DEPARTMENT

@app.route('/delete_department/<id>')
def delete_department(id):
    print(id)
    db.session.query(Department).filter_by(id=id).delete()
    db.session.commit()
    return render_template('departments/departments.html',departments = Department.query.all())


#ADD DEPARTMENT
@app.route('/add_department',methods = ['POST','GET'])
def add_department():
    if request.method == 'GET':
        return render_template('departments/add_department.html')
    elif request.method == 'POST':
        name = request.form['name']
        print(name)
        if name == '':
            flash('Name Not Found')
            return render_template('departments/add_department.html')

        if db.session.query(Department).filter(Department.name == name).count() == 0:
            data = Department(name)
            db.session.add(data)
            db.session.commit()
            
           
            return render_template('departments/departments.html'
            ,departments = Department.query.all())









##GET ALL EMPLOYEES

@app.route('/employees',methods = ['GET','POST'])
def show_employees():
    if request.method == 'GET':
        return render_template('employees/employees.html'
            ,employees = Employee.query.all(),departments = Department.query.all())



##EDIT EMPLOYEE
    

@app.route('/employees/edit_employee/<id>',methods = ['POST','GET'])
def edit_employee(id):
    if request.method == 'POST':
        
        department = Department.query.filter_by(name = request.form['department']).first()


        print(request.form['title'])
        db.session.query(Employee).filter_by(id=id).update(
        dict(first_name = request.form['first_name'], last_name = request.form['last_name'],
        job_title = request.form['title'],years_of_experience = request.form['years_of_experience']
        ,department_id = department.id,
        salary = compute_salary(int(request.form['years_of_experience']),request.form['title'])))

        db.session.commit()
        return render_template('employees/employees.html' 
        ,employees = Employee.query.all(),departments = Department.query.all())
    if request.method == 'GET':
        return render_template('employees/edit_employee.html'
        ,employee = Employee.query.get(id))

##DELETE EMPLOYEE
@app.route('/employees/delete_employee/<id>')
def delete_employee(id):
    print(id)
    db.session.query(Employee).filter_by(id=id).delete()
    db.session.commit()
    return render_template('employees/employees.html'
            ,employees = Employee.query.all(),departments = Department.query.all())

##ADD EMPLOYEE

@app.route('/employees/add_employee',methods = ['POST', 'GET'])
def add_employee():
    if request.method == 'GET':
        return render_template('employees/add_employee.html',departments = Department.query.all())
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        title =  request.form['title']
        department = request.form['department']
        years_of_experience =  int(request.form['years_of_experience'])
        salary =  compute_salary(years_of_experience,title)
        
        employee = Employee(first_name,last_name,department,title,
        years_of_experience,salary)


        

        db.session.add(employee)
        db.session.commit()
            
           
        return render_template('employees/employees.html'
            ,employees = Employee.query.all(),departments = Department.query.all())

if __name__ == '__main__':
    app.run()

        
    