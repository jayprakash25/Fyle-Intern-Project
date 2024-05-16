import pytest
from core.models.assignments import Assignment, AssignmentStateEnum
from core import db 
import threading



def test_grade_assignment(client, h_principal):
    # # Grade the assignment
    grade_payload = {'id': '1', 'grade': 'A'}
    response = client.post('/principal/assignments/grade', headers=h_principal, json=grade_payload)

    assert response.status_code == 200
    assert response.json['data']['grade'] == 'A'
    assert response.json['data']['state'] == 'GRADED'

def test_grade_non_existing_assignment(client, h_principal):
    """
    Test grading a non-existing assignment
    """
    # grade_payload = {'id': 999, 'grade': 'A'}
    response = client.post('/principal/assignments/grade', json={'id': 999, 'grade': 'A'} , headers=h_principal)

    assert response.status_code == 404
    assert 'Assignment not found' in response.json['error']

def test_grade_draft_assignment(client, h_principal):
    """Test grading an assignment in the draft state"""
    # Retrieve an existing assignment in the DRAFT state
    assignment = Assignment.query.filter_by(state=AssignmentStateEnum.DRAFT.value).first()
    if assignment:
        grade_payload = {'id': assignment.id, 'grade': 'A'}
        response = client.post('/principal/assignments/grade', headers=h_principal, json=grade_payload)
        assert response.status_code == 400
        assert 'Assignment cannot be graded in the draft state' in response.json['error']
    else:
        pytest.skip("No assignment in DRAFT state found in the database")

def test_regrade_assignment(client, h_principal):
    """Test re-grading an already graded assignment"""
    # Retrieve an existing assignment in the GRADED state
    assignment = Assignment.query.filter_by(state=AssignmentStateEnum.GRADED.value).first()
    if assignment:
        grade_payload = {'id': assignment.id, 'grade': 'A'}
        response = client.post('/principal/assignments/grade', headers=h_principal, json=grade_payload)
        assert response.status_code == 200
        assert response.json['data']['grade'] == 'A'
        assert response.json['data']['state'] == 'GRADED'
    else:
        pytest.skip("No assignment in GRADED state found in the database")



def test_concurrent_grading(client, h_principal):
    """Test concurrent grading attempts"""
    grade_payload = {'id': '1', 'grade': 'B'}

    def grade():
        client.post('/principal/assignments/grade', headers=h_principal, json=grade_payload)

    threads = []
    for _ in range(2):
        thread = threading.Thread(target=grade)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assignment = Assignment.query.get(1)
    assert assignment.grade == 'B'

def test_idempotent_grading(client, h_principal):
    """Test same grading behavior"""
    assignment = Assignment.query.filter_by(state=AssignmentStateEnum.GRADED.value).first()
    original_grade = assignment.grade
    grade_payload = {'id': assignment.id, 'grade': original_grade}
    response = client.post('/principal/assignments/grade', headers=h_principal, json=grade_payload)
    assert response.status_code == 200
    assert response.json['data']['grade'] == original_grade



