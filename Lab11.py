import os
import matplotlib.pyplot as plt
def read_students(file_path):
    students = {}
    with open(file_path, 'r') as file:
        for line in file:
            student_id = line[:3]
            student_name = line[3:].strip()
            students[student_id] = student_name
    return students
def read_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as file:
        while True:
            assignment_name = file.readline().strip()
            if not assignment_name:
                break
            assignment_id = file.readline().strip()
            points = int(file.readline().strip())
            assignments[assignment_id] = (assignment_name, points)
    return assignments
def read_scores(folder_path):
    scores = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                for line in file:
                    student_id, assignment_id, score = line.strip().split('|')
                    if assignment_id not in scores:
                        scores[assignment_id] = []
                    scores[assignment_id].append((student_id, int(score)))
    return scores
def calculate_student_grade(student_name, students, scores, assignments):
    student_id = next((id for id, name in students.items() if name.lower() == student_name.lower()), None)
    if not student_id:
        return "Student not found"
    total_weighted_score = 0
    total_points = 0
    for assignment_id, score_list in scores.items():
        for sid, s_score in score_list:
            if sid == student_id:
                assignment_name, points = assignments[assignment_id]
                total_weighted_score += (s_score / 100) * points
                total_points += points
    percentage = int(round((total_weighted_score / total_points) * 100)) if total_points > 0 else 0
    return f"{percentage}%"
def assignment_statistics(assignment_name, assignments, scores):
    assignment_id = next((id for id, (name, _) in assignments.items() if name == assignment_name), None)
    if not assignment_id:
        return "Assignment not found"
    scores_list = [s_score for sid, s_score in scores.get(assignment_id, [])]
    if not scores_list:
        return "No scores found for this assignment."
    max_score = max(scores_list)
    min_score = min(scores_list)
    avg_score = sum(scores_list) / len(scores_list)
    return f"Min: {min_score}% \nAvg: {int(round(avg_score,1)*10//10)}% \nMax: {max_score}%"
def plot_assignment_graph(assignment_name, assignments, scores):
    assignment_id = next((id for id, (name, _) in assignments.items() if name == assignment_name), None)
    if not assignment_id:
        print("Assignment not found")
        return
    scores_list = []
    for sid, s_score in scores.get(assignment_id, []):
        scores_list.append(s_score)
    if not scores_list:
        print("No scores found for this assignment.")
        return
    plt.hist(scores_list, bins=10, edgecolor='black')
    plt.title(f'Scores for {assignment_name}')
    plt.xlabel('Assignment Score out of 100')
    plt.ylabel('Number of Students')
    plt.show()
def print_menu():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print("\nEnter your selection: ", end='')
def main():
    students = read_students("data/students.txt")
    assignments = read_assignments("data/assignments.txt")
    scores = read_scores("data/submissions")
    print_menu()
    selection = input().strip()
    if selection == '1':
        student_name = input("What is the student's name: ")
        result = calculate_student_grade(student_name, students, scores, assignments)
        print(result)
    elif selection == '2':
        assignment_name = input("What is the assignment name: ")
        result = assignment_statistics(assignment_name, assignments, scores)
        print(result)
    elif selection == '3':
        assignment_name = input("What is the assignment name: ")
        plot_assignment_graph(assignment_name, assignments, scores)
    else:
        print("Invalid selection.")
if __name__ == "__main__":
    main()
