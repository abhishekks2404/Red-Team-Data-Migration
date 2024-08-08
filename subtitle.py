import os
import re
import requests
from fpdf import FPDF

def download_srt(url, filename, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    output_path = os.path.join(folder, filename)
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"Downloaded SRT file saved as {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

def clean_srt_content(srt_content):
    cleaned_lines = []
    for line in srt_content.splitlines():
        # Remove lines that are numbers or contain timestamps
        if not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line):
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def srt_to_pdf(srt_filepath, pdf_filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open(srt_filepath, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    cleaned_content = clean_srt_content(srt_content)
    
    for line in cleaned_content.splitlines():
        pdf.multi_cell(0, 10, line)
    
    pdf.output(pdf_filepath)
    print(f"Converted PDF saved as {pdf_filepath}")

# Main script
# url = "https://videoproxy-production.s3.amazonaws.com/c6f6guo40bhpn3svvs5g/cq5phck2pc3s72o45590/captions/eng.srt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAX76LAXHSXQUYHC5U%2F20240731%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240731T082005Z&X-Amz-Expires=1800&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHAaCXVzLWVhc3QtMSJHMEUCIDgb4IuqjHaRVVZmUUHM8vO5fbems6USI3dEu8wGrO%2FIAiEAuccxthtEp42uDMv%2BaQ0ToFStFldGLuPKr0%2FKo5bPU%2BAq9AQIWRAEGgw1NDk2NDQ3MTI0MjEiDHgu9VASzWKmsZoH6irRBASu9dhVtrwKhJh9MAivWxjYPV6PxvL6JwxOq7bBkUhXi0VxcUoAQDfkfXbMmGYjWUVf05vsV%2FHgk8vGdK5jj3BZ0KiDe%2FcOZ9QTs3T0%2BCCnakxo32nwV6TM9m4dxzqPWuh3med%2FdXIlAVOBxA0Nd6Qg3N3uPEbPR4fNYQ%2FHI4WyHB9RAHZiRkfkCsJNv4kNoJYCg2wylk5fhxzVTlTdAh9IVT3pHPED0DVHbZCVSPg0volfk3Avw8VqgTlhHnJY75fjUj0wlrY0Z59KhShlWIK%2FgBKproLHXhoIi1XsScpFsZY6Q5cyX4omp%2Fe%2FW8s%2B%2FaQ9juqm%2BMotydwLU54C29ES5q20DJQCs04E1p5RhUpeMFnXcJL3jBK3FXXZApCy8PSKQmdjfO5TitnHxiRRKhe2VE5CphXMRbrX6QVHtX2yIuVfNzuVsxw8N4%2FF2KIgxCWwdY28kXUgK5%2B7rcX9YAaHJXcT9cdXRfeZU00%2FjuPIl95njWAQYzReF0TUfxGPOyiZ9ccX%2FODX3nP%2B8M2vuJ%2F7dDWTLLz0WAnuHegDW%2Fdq52OEs6%2BYzizqHRLsh5%2FMfTBGb1%2BzlNfRtnCR4q7qBq%2F3ek57NFYnhSUWuOJITTw8nvJL63DPo%2B73hB%2BN1blnRBEdpi7fhaWQ%2FYFmwhRWhSN8OKplc%2FWyV%2BzYE78E4ptuUUz35iE6h2HYCxGxuWb%2FPS6VbENQ0rcA9GwloTMFPrWTz8tJ9NiBi57967BAb9N77JDjzzUSIrpUJ7hL2%2Fm3q6Ww9Q2fsV0QqXpDbTM7aH8vMPvSp7UGOpoBfE0RcawFerh7wruYvGvRklTAm60hDyb5gjHj139K71smyUXxwDhXfhowDzegfvBPk4zRqpgcAjjnuCBSm67wpcQyWorLJvidWuogGZz3gNmctBaaTwlV7wwVmH23EMH1DWv%2BrTQTBJiPBpSaqxF3jvq7FJfGZL7K8lmWylofkmI7PBAe%2BxTqwSouxku%2BCHQeGTqIuM%2BeN8a3yw%3D%3D&X-Amz-SignedHeaders=host&response-content-disposition=attachment&X-Amz-Signature=c452aa8ad9c9e919e28397f81f24a6e393a2cea006b7e1fa90546c25ddd8ed75"  # Provide your URL here
# srt_filename = "subtitle5.srt"
# pdf_filename = "subtitle5.pdf"
# folder = "subtitle"

def subtitle_to_pdf(url, srt_filename, pdf_filename, folder):
    if url:
        download_srt(url, srt_filename, folder)
        srt_filepath = os.path.join(folder, srt_filename)
        pdf_filepath = os.path.join(folder, pdf_filename)
        srt_to_pdf(srt_filepath, pdf_filepath)
    else:
        print("Please provide a valid URL.")
