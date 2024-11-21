import os
import matplotlib.pyplot as plt
def load_students(file_path):
    students = {}
    with open(file_path, 'r') as file:
        for line in file:
            id = int(line[:3])
            name = line[3:].strip() 
            students[id] = name
    return students

def load_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            id = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments[id] = {"name": name, "points": points}
    return assignments
def load_valid_submissions(folder_path):
    submissions = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    student_id, assignment_id, grade = line.strip().split(',')
                    submissions.append({
                        "student_id": int(student_id),
                        "assignment_id": int(assignment_id),
                        "score": float(grade)
                    })
    return submissions

def calculate_student_grade(student_name, students, assignments, submissions):
    student_id = next((id for id, name in students.items() if name == student_name), None)
    if student_id is None:
        return "Student not found"
    
    total_score = 0
    total_possible = 0
    
    for submission in submissions:
        if submission['student_id'] == student_id:
            assignment = assignments[submission['assignment_id']]
            total_score += (submission['score'] / 100) * assignment['points']
            total_possible += assignment['points']
    
    grade_percentage = round((total_score / total_possible) * 100)
    return f"{grade_percentage}%"

def assignment_statistics(assignment_name, assignments, submissions):
    assignment_id = next((id for id, data in assignments.items() if data['name'] == assignment_name), None)
    if assignment_id is None:
        return "Assignment not found"
    
    scores = [sub['score'] for sub in submissions if sub['assignment_id'] == assignment_id]
    if not scores:
        return "No submissions found for this assignment"
    
    min_score = min(scores)
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)
    return f"Min: {round(min_score)}%\nAvg: {round(avg_score)}%\nMax: {round(max_score)}%"

def assignment_graph(assignment_name, assignments, submissions):
    assignment_id = next((id for id, data in assignments.items() if data['name'] == assignment_name), None)
    if assignment_id is None:
        return "Assignment not found"
    
    scores = [sub['score'] for sub in submissions if sub['assignment_id'] == assignment_id]
    if not scores:
        return "No submissions found for this assignment"
    
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Histogram for {assignment_name}")
    plt.xlabel("Scores")
    plt.ylabel("Frequency")
    plt.show()

def main():
    data_path = "C:\\Users\\Colin\\Downloads\\data"
    submissions_path = os.path.join(data_path, 'submissions')
    students = load_students(os.path.join(data_path, 'students.txt'))
    assignments = load_assignments(os.path.join(data_path, 'assignments.txt'))
    submissions = load_valid_submissions(submissions_path)
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    
    choice = input("Enter your selection: ")
    
    if choice == '1':
        student_name = input("What is the student's name: ")
        print(calculate_student_grade(student_name, students, assignments, submissions))
    elif choice == '2':
        assignment_name = input("What is the assignment name: ")
        print(assignment_statistics(assignment_name, assignments, submissions))
    elif choice == '3':
        assignment_name = input("What is the assignment name: ")
        result = assignment_graph(assignment_name, assignments, submissions)
        if result is not None:
            print(result)
    else:
        print("Invalid selection")

if __name__ == "__main__":
    main()
