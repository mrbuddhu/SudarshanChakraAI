import requests
import json
import os
from typing import Dict, Any, Optional
import openai
from anthropic import Anthropic
from transformers import pipeline
import subprocess
import time

class LLMService:
    def __init__(self):
        """Initialize LLM service with multiple provider support"""
        self.current_config = {
            'provider': 'huggingface',
            'apiKey': '',
            'model': 'microsoft/DialoGPT-medium',
            'isEnabled': True
        }
        self.text_generator = None
        self.setup_fallback_model()

    def setup_fallback_model(self):
        """Setup Hugging Face fallback model"""
        try:
            self.text_generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                device=-1
            )
            print("✅ Fallback LLM model loaded")
        except Exception as e:
            print(f"⚠️ Fallback model not available: {e}")

    def update_config(self, config: Dict[str, Any]):
        """Update LLM configuration"""
        self.current_config.update(config)
        print(f"🔄 LLM config updated: {config['provider']} - {config['model']}")

    def generate_explanation(self, vuln_type: str, line_content: str, code: str) -> str:
        """Generate vulnerability explanation using configured LLM"""
        if not self.current_config.get('isEnabled', False):
            return self._get_fallback_explanation(vuln_type)

        provider = self.current_config['provider']
        
        try:
            if provider == 'openai':
                return self._generate_openai_explanation(vuln_type, line_content, code)
            elif provider == 'anthropic':
                return self._generate_anthropic_explanation(vuln_type, line_content, code)
            elif provider == 'huggingface':
                return self._generate_huggingface_explanation(vuln_type, line_content, code)
            elif provider == 'local':
                return self._generate_local_explanation(vuln_type, line_content, code)
            else:
                return self._get_fallback_explanation(vuln_type)
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            return self._get_fallback_explanation(vuln_type)

    def generate_fix(self, vuln_type: str, line_content: str) -> str:
        """Generate fix suggestion using configured LLM"""
        if not self.current_config.get('isEnabled', False):
            return self._get_fallback_fix(vuln_type)

        provider = self.current_config['provider']
        
        try:
            if provider == 'openai':
                return self._generate_openai_fix(vuln_type, line_content)
            elif provider == 'anthropic':
                return self._generate_anthropic_fix(vuln_type, line_content)
            elif provider == 'huggingface':
                return self._generate_huggingface_fix(vuln_type, line_content)
            elif provider == 'local':
                return self._generate_local_fix(vuln_type, line_content)
            else:
                return self._get_fallback_fix(vuln_type)
        except Exception as e:
            print(f"❌ LLM fix generation failed: {e}")
            return self._get_fallback_fix(vuln_type)

    def _generate_openai_explanation(self, vuln_type: str, line_content: str, code: str) -> str:
        """Generate explanation using OpenAI"""
        if not self.current_config.get('apiKey'):
            raise Exception("OpenAI API key not configured")

        openai.api_key = self.current_config['apiKey']
        
        prompt = f"""
        Explain this {vuln_type} vulnerability found in code:
        Line: {line_content}
        
        Provide a detailed explanation of:
        1. Why this is dangerous
        2. How attackers can exploit it
        3. What could happen if exploited
        
        Keep it clear and technical.
        """
        
        response = openai.ChatCompletion.create(
            model=self.current_config['model'],
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert analyzing code vulnerabilities."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        return response.choices[0].message.content

    def _generate_openai_fix(self, vuln_type: str, line_content: str) -> str:
        """Generate fix using OpenAI"""
        if not self.current_config.get('apiKey'):
            raise Exception("OpenAI API key not configured")

        openai.api_key = self.current_config['apiKey']
        
        prompt = f"""
        Provide a fix for this {vuln_type} vulnerability:
        Vulnerable code: {line_content}
        
        Give:
        1. Secure code example
        2. Best practices to follow
        3. Additional security measures
        
        Keep it practical and actionable.
        """
        
        response = openai.ChatCompletion.create(
            model=self.current_config['model'],
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert providing secure code fixes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        return response.choices[0].message.content

    def _generate_anthropic_explanation(self, vuln_type: str, line_content: str, code: str) -> str:
        """Generate explanation using Anthropic Claude"""
        if not self.current_config.get('apiKey'):
            raise Exception("Anthropic API key not configured")

        anthropic = Anthropic(api_key=self.current_config['apiKey'])
        
        prompt = f"""
        Explain this {vuln_type} vulnerability found in code:
        Line: {line_content}
        
        Provide a detailed explanation of:
        1. Why this is dangerous
        2. How attackers can exploit it
        3. What could happen if exploited
        
        Keep it clear and technical.
        """
        
        response = anthropic.messages.create(
            model=self.current_config['model'],
            max_tokens=300,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

    def _generate_anthropic_fix(self, vuln_type: str, line_content: str) -> str:
        """Generate fix using Anthropic Claude"""
        if not self.current_config.get('apiKey'):
            raise Exception("Anthropic API key not configured")

        anthropic = Anthropic(api_key=self.current_config['apiKey'])
        
        prompt = f"""
        Provide a fix for this {vuln_type} vulnerability:
        Vulnerable code: {line_content}
        
        Give:
        1. Secure code example
        2. Best practices to follow
        3. Additional security measures
        
        Keep it practical and actionable.
        """
        
        response = anthropic.messages.create(
            model=self.current_config['model'],
            max_tokens=300,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

    def _generate_huggingface_explanation(self, vuln_type: str, line_content: str, code: str) -> str:
        """Generate explanation using Hugging Face"""
        if not self.text_generator:
            raise Exception("Hugging Face model not available")

        prompt = f"Explain this {vuln_type} vulnerability: {line_content}"
        
        response = self.text_generator(prompt, max_length=200, num_return_sequences=1)
        return response[0]['generated_text']

    def _generate_huggingface_fix(self, vuln_type: str, line_content: str) -> str:
        """Generate fix using Hugging Face"""
        if not self.text_generator:
            raise Exception("Hugging Face model not available")

        prompt = f"Fix this {vuln_type} vulnerability: {line_content}"
        
        response = self.text_generator(prompt, max_length=200, num_return_sequences=1)
        return response[0]['generated_text']

    def _generate_local_explanation(self, vuln_type: str, line_content: str, code: str) -> str:
        """Generate explanation using local Ollama model"""
        try:
            prompt = f"Explain this {vuln_type} vulnerability: {line_content}"
            
            response = subprocess.run([
                'ollama', 'run', self.current_config['model'], prompt
            ], capture_output=True, text=True, timeout=30)
            
            if response.returncode == 0:
                return response.stdout.strip()
            else:
                raise Exception(f"Ollama error: {response.stderr}")
        except Exception as e:
            print(f"Local model error: {e}")
            return self._get_fallback_explanation(vuln_type)

    def _generate_local_fix(self, vuln_type: str, line_content: str) -> str:
        """Generate fix using local Ollama model"""
        try:
            prompt = f"Fix this {vuln_type} vulnerability: {line_content}"
            
            response = subprocess.run([
                'ollama', 'run', self.current_config['model'], prompt
            ], capture_output=True, text=True, timeout=30)
            
            if response.returncode == 0:
                return response.stdout.strip()
            else:
                raise Exception(f"Ollama error: {response.stderr}")
        except Exception as e:
            print(f"Local model error: {e}")
            return self._get_fallback_fix(vuln_type)

    def _get_fallback_explanation(self, vuln_type: str) -> str:
        """Get fallback explanation"""
        return f"**{vuln_type} Vulnerability Detected**\n\nThis vulnerability was detected in your code and requires immediate attention. Please review the code and implement proper security measures."

    def _get_fallback_fix(self, vuln_type: str) -> str:
        """Get fallback fix suggestion"""
        return f"**Fix for {vuln_type}**\n\nPlease review the code and implement proper security measures for this vulnerability."

    def test_connection(self) -> Dict[str, Any]:
        """Test LLM connection"""
        try:
            provider = self.current_config['provider']
            
            if provider == 'openai':
                return self._test_openai()
            elif provider == 'anthropic':
                return self._test_anthropic()
            elif provider == 'huggingface':
                return self._test_huggingface()
            elif provider == 'local':
                return self._test_local()
            else:
                return {'status': 'error', 'message': 'Unknown provider'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _test_openai(self) -> Dict[str, Any]:
        """Test OpenAI connection"""
        if not self.current_config.get('apiKey'):
            return {'status': 'error', 'message': 'API key not configured'}
        
        try:
            openai.api_key = self.current_config['apiKey']
            response = openai.ChatCompletion.create(
                model=self.current_config['model'],
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return {'status': 'success', 'message': 'OpenAI connection successful'}
        except Exception as e:
            return {'status': 'error', 'message': f'OpenAI error: {str(e)}'}

    def _test_anthropic(self) -> Dict[str, Any]:
        """Test Anthropic connection"""
        if not self.current_config.get('apiKey'):
            return {'status': 'error', 'message': 'API key not configured'}
        
        try:
            anthropic = Anthropic(api_key=self.current_config['apiKey'])
            response = anthropic.messages.create(
                model=self.current_config['model'],
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            return {'status': 'success', 'message': 'Anthropic connection successful'}
        except Exception as e:
            return {'status': 'error', 'message': f'Anthropic error: {str(e)}'}

    def _test_huggingface(self) -> Dict[str, Any]:
        """Test Hugging Face connection"""
        if self.text_generator:
            return {'status': 'success', 'message': 'Hugging Face model loaded'}
        else:
            return {'status': 'error', 'message': 'Hugging Face model not available'}

    def _test_local(self) -> Dict[str, Any]:
        """Test local Ollama connection"""
        try:
            response = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            if response.returncode == 0:
                return {'status': 'success', 'message': 'Ollama is running'}
            else:
                return {'status': 'error', 'message': 'Ollama not running'}
        except Exception as e:
            return {'status': 'error', 'message': f'Ollama not installed: {str(e)}'}

