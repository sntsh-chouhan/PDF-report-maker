from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader('templates'))

def render_student_report(student):
    template = env.get_template('report.html')
    return template.render(student=student)

def get_students():
    with open('data/students.json') as f:
        return json.load(f)
