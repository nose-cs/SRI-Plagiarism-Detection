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
            doc1 = form1.save()
            doc2 = form2.save()
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
    
    with open(doc1.archivo.path, 'r') as file1, open(doc2.archivo.path, 'r') as file2:
        doc1_text = file1.read()
        doc2_text = file2.read()

        documentos = [doc1_text, doc2_text]

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

        return render(request, 'show_results.html', {'doc1_text': doc1_text, 'doc2_text': doc2_text})
