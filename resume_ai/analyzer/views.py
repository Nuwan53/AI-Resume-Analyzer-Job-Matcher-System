from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Resume, ExtarctedData, Job, MatchResult


def home(request):
    """Root route for the app."""
    return redirect('upload_resume')


def extract_resume_data(file_path):
    """
    Placeholder function to extract data from resume file.
    In production, integrate with actual AI/NLP library (spaCy, YAKE, etc.)
    
    Args:
        file_path: Path to the uploaded resume file
    
    Returns:
        dict with 'skills', 'experience', 'education' keys
    """
    # TODO: Implement actual extraction logic
    # Placeholder data for MVP
    return {
        'skills': 'Python, Django, JavaScript, SQL, REST API',
        'experience': '3 years as Software Developer, 2 years as Junior Developer',
        'education': 'B.S. Computer Science'
    }


@require_http_methods(["GET", "POST"])
def upload_resume(request):
    """
    Handle resume file upload and create Resume + ExtractedData records.
    GET: Display upload form
    POST: Process uploaded file and extract data
    """
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES.get('resume_file')
            
            if not uploaded_file:
                messages.error(request, 'Please select a file to upload.')
                return redirect('upload_resume')
            
            # Validate file type (optional)
            allowed_extensions = ['pdf', 'doc', 'docx', 'txt']
            file_ext = uploaded_file.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                messages.error(request, f'File type .{file_ext} not allowed. Use {", ".join(allowed_extensions)}')
                return redirect('upload_resume')
            
            # Create Resume record
            resume = Resume.objects.create(file=uploaded_file)
            
            # Extract data from resume
            extracted_data_dict = extract_resume_data(resume.file.path)
            
            # Create ExtractedData record
            ExtarctedData.objects.create(
                resume=resume,
                skills=extracted_data_dict['skills'],
                experience=extracted_data_dict['experience'],
                education=extracted_data_dict['education']
            )
            
            messages.success(request, f'Resume uploaded successfully! ID: {resume.id}')
            return redirect('resume_detail', pk=resume.id)
            
        except Exception as e:
            messages.error(request, f'Error processing resume: {str(e)}')
            return redirect('upload_resume')
    
    return render(request, 'analyzer/upload.html')


def resume_list(request):
    """
    Display all uploaded resumes.
    """
    resumes = Resume.objects.all().order_by('-uploaded_at')
    context = {
        'resumes': resumes,
        'total_resumes': resumes.count()
    }
    return render(request, 'analyzer/resume_list.html', context)


def resume_detail(request, pk):
    """
    Display details of a specific resume with extracted data.
    """
    resume = get_object_or_404(Resume, pk=pk)
    
    try:
        extracted_data = ExtarctedData.objects.get(resume=resume)
    except ExtarctedData.DoesNotExist:
        extracted_data = None
    
    context = {
        'resume': resume,
        'extracted_data': extracted_data
    }
    return render(request, 'analyzer/resume_detail.html', context)


def match_results(request, pk):
    """
    Display job matches for a specific resume with match scores.
    """
    resume = get_object_or_404(Resume, pk=pk)
    matches = MatchResult.objects.filter(resume=resume).select_related('job').order_by('-score')
    
    context = {
        'resume': resume,
        'matches': matches,
        'total_matches': matches.count()
    }
    return render(request, 'analyzer/match_results.html', context)


def job_list(request):
    """
    Display all jobs in the system.
    """
    jobs = Job.objects.all()
    context = {
        'jobs': jobs,
        'total_jobs': jobs.count()
    }
    return render(request, 'analyzer/job_list.html', context)
