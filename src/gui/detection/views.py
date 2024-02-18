from django.shortcuts import render, redirect
from .forms import DocumentoForm
from .models import Documento
from django.http import Http404
from .detect import detect

def upload_and_compare(request):
    if request.method == 'POST':
        form1 = DocumentoForm(request.POST, request.FILES, prefix="doc1")
        form2 = DocumentoForm(request.POST, request.FILES, prefix="doc2")
        if form1.is_valid() and form2.is_valid():
            doc1_file = request.FILES.get('doc1-file', None)
            doc2_file = request.FILES.get('doc2-file', None)

            doc1 = form1.save(commit=False)
            doc2 = form2.save(commit=False)

            if doc1_file:
                doc1.name = doc1_file.name
            if doc2_file:
                doc2.name = doc2_file.name

            doc1.save()
            doc2.save()

            return redirect('show_results', doc1_id=doc1.id, doc2_id=doc2.id)
    else:
        form1 = DocumentoForm(prefix="doc1")
        form2 = DocumentoForm(prefix="doc2")
    return render(request, 'upload_and_compare.html', {'form1': form1, 'form2': form2})


def show_results(request, doc1_id, doc2_id):
    try:
        doc1 = Documento.objects.get(pk=doc1_id)
        doc2 = Documento.objects.get(pk=doc2_id)
    except Documento.DoesNotExist:
        raise Http404("Document doesn´t exists")
    
    with open(doc1.file.path, 'r') as file1, open(doc2.file.path, 'r') as file2:
        _doc1_text = file1.read()
        _doc2_text = file2.read()

        documentos = [_doc1_text, _doc2_text]

        plagiarism, theme, different = detect(documentos)

        def join(intervals_1, intervals_2):
            mixed = [(interval, True) for interval in intervals_1] + [(interval, False) for interval in intervals_2]

            mixed.sort(key=lambda x: (x[0][0], x[0][1]))

            resultado = []

            for interval, is_plagio in mixed:
                if resultado and resultado[-1][0] == interval:
                    continue
                resultado.append((interval, is_plagio))

            return resultado
        
        plagio_doc1 = join([p[0][1] for p in plagiarism], [t[0][1] for t in theme])
        plagio_doc2 = join([p[1][1] for p in plagiarism], [t[1][1] for t in theme])

        doc1_text = _doc1_text
        doc2_text = _doc2_text

        for pos, is_plagio in reversed(plagio_doc1):
            start = pos[0]
            end = pos[1]

            doc1_text = doc1_text[:end] + "</span>" + doc1_text[end:]
            doc1_text = doc1_text[:start] + ("<span class='resaltado'>" if is_plagio else "<span class='resaltadoYellow'>") + doc1_text[start:]
        
        for pos, is_plagio in reversed(plagio_doc2):
            start = pos[0]
            end = pos[1]

            doc2_text = doc2_text[:end] + "</span>" + doc2_text[end:]
            doc2_text = doc2_text[:start] + ("<span class='resaltado'>" if is_plagio else "<span class='resaltadoYellow'>") + doc2_text[start:]

        mixed_12 = {}

        for doc_1, doc_2, similitud in plagiarism:
            if doc_1[1] not in mixed_12:
                mixed_12[doc_1[1]] = []
            mixed_12[doc_1[1]].append((_doc2_text[doc_2[1][0] : doc_2[1][1]], "#ffcccc"))

        for doc_1, doc_2, similitud in theme:
            if doc_1[1] not in mixed_12:
                mixed_12[doc_1[1]] = []
            mixed_12[doc_1[1]].append((_doc2_text[doc_2[1][0] : doc_2[1][1]], "#ffff00"))

        data_match_12 = [(_doc1_text[key[0] : key[1]], value) for key, value in mixed_12.items()]

        mixed_21 = {}

        for doc_1, doc_2, similitud in plagiarism:
            if doc_2[1] not in mixed_21:
                mixed_21[doc_2[1]] = []
            mixed_21[doc_2[1]].append((_doc1_text[doc_1[1][0] : doc_1[1][1]], "#ffcccc"))

        for doc_1, doc_2, similitud in theme:
            if doc_2[1] not in mixed_21:
                mixed_21[doc_2[1]] = []
            mixed_21[doc_2[1]].append((_doc1_text[doc_1[1][0] : doc_1[1][1]], "#ffff00"))

        data_match_21 = [(_doc2_text[key[0] : key[1]], value) for key, value in mixed_21.items()]

        return render(request, 'show_results.html', {'doc1_name': doc1.name, 'doc2_name': doc2.name, 'doc1_text': doc1_text, 'doc2_text': doc2_text, 'data_match_12': data_match_12, 'data_match_21': data_match_21})
