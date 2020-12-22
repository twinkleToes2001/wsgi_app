"""Tables for database with abstract class
Tables: Employee, Job, Department, also
there are Marshmallow Schemas for convert
flask-sqlalchemy data to JSON data"""

from . import db, ma


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        """Define a base way to print models"""
        return '{name}({kwargs})' \
            .format(name=self.__class__.__name__,
                    kwargs={column: value
                            for column, value in self.__dict__.items()})


class Employee(BaseModel, db.Model):
    """Employees table"""
    __tablename__ = 'employees'

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))


class EmployeeSchema(ma.Schema):
    """Employee marshmallow schema"""
    class Meta:
        fields = ('id', 'first_name', 'last_name',
                  'email', 'job_id', 'department_id')


class Job(BaseModel, db.Model):
    """Jobs table"""
    __tablename__ = 'jobs'

    job_title = db.Column(db.String(30), unique=True)
    salary = db.Column(db.Integer)

    employee_id = db.relationship('Employee', backref='job')


class JobSchema(ma.Schema):
    """Job marshmallow schema"""
    class Meta:
        fields = ('id', 'job_title', 'salary')


class Department(BaseModel, db.Model):
    """Departments table"""
    __tablename__ = 'departments'

    department_name = db.Column(db.String(30), unique=True)
    location = db.Column(db.String(50), unique=True)

    employee_id = db.relationship('Employee', backref='department')


class DepartmentSchema(ma.Schema):
    """Department marshmallow schema"""
    class Meta:
        fields = ('id', 'department_name', 'location')
