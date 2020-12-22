"""Flask routes. API implementation"""

import re

from jsonschema import validate
from flask import request, jsonify
from flask import current_app as app

from .json_validation_schemas import \
    employee_json_schema, \
    job_json_schema, \
    department_json_schema
from .models import db, \
    Job, JobSchema, \
    Employee, EmployeeSchema, \
    Department, DepartmentSchema

# Init employee-schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Init job-schema
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

# Init department-schema
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


# For Jobs
@app.route('/job', methods=['GET'])
def get_all_jobs():
    """Get all records"""
    all_records = Job.query.all()
    result = jobs_schema.dump(all_records)
    return jsonify(result)


@app.route('/job/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    """Get record by ID"""
    record = Job.query.get(job_id)
    return job_schema.jsonify(record)


@app.route('/job', methods=['POST'])
def create_job():
    """Create record"""
    # Validate data
    try:
        validate(instance=request.get_json(),
                 schema=job_json_schema)
    except Exception as e:
        message = str(e).splitlines()[0]
        if re.search(r'does not match', message):
            message = "job_title required only alphabet " \
                      "characters and capitalize first letter!"
        return {"error": message}
    else:
        job_title = request.json['job_title']
        salary = request.json['salary']

        new_record = Job(job_title=job_title, salary=salary)
        db.session.add(new_record)
        db.session.commit()
        return job_schema.jsonify(new_record)


@app.route('/job/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    """Edit record"""
    record = Job.query.get(job_id)

    job_title = request.json['job_title']
    salary = request.json['salary']

    record.job_title = job_title
    record.salary = salary

    db.session.commit()
    return job_schema.jsonify(record)


@app.route('/job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete record"""
    record = Job.query.get(job_id)
    db.session.delete(record)
    db.session.commit()
    return job_schema.jsonify(record)


# For Employees
@app.route('/employee', methods=['GET'])
def get_all_employees():
    """Get all records"""
    all_records = Employee.query.all()
    result = employees_schema.dump(all_records)
    return jsonify(result)


@app.route('/employee/<int:employee_id>', methods=['GET'])
def get_one_employee(employee_id):
    """Get record by ID"""
    record = Employee.query.get(employee_id)
    return employee_schema.jsonify(record)


@app.route('/employee', methods=['POST'])
def create_employee():
    """Create record"""
    # Validate data
    try:
        validate(instance=request.get_json(),
                 schema=employee_json_schema)
    except Exception as e:
        message = str(e).splitlines()[0]
        if re.search(r'does not match', message):
            message = "first_name, last_name required only alphabet " \
                      "characters and capitalize first letter! " \
                      "And check Email!"
        return {"error": message}
    else:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        job_id = request.json['job_id']
        department_id = request.json['department_id']

        try:
            new_record = Employee(first_name=first_name,
                                  last_name=last_name,
                                  email=email, job_id=job_id,
                                  department_id=department_id)
            db.session.add(new_record)
            db.session.commit()
            return employee_schema.jsonify(new_record)
        except Exception as e:
            details = re.search(r'DETAIL:.+\.', str(e))
            return {"error": "Invalid foreign key! {}".format(details.group(0))}


@app.route('/employee/<int:employee_id>', methods=['PUT'])
def edit_employee(employee_id):
    """Edit record"""
    record = Employee.query.get(employee_id)

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    job_id = request.json['job_id']
    department_id = request.json['department_id']

    record.first_name = first_name
    record.last_name = last_name
    record.email = email
    record.job_id = job_id
    record.department_id = department_id

    db.session.commit()
    return employee_schema.jsonify(record)


@app.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete record"""
    record = Employee.query.get(employee_id)
    db.session.delete(record)
    db.session.commit()
    return employee_schema.jsonify(record)


# For Departments
@app.route('/department', methods=['GET'])
def get_all_departments():
    """Get all records"""
    all_records = Department.query.all()
    result = departments_schema.dump(all_records)
    return jsonify(result)


@app.route('/department/<int:department_id>', methods=['GET'])
def get_one_department(department_id):
    """Get record by ID"""
    record = Department.query.get(department_id)
    return department_schema.jsonify(record)


# Create record
@app.route('/department', methods=['POST'])
def create_department():
    """Create record"""
    # Validate data
    try:
        validate(instance=request.get_json(),
                 schema=department_json_schema)
    except Exception as e:
        message = str(e).splitlines()[0]
        if re.search(r'does not match', message):
            message = "department_name, location required only alphabet " \
                      "characters and capitalize first letter!"
        return {"error": message}
    else:
        department_name = request.json['department_name']
        location = request.json['location']

        new_record = Department(department_name=department_name,
                                location=location)
        db.session.add(new_record)
        db.session.commit()
        return department_schema.jsonify(new_record)


@app.route('/department/<int:department_id>', methods=['PUT'])
def edit_department(department_id):
    """Edit record"""
    record = Department.query.get(department_id)

    department_name = request.json['department_name']
    location = request.json['location']

    record.department_name = department_name
    record.location = location

    db.session.commit()
    return department_schema.jsonify(record)


@app.route('/department/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    """Delete record"""
    record = Department.query.get(department_id)
    db.session.delete(record)
    db.session.commit()
    return department_schema.jsonify(record)


@app.route('/salary-more-than', methods=['GET'])
def salary_more_than():
    """Bonus method.
    Returns employees having
    salary more than param <s>"""
    salary = request.args.get('s')
    records = Employee.query.join(Job).filter(Job.salary > salary)
    result = employees_schema.dump(records)
    return jsonify(result)
