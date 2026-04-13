"""
Management command to load sample jobs into the database.
Usage: python manage.py load_jobs
"""

from django.core.management.base import BaseCommand
from analyzer.models import Job


class Command(BaseCommand):
    help = 'Load sample jobs into the database'

    def handle(self, *args, **options):
        """Handle the command execution."""
        
        # Check if jobs already exist
        if Job.objects.exists():
            self.stdout.write(
                self.style.WARNING('Jobs already exist in database. Skipping.')
            )
            return
        
        # Sample jobs data
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'description': 'We are looking for an experienced Python developer to lead backend development. You will work on Django-based microservices, optimize database queries, and mentor junior developers.',
                'required_skills': 'Python, Django, SQL, REST API, Docker, PostgreSQL, Git, Unit Testing'
            },
            {
                'title': 'Full Stack JavaScript Developer',
                'description': 'Join our team to build modern web applications. You will develop both frontend with React and backend with Node.js/Express. Own features end-to-end from design to deployment.',
                'required_skills': 'JavaScript, React, Node.js, Express, HTML, CSS, MongoDB, Git, webpack'
            },
            {
                'title': 'Data Scientist',
                'description': 'We need a Data Scientist to build ML models for predictive analytics. Work with large datasets, conduct A/B testing, and deploy models to production. Strong statistical background required.',
                'required_skills': 'Python, Machine Learning, Deep Learning, TensorFlow, Pandas, NumPy, SQL, Tableau, R'
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Manage and optimize our cloud infrastructure on AWS. You will implement CI/CD pipelines, containerize applications, monitor system performance, and ensure high availability.',
                'required_skills': 'Docker, Kubernetes, AWS, CI/CD, Jenkins, Terraform, Linux, Git, Ansible'
            },
            {
                'title': 'Frontend React Developer',
                'description': 'Create beautiful and responsive user interfaces using React. Focus on component design, state management, and performance optimization. Work with modern frontend tooling.',
                'required_skills': 'React, JavaScript, HTML, CSS, Redux, Jest, Webpack, Git, UI/UX'
            },
            {
                'title': 'Mobile App Developer (iOS)',
                'description': 'Develop native iOS applications using Swift. Build performant, user-friendly apps with beautiful UI. Participate in code reviews and contribute to architectural decisions.',
                'required_skills': 'Swift, Objective-C, iOS SDK, Xcode, REST API, Git, Core Data, XCTest'
            },
            {
                'title': 'Database Administrator',
                'description': 'Manage and maintain our database infrastructure. Optimize queries, handle backups, ensure security and compliance, and troubleshoot performance issues.',
                'required_skills': 'SQL, PostgreSQL, MySQL, MongoDB, NoSQL, Linux, Backup & Recovery, Performance Tuning'
            },
            {
                'title': 'QA Engineer / Test Automation',
                'description': 'Develop automated test suites and ensure software quality. Create test strategies, identify bugs, and collaborate with developers to fix issues.',
                'required_skills': 'Selenium, Python, TestNG, JIRA, API Testing, CI/CD, Git, SQL, Problem-solving'
            },
            {
                'title': 'Cloud Solutions Architect',
                'description': 'Design scalable cloud solutions for enterprise clients. Work with AWS/Azure, design microservices architecture, and ensure best practices for security and performance.',
                'required_skills': 'AWS, Azure, Microservices, Docker, Kubernetes, Architecture Design, Linux, Networking'
            },
            {
                'title': 'Java Backend Developer',
                'description': 'Develop robust backend services using Java and Spring framework. Build RESTful APIs, work with relational databases, and ensure code quality through testing.',
                'required_skills': 'Java, Spring Boot, SQL, REST API, Microservices, JUnit, Maven, Git, Apache'
            },
        ]
        
        # Create jobs
        created_count = 0
        for job_data in sample_jobs:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                defaults={
                    'description': job_data['description'],
                    'required_skills': job_data['required_skills']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {job.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'~ Already exists: {job.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully loaded {created_count} new jobs!'
            )
        )
