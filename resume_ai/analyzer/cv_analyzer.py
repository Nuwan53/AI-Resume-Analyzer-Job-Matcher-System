"""
CV Analyzer Module
Handles resume data extraction, skill parsing, and job matching algorithms.
"""

from difflib import SequenceMatcher
import re


class CVAnalyzer:
    """Analyzes CV/resume data and matches against job requirements."""
    
    # Common skill keywords for better matching
    SKILL_KEYWORDS = {
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
        'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'nosql', 'postgresql', 'mysql',
        'mongodb', 'redis', 'elasticsearch', 'django', 'flask', 'fastapi', 'spring',
        'react', 'vue', 'angular', 'node', 'express', 'webpack', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'ci/cd', 'jenkins', 'gitlab', 'github', 'linux', 'windows',
        'git', 'svn', 'rest', 'graphql', 'soap', 'html', 'css', 'json', 'xml', 'yaml',
        'agile', 'scrum', 'jira', 'confluence', 'selenium', 'pytest', 'junit', 'unittest',
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
        'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'excel', 'tableau',
        'power bi', 'looker', 'datarobot', 'spark', 'hadoop', 'hive', 'presto',
        'devops', 'infrastructure', 'terraform', 'ansible', 'prometheus', 'grafana',
        'iot', 'blockchain', 'microservices', 'monolith', 'api', 'rpc', 'grpc',
        'communication', 'teamwork', 'leadership', 'problem-solving', 'analytical',
        'project management', 'stakeholder management', 'mentoring', 'technical writing'
    }
    
    @staticmethod
    def extract_skills(text):
        """
        Extract skills from resume text.
        
        Args:
            text (str): Resume text content
            
        Returns:
            list: List of detected skills
        """
        if not text:
            return []
        
        text_lower = text.lower()
        detected_skills = []
        
        for skill in CVAnalyzer.SKILL_KEYWORDS:
            if skill in text_lower:
                detected_skills.append(skill)
        
        return list(set(detected_skills))  # Remove duplicates
    
    @staticmethod
    def normalize_skill(skill):
        """
        Normalize skill name for comparison.
        
        Args:
            skill (str): Skill name
            
        Returns:
            str: Normalized skill
        """
        return skill.lower().strip()
    
    @staticmethod
    def string_similarity(a, b):
        """
        Calculate similarity between two strings (0-1).
        
        Args:
            a (str): First string
            b (str): Second string
            
        Returns:
            float: Similarity score
        """
        a = CVAnalyzer.normalize_skill(a)
        b = CVAnalyzer.normalize_skill(b)
        return SequenceMatcher(None, a, b).ratio()
    
    @staticmethod
    def calculate_match_score(resume_data, job):
        """
        Calculate match score between resume and job (0-100).
        
        Scoring logic:
        - Extract skills from resume text
        - Compare against job required skills
        - Match score = (matched_skills / total_required_skills) * 100
        - Bonus points for keyword/experience matching
        
        Args:
            resume_data (ExtractedData): Resume extracted data object
            job (Job): Job object
            
        Returns:
            float: Match score (0-100)
        """
        if not resume_data or not job:
            return 0.0
        
        # Combine all resume text for analysis
        resume_text = f"{resume_data.skills} {resume_data.experience} {resume_data.education}"
        
        # Extract skills from resume
        resume_skills = CVAnalyzer.extract_skills(resume_text)
        
        if not resume_skills:
            return 0.0
        
        # Parse required skills from job
        job_skills_text = job.required_skills.lower()
        required_skills = [s.strip() for s in job_skills_text.split(',')]
        required_skills = [s for s in required_skills if s]  # Remove empty strings
        
        if not required_skills:
            return 0.0
        
        # Calculate skill matches
        matched_count = 0
        for required_skill in required_skills:
            # Check for exact or similar match
            for resume_skill in resume_skills:
                similarity = CVAnalyzer.string_similarity(required_skill, resume_skill)
                if similarity >= 0.6:  # 60% threshold for similarity
                    matched_count += 1
                    break
                    
                # Also check substring matches
                if required_skill in resume_skill or resume_skill in required_skill:
                    matched_count += 1
                    break
        
        # Base score: skill match percentage
        base_score = (matched_count / len(required_skills)) * 100
        
        # Bonus scoring for experience/education keywords
        experience_bonus = 0
        if 'experience' in resume_text.lower() or 'years' in resume_text.lower():
            experience_bonus = 10
        
        education_bonus = 0
        if 'degree' in resume_text.lower() or 'university' in resume_text.lower() or 'college' in resume_text.lower():
            education_bonus = 5
        
        # Calculate final score (capped at 100)
        final_score = min(base_score + experience_bonus + education_bonus, 100.0)
        
        return round(final_score, 2)
    
    @staticmethod
    def generate_all_matches(resume, jobs):
        """
        Generate match scores for resume against all jobs.
        
        Args:
            resume (Resume): Resume object
            jobs (QuerySet): Job queryset
            
        Returns:
            list: List of tuples (job, score)
        """
        from .models import ExtarctedData
        
        try:
            extracted_data = ExtarctedData.objects.get(resume=resume)
        except ExtarctedData.DoesNotExist:
            return []
        
        matches = []
        for job in jobs:
            score = CVAnalyzer.calculate_match_score(extracted_data, job)
            matches.append((job, score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
