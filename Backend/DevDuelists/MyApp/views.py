from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Problem
from .forms import CodeSubmissionForm
import uuid
import subprocess
import os
from django.conf import settings
from pathlib import Path



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    context = {}
    return render(request, 'login.html', context)

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Oops! Something went wrong. Please try again.')
    
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def homePage(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url = 'login')
def problemPage(request):
    search_query = request.GET.get('search') if request.GET.get('search') else ''
    problems = Problem.objects.filter(
        Q(name__icontains=search_query)
    )
    return render(request, 'problems.html', {'problems': problems, 'search_query': search_query})

@login_required(login_url = 'login')
def discussionPage(request):
    return render(request, 'Discussions.html')

@login_required(login_url = 'login')
def solvePage(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render(request, 'solve.html', {'problem': problem})

@login_required(login_url = 'login')
def logoutButton(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def solveProblemPage(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeSubmissionForm(request.POST or None)
    if request.method == 'POST':
        custom_tc = request.POST.get('custom_tc', '')
        action = request.POST.get('action')

        if form.is_valid():
            language = form.cleaned_data['language']
            code = form.cleaned_data['code']
            output, error, verdict = '', '', ''

            if action == 'run':
                output, error = run_code(language, code, custom_tc)
            elif action == 'submit':
                hidden_input = problem.hidden_input
                expected_output = problem.expected_output.strip()
                output, error = run_code(language, code, hidden_input)
                print(f"Expected Output: {expected_output!r}")
                print(f"Actual Output: {output!r}")
                output = output.strip()
                expected_output = expected_output.strip()
                verdict = "Accepted" if output == expected_output else "Wrong Answer"

            code_instance = form.save(commit=False)
            code_instance.myuser = request.user
            code_instance.result = output if not error else error
            code_instance.save()
            context = {
                'problem': problem,
                'form': form,
                'code': code_instance.code,
                'custom_tc': custom_tc,
                'output': output,
                'error': error,
                'verdict': verdict,
            }
            return render(request, 'solve.html', context)
    context = {'problem': problem, 'form': form}
    return render(request, 'solve.html', context)


def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ("codes", "inputs", "outputs")

    # Create directories if they don't exist
    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    ext_map = {"cpp": "cpp", "py": "py", "c": "c"}
    code_file_name = f"{unique}.{ext_map[language]}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    print(f"Writing code to {code_file_path}")
    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    print(f"Writing input data to {input_file_path}")
    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    output_data = ""
    error_data = ""

    try:
        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                capture_output=True,
                text=True
            )
            print(f"Compile result: {compile_result.returncode}, stderr: {compile_result.stderr}")
            if compile_result.returncode == 0:
                run_result = subprocess.run(
                    [str(executable_path)],
                    stdin=open(input_file_path, "r"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output_data = run_result.stdout
                error_data = run_result.stderr
                print(f"Run result: stdout: {output_data}, stderr: {error_data}")
                print(f"Writing output data to {output_file_path}")
                with open(output_file_path, "w") as output_file:
                    output_file.write(output_data)
            else:
                error_data = compile_result.stderr
        elif language == "c":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["gcc", str(code_file_path), "-o", str(executable_path)],
                capture_output=True,
                text=True
            )
            print(f"Compile result: {compile_result.returncode}, stderr: {compile_result.stderr}")
            if compile_result.returncode == 0:
                run_result = subprocess.run(
                    [str(executable_path)],
                    stdin=open(input_file_path, "r"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output_data = run_result.stdout
                error_data = run_result.stderr
                print(f"Run result: stdout: {output_data}, stderr: {error_data}")
                print(f"Writing output data to {output_file_path}")
                with open(output_file_path, "w") as output_file:
                    output_file.write(output_data)
            else:
                error_data = compile_result.stderr
        elif language == "py":
            run_result = subprocess.run(
                ["python", str(code_file_path)],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output_data = run_result.stdout
            error_data = run_result.stderr
            print(f"Run result: stdout: {output_data}, stderr: {error_data}")
            print(f"Writing output data to {output_file_path}")
            with open(output_file_path, "w") as output_file:
                output_file.write(output_data)

    except Exception as e:
        error_data = str(e)
        print(f"Exception: {error_data}")

    os.remove(code_file_path)
    os.remove(input_file_path)
    if output_file_path.exists():
        os.remove(output_file_path)
    if 'executable_path' in locals() and executable_path.exists():
        os.remove(executable_path)

    return output_data, error_data