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
    
    @staticmethod
    def analyze_skill_gaps(resume_data, job):
        """
        Analyze skill gaps between resume and job requirements.
        
        Args:
            resume_data (ExtractedData): Resume extracted data
            job (Job): Job object
            
        Returns:
            dict: Gap analysis with matched and missing skills
        """
        if not resume_data or not job:
            return {
                'matched_skills': [],
                'missing_skills': [],
                'gap_percentage': 100.0
            }
        
        # Extract resume skills
        resume_text = f"{resume_data.skills} {resume_data.experience} {resume_data.education}"
        resume_skills = CVAnalyzer.extract_skills(resume_text)
        
        # Parse required skills
        job_skills_text = job.required_skills.lower()
        required_skills = [s.strip() for s in job_skills_text.split(',')]
        required_skills = [s for s in required_skills if s]
        
        if not required_skills:
            return {
                'matched_skills': [],
                'missing_skills': [],
                'gap_percentage': 0.0
            }
        
        matched_skills = []
        missing_skills = []
        
        for required_skill in required_skills:
            found = False
            for resume_skill in resume_skills:
                similarity = CVAnalyzer.string_similarity(required_skill, resume_skill)
                if similarity >= 0.6 or required_skill in resume_skill or resume_skill in required_skill:
                    matched_skills.append(required_skill)
                    found = True
                    break
            
            if not found:
                missing_skills.append(required_skill)
        
        gap_percentage = (len(missing_skills) / len(required_skills)) * 100 if required_skills else 0
        
        return {
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'gap_percentage': round(gap_percentage, 1)
        }
    
    @staticmethod
    def get_top_recommendations(resume, jobs, top_n=5):
        """
        Get top skill recommendations based on job market demand.
        
        Args:
            resume (Resume): Resume object
            jobs (QuerySet): All available jobs
            top_n (int): Number of recommendations to return
            
        Returns:
            list: List of skill recommendations with frequency and importance scores
        """
        from .models import ExtarctedData
        from collections import Counter
        
        try:
            extracted_data = ExtarctedData.objects.get(resume=resume)
        except ExtarctedData.DoesNotExist:
            return []
        
        # Get resume skills
        resume_text = f"{extracted_data.skills} {extracted_data.experience} {extracted_data.education}"
        resume_skills = set(CVAnalyzer.extract_skills(resume_text))
        
        # Count skill demand across all jobs
        skill_frequency = Counter()
        skill_improvements = {}
        
        for job in jobs:
            job_skills_text = job.required_skills.lower()
            required_skills = [s.strip() for s in job_skills_text.split(',')]
            required_skills = [s for s in required_skills if s]
            
            for skill in required_skills:
                # Check if user already has this skill
                has_skill = any(
                    CVAnalyzer.string_similarity(skill, user_skill) >= 0.6 
                    for user_skill in resume_skills
                )
                
                if not has_skill:
                    skill_frequency[skill] += 1
                    if skill not in skill_improvements:
                        skill_improvements[skill] = 0
                    skill_improvements[skill] += 1
        
        # Calculate importance score
        recommendations = []
        for skill, frequency in skill_frequency.most_common():
            improvement = skill_improvements.get(skill, 0)
            importance_score = (frequency * 0.6) + (improvement * 0.4)
            recommendations.append({
                'skill': skill,
                'frequency': frequency,
                'importance_score': round(importance_score, 2)
            })
        
        return recommendations[:top_n]
    
    @staticmethod
    def get_skill_recommendations_for_job(resume_data, job):
        """
        Get skill recommendations specific to a job with priority levels.
        
        Args:
            resume_data (ExtractedData): Resume data
            job (Job): Target job
            
        Returns:
            dict: Recommendations categorized by priority
        """
        gaps = CVAnalyzer.analyze_skill_gaps(resume_data, job)
        
        # Categorize skills by priority
        high_priority = []
        medium_priority = []
        low_priority = []
        
        core_skills = {'python', 'java', 'javascript', 'sql', 'rest', 'api'}
        infrastructure_skills = {'docker', 'kubernetes', 'aws', 'azure', 'linux', 'devops'}
        soft_skills = {'communication', 'leadership', 'teamwork', 'management'}
        
        for skill in gaps['missing_skills']:
            skill_lower = skill.lower()
            
            if any(core in skill_lower for core in core_skills):
                high_priority.append(skill)
            elif any(infra in skill_lower for infra in infrastructure_skills):
                medium_priority.append(skill)
            elif any(soft in skill_lower for soft in soft_skills):
                low_priority.append(skill)
            else:
                medium_priority.append(skill)
        
        return {
            'total_missing': len(gaps['missing_skills']),
            'matched_count': len(gaps['matched_skills']),
            'gap_percentage': gaps['gap_percentage'],
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority,
            'all_missing': gaps['missing_skills']
        }
