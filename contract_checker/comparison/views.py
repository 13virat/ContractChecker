from django.shortcuts import render
from .models import Comparison
from utils.ollama import call_ollama
from utils.extract_text import extract_from_docx, extract_from_pdf, extract_from_txt
import difflib
from difflib import SequenceMatcher
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from utils.clause_analyzer import analyze_contract_diff

import hashlib
from django.core.cache import cache
from utils.clause_split import extract_clauses  # ⬅️ Add this util to split by clauses


def compare_view(request):
    context = {}
    if request.method == 'POST':
        prev_text = request.POST.get('prev_text', '')
        curr_text = request.POST.get('curr_text', '')

        if 'prev_file' in request.FILES:
            prev_text = extract_file(request.FILES['prev_file'])


        if 'curr_file' in request.FILES:
            curr_text = extract_file(request.FILES['curr_file'])

        if prev_text and curr_text:
            old_clauses = extract_clauses(prev_text)
            new_clauses = extract_clauses(curr_text)

            result = []
            for title, new_clause in new_clauses.items():
                old_clause = old_clauses.get(title, '')
                if old_clause != new_clause:
                    key = hashlib.sha256((title + old_clause + new_clause).encode()).hexdigest()
                    cached = cache.get(key)
                    if cached:
                        res = cached
                    else:
                        res = call_ollama(old_clause, new_clause)
                        cache.set(key, res, timeout=36000)
                    result.append({'clause': title, 'response': res})

            differ = difflib.HtmlDiff(wrapcolumn=80)

            html_diff = differ.make_table(
                prev_text.splitlines(),
                curr_text.splitlines(),
                fromdesc='Previous Version',
                todesc='Current Version',
                context=True,
                numlines=2
            )

            # Calculate similarity score
            similarity_score = calculate_similarity(prev_text, curr_text)

            # Save to DB (optional)
            Comparison.objects.create(
                previous_text=prev_text,
                current_text=curr_text,
                llm_response=str(result)
            )
            
            context = {
                'prev_text': prev_text,
                'curr_text': curr_text,
                'result': result,
                'html_diff': html_diff,
                'similarity_score': similarity_score
            }

    return render(request, 'compare.html', context)


# Extract text from uploaded file
def extract_file(file):
    ext = file.name.lower()
    if ext.endswith('.txt'):
        return extract_from_txt(file)
    elif ext.endswith('.docx'):
        return extract_from_docx(file)
    elif ext.endswith('.pdf'):
        return extract_from_pdf(file)
    else:
        return ""

# Calculate similarity percentage
def calculate_similarity(a, b):
    return round(SequenceMatcher(None, a, b).ratio() * 100, 2)


def history_view(request):
    comparisons = Comparison.objects.order_by('-created_at')
    return render(request, 'history.html', {'comparisons': comparisons})


def comparison_detail_view(request, pk):
    compare = Comparison.objects.get(pk=pk)

    differ = difflib.HtmlDiff()

    html_diff = differ.make_table(
        compare.previous_text.splitlines(),
        compare.current_text.splitlines(),
        fromdesc='Previous Version',
        todesc='Current Version',
        context=True,
        numlines=2
    )

    similarity_score = calculate_similarity(compare.previous_text, compare.current_text)

    return render(request, 'comparison_detail.html', {
        'compare': compare,
        'html_diff': html_diff,
        'similarity_score': similarity_score
    })


def download_report(request, pk):
    compare = Comparison.objects.get(pk=pk)


    differ = difflib.HtmlDiff(wrapcolumn=80)
    html_diff = differ.make_table(
        compare.previous_text.splitlines(),
        compare.current_text.splitlines(),
        fromdesc='Previous Version',
        todesc='Current Version',
        context=True,
        numlines=2
    )

    similarity_score = calculate_similarity(compare.previous_text, compare.current_text)

    html_string = render_to_string('report_template.html', {
        'compare': compare,
        'html_diff': html_diff,
        'similarity_score': similarity_score
    })

    pdf_file = HTML(string=html_string).write_pdf()
    return HttpResponse(pdf_file, content_type='application/pdf')

def home_view(request):
    return render(request, 'main.html')

def smart_contract_analyzer_view(request):
    context = {}
    if request.method == 'POST':
        prev_text = request.POST.get('prev_text', '')
        curr_text = request.POST.get('curr_text', '')

        if 'prev_file' in request.FILES:
            prev_file = request.FILES['prev_file']
            prev_text = extract_file(prev_file)

        if 'curr_file' in request.FILES:
            curr_file = request.FILES['curr_file']
            curr_text = extract_file(curr_file)

        if prev_text and curr_text:
            clause_analysis = analyze_contract_diff(prev_text, curr_text)

            context = {
                'prev_text': prev_text,
                'curr_text': curr_text,
                'clause_differences': clause_analysis['differences'],
                'red_flags': clause_analysis['red_flags']
            }

    return render(request, 'smart_analyze.html', context)