from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher

from .schema import AssignmentSchema

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_principal_assignments(p, incoming_payload):
    """Returns list of submitted and graded assignments"""
    assignments = Assignment.query.filter(
        Assignment.state.in_(['SUBMITTED', 'GRADED', 'DRAFT'])
    ).all()
    assignment_data = AssignmentSchema(many=True).dump(assignments)
    return APIResponse.respond(data=assignment_data)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_principal_teachers(p, incoming_payload):
    """Returns list of all teachers"""
    teachers = Teacher.query.all()
    #serialize the teachers
    
    teacher_data = [teacher.serialize() for teacher in teachers]
    return APIResponse.respond(data=teacher_data)

@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def principal_grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    assignment_id = incoming_payload.get('id')
    grade = incoming_payload.get('grade')

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return APIResponse.respond_error('Assignment not found', 404)

    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond_error('Assignment cannot be graded in the draft state', 400)

    assignment.grade = grade
    assignment.state = 'GRADED'
    db.session.commit()

    return APIResponse.respond(data=assignment.serialize())
